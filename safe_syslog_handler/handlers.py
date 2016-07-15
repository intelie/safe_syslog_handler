# -*- coding: utf-8 -*-

import errno
from logging.handlers import SysLogHandler
import socket
import sys


class SafeSysLogHandler(SysLogHandler):
    """
        A handler class that inherits from `logging.handlers.SyslogHandler`.

        If using `socket.SOCK_STREAM` as the sockettype and it's not using a unixsocket,
        then this handler will try to restore the socket's connection if target go down.

        It will supress any `[Errno 32] Broken pipe` exception that might occour
        during the emission of the message, and instead will try to reconect the socket.

        If any socket.error exception occours during this reconnection, then this error is handled by
        `logging.handlers.SyslogHandler`. That is, it will try to traceback the exception into `sys.stderr`.
    """

    def is_socketstream_and_not_unixsocket(self):
        return self.socktype == socket.SOCK_STREAM and not self.unixsocket

    def recreate_socket(self):
        self.socket.close()
        self.socket = socket.socket(socket.AF_INET, self.socktype)

    def retry_socketstream_connection(self, record):
        self.recreate_socket()
        try:
            self.socket.connect(self.address)
        except socket.error as e:
            """
            this connection error is handled by SyslogHandler
            that basically will try to traceback into sys.stderr
            """
            SysLogHandler.handleError(self, record)

    def handleError(self, record):
        # not sure if it should check for
        # raiseException and sys.stderr here, just as it's verified in here:
        # https://hg.python.org/cpython/file/2.7/Lib/logging/__init__.py#l808
        ei = sys.exc_info()
        if isinstance(ei[1], socket.error):
            sock_error = ei[1]
            if sock_error.errno == errno.EPIPE and self.is_socketstream_and_not_unixsocket():
                    del ei
                    self.retry_socketstream_connection(record)
                    """
                    will suppress exception
                    so  wont call the baseclasse handleError in here
                    """
                    return

        SysLogHandler.handleError(self, record)
