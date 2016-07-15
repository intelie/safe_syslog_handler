#!/usr/bin/env python
import time
import logging
import socket
import sys
from logging import config

# some logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'syslog': {
            'format': '%(asctime)s %(hostname)s %(name)s: #{filename:%(filename)s} #{line:%(lineno)d} #{process:%(process)d} #{thread:%(thread)d} %(message)s\n',
            'datefmt': '%b %d %H:%M:%S',
        },
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'my-app': {
            'handlers': ['syslog_handlers', 'stdout'],
            'level': logging.DEBUG,
            'propagate': True,
        },
    }
}

# using LiveLogHandler in port 5140
LOGGING['handlers'].update({
    'syslog_handlers': {
        'formatter': 'syslog',
        'class': 'safe_syslog_handler.handlers.SafeSysLogHandler',
        'socktype': socket.SOCK_STREAM,
        'address': ('localhost', 5140),
    }
})


# append hostname to log
class ContextFilter(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True

config.dictConfig(LOGGING)
logger = logging.getLogger("my-app")
f = ContextFilter()
logger.addFilter(f)


# Send logs forever
i = 0
while True:
    logger.info("testing something %d" % i)
    print("logged: %d" % i)
    time.sleep(1)
    i += 1
