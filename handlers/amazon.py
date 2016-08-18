#!/usr/bin/env python
# coding=utf-8
# author=haishan09@gmail.com
import re
from tornado import gen
from tornado.web import asynchronous
from tornado.httpclient import AsyncHTTPClient, HTTPClient
from handlers.base import BaseHandler
from utils.urlmap import urlmap
from BeautifulSoup import BeautifulSoup


@urlmap(url=r'/amazon/topreviewers')
class TopReviewers(BaseHandler):

    # start_url = 'https://www.amazon.com/review/top-reviewers/ref=cm_cr_tr_link_3?ie=UTF8&page=3'
    start_url = 'https://www.amazon.com/review/top-reviewers/ref=cm_cr_tr_link_4?ie=UTF8&page=4'

    @asynchronous
    @gen.coroutine
    def get(self):
        cli = AsyncHTTPClient()
        yield cli.fetch(self.start_url, self.callback)

    def extract_mail(self, profile_url):
        self.write('<br/>')
        cli = HTTPClient()
        response = cli.fetch(profile_url)
        parsed_html = BeautifulSoup(response.body)
        email = parsed_html.find(rel='nofollow')
        if not email:
            self.write('email address not found')
        else:
            self.write(email.text)
        self.write('<br/>')
        self.flush()
         

    def callback(self, response):
        parsed_html = BeautifulSoup(response.body)
        for tr in parsed_html.findAll('tr', id=re.compile('reviewer*')):
            tds = tr.findAll('td')
            name = tds[2].a.b.text
            href = tds[1].a.get('href')
            self.write(name)
            self.extract_mail('https://www.amazon.com' + href)
            self.write('<br/>')
        self.finish()

