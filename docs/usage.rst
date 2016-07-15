=====
Usage
=====


If you have some simple logging configured, exemple::

    from logging import config
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'syslog': {
                'format': '%(asctime)s %(hostname)s %(name)s: #{filename:%(filename)s} #{line:%(lineno)d} #{process:%(process)d} #{thread:%(thread)d} %(message)s\n',
                'datefmt': '%b %d %H:%M:%S',
            },
        },
        'loggers': {
            'my-app': {
                'handlers': ['syslog_handlers', ],
                'level': logging.DEBUG,
                'propagate': True,
            },
        }
    }


Then you just need to add this::

    LOGGING['handlers'] = {
        'syslog_handlers': {
            'formatter': 'syslog',
            'class': 'safe_syslog_handler.handlers.SafeSysLogHandler',
            'socktype': socket.SOCK_STREAM,
            'address': ('localhost', 5140),
        }
    }


You can see an example app in the example_ folder