#!/usr/bin/env python
# coding=utf-8
# author=haishan09@gmail.com
import re
import sys
import time
import logging
import urlparse
from BeautifulSoup import BeautifulSoup
from tornado import httpclient, gen, ioloop, queues

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(message)s')
concurrency = 1
domain = 'https://www.amazon.com'
start_url = 'https://www.amazon.com/review/top-reviewers'
headers = {
    'User-Agent': 'Mozilla/5.0（iPad; U; CPU OS 3_2_1 like Mac OS X; en-us）AppleWebKit/531.21.10（KHTML, like Gecko）Mobile/7B405'
}

@gen.coroutine
def get_reviewers(url_type, url):
    urls = []
    req = httpclient.HTTPRequest(url=url, method='GET', headers=headers)
    try:
        response = yield httpclient.AsyncHTTPClient().fetch(req)
    except Exception, e:
        logging.error('error: {0}, {1}'.format(e.message, url))
    else:
        html = response.body if isinstance(response.body, str) else response.body.decode()
        soup = BeautifulSoup(html)
        paging_span = soup.find('span', {'class': 'paging'})
        if paging_span:
            for a in paging_span.findAll('a'):
                urls.append((0, a.get('href')))
        reviewer_trs = soup.findAll('tr', id=re.compile('reviewer*'))
        for tr in reviewer_trs:
            urls.append((1, domain + tr.findAll('td')[1].a.get('href')))
    raise gen.Return(urls)

@gen.coroutine
def get_contact(url):
    rank, name, contact = 0, None, None
    req = httpclient.HTTPRequest(url=url, method='GET', headers=headers)
    try:
        response = yield httpclient.AsyncHTTPClient().fetch(req)
    except Exception, e:
        logging.error('error: {0}, {1}'.format(e.message, url))
    else:
        logging.debug('fetched {0}'.format(url))
        html = response.body if isinstance(response.body, str) else response.body.decode()
        soup = BeautifulSoup(html)
        rank_node = soup.find('a', {'class': 'a-link-normal top-reviewer-link a-color-base'})
        name_node = soup.find('span', {'class': 'public-name-text'})
        contact_node = soup.find(rel='nofollow')
        if name_node:
            name = name_node.text
        if rank_node:
            rank = rank_node.div.span.text
        if contact_node:
            contact = contact_node.text
            if '@' in contact:
                logging.info((rank, name, contact))

def get_page(url):
    page = urlparse.parse_qs(url).get('page')
    if page:
        return int(page[0])
    return 0
    

@gen.coroutine
def main():

    q = queues.Queue()
    start = time.time()
    fetching, fetched, fetched_page_set = set(), set(), set()

    @gen.coroutine
    def fetch_url():
        current_url_type, current_url = yield q.get()
        try:
            if current_url in fetching:
                return
            if current_url_type == 0 and get_page(current_url) not in fetched_page_set:
                fetching.add(current_url)
                logging.debug('fetching {0}'.format(current_url))
                urls = yield get_reviewers(current_url_type, current_url)
                fetched.add(current_url)
                fetched_page_set.add(get_page(current_url))

                for (url_type, url) in urls:
                    if (url in fetched) or (url_type == 0 and get_page(url) in fetched_page_set):
                        continue
                    yield q.put((url_type, url))
            elif current_url_type == 1 and current_url not in fetched:
                fetching.add(current_url)
                logging.debug('fetching {0}'.format(current_url))
                yield get_contact(current_url)
                fetched.add(current_url)
        except Exception, e:
            logging.error('error: {0}, {1}'.format(e.message, current_url))
        finally:
            q.task_done()

    @gen.coroutine
    def worker():
        while True:
            yield fetch_url()

    q.put((0, start_url))

    for _ in range(concurrency):
        worker()
    yield q.join()
    assert fetching == fetched
    logging.debug('Done in {0} seconds, fetched {1} URLs.'.format(time.time() - start, len(fetched)))


if __name__ == '__main__':
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(main)
