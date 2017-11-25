#! -*- coding: utf-8 -*-


url_patterns = [
    r'/(.*)/', 'RedirectView',
    r'/', 'IndexView'
    r'/statics/(js|css|img)/(.*)', 'StaticFileView'
]
