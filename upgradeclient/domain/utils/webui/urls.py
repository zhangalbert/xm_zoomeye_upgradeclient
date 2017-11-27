#! -*- coding: utf-8 -*-


url_patterns = [
    r'/(.*)/', 'RedirectView',
    r'/', 'IndexView',
    r'/statics/(js|css|img|fonts)/(.*)', 'StaticFileView',
    r'/ajax/exception/threads', 'ExceptionThreadView',
    r'/ajax/exception/fmodels', 'ExceptionFmodelView',
    r'/ajax/exception/excepts', 'ExceptionExceptView',
    r'/ajax/exception/realtime', 'ExceptionRealtimeView',
    r'/firmware/([0-9])', 'FirmwareDetailView',
]
