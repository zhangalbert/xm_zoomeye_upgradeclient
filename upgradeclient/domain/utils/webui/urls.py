#! -*- coding: utf-8 -*-


url_patterns = [
    r'/(.*)/', 'RedirectView',
    r'/', 'IndexView'
    r'/static/(js|css|img)/(.*)', 'StaticFileView'
]
