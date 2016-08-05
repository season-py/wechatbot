from collections import defaultdict

class UrlMap(object):

    def __init__(self):
        self.handlers = defaultdict(lambda: [])

    def __call__(self, appkey=0, url=r'/'):
        def urlmap(cls): 
            if isinstance(appkey, (list, tuple)):
                for each_appkey in appkey:
                    self.handlers[each_appkey].append((url, cls))
            else:
                self.handlers[appkey].append((url, cls))
            return cls
        return urlmap

urlmap = UrlMap()
