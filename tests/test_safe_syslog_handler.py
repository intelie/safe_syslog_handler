#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_safe_syslog_handler
----------------------------------

Tests for `hanlders` module.
"""

import socket
import errno
import sys
import unittest
from collections import namedtuple
from mock import patch, Mock

from safe_syslog_handler.handlers import SafeSysLogHandler


def simple_broken_pipe_error():
    broken_pipe_error = socket.error()
    broken_pipe_error.errno = errno.EPIPE
    return broken_pipe_error


def simple_socket_mock(connect=None):
    NewSocket = namedtuple('Socket', ['close', 'connect'])
    socket_mock = NewSocket(close=Mock(), connect=connect if connect else Mock())
    return socket_mock


class TestSafeSysLogHandler(unittest.TestCase):

    def setUp(self):
        self.handler = SafeSysLogHandler()

    def tearDown(self):
        self.handler.close()

    def test_is_socketstream_and_not_unixsocket_returns_correctly_true(self):
        self.handler.socktype = socket.SOCK_STREAM
        self.handler.unixsocket = 0

        self.assertEqual(self.handler.is_socketstream_and_not_unixsocket(), True)

    def test_1_is_socketstream_and_not_unixsocket_returns_correctly_false(self):
        self.handler.socktype = socket.SOCK_STREAM
        self.handler.unixsocket = 1

        self.assertEqual(self.handler.is_socketstream_and_not_unixsocket(), False)

    def test_2_is_socketstream_and_not_unixsocket_returns_correctly_false(self):
        self.handler.socktype = socket.SOCK_DGRAM
        self.handler.unixsocket = 0

        self.assertEqual(self.handler.is_socketstream_and_not_unixsocket(), False)

    def test_3_is_socketstream_and_not_unixsocket_returns_correctly_false(self):
        self.handler.socktype = socket.SOCK_DGRAM
        self.handler.unixsocket = 1

        self.assertEqual(self.handler.is_socketstream_and_not_unixsocket(), False)

    @patch('sys.exc_info', return_value=['', simple_broken_pipe_error(), ''])
    @patch('safe_syslog_handler.handlers.SafeSysLogHandler.is_socketstream_and_not_unixsocket', return_value=True)
    @patch('safe_syslog_handler.handlers.SafeSysLogHandler.retry_socketstream_connection')
    def test_handleError_for_broken_pip_exception_should_call_retry_socketstream_connection(self, m_retry, m_is_socket, m_sys_ex):
        record = "record"
        self.handler.handleError(record)
        m_retry.assert_called_once_with(record)

    @patch('sys.exc_info', return_value=['', simple_broken_pipe_error(), ''])
    @patch('safe_syslog_handler.handlers.SafeSysLogHandler.is_socketstream_and_not_unixsocket', return_value=True)
    @patch('logging.handlers.SysLogHandler.handleError')
    def test_handleError_for_broken_pip_exception_shouldnt_call_base_class_handleError(self, m_syslg_h, m_is_socket, m_sys_ex):
        record = "record"
        self.handler.handleError(record)
        assert not m_syslg_h.called, 'SysLogHandler.handleError should not have been called'

    @patch('sys.exc_info', return_value=['', 'SOME_OTHER_ERROR', ''])
    @patch('safe_syslog_handler.handlers.SafeSysLogHandler.is_socketstream_and_not_unixsocket', return_value=True)
    @patch('safe_syslog_handler.handlers.SafeSysLogHandler.retry_socketstream_connection')
    @patch('logging.handlers.SysLogHandler.handleError')
    def test_handleError_for_other_exception_shouldnt_call_retry_socketstream_connection(self, m_syslg_h, m_retry, m_is_socket, m_sys_ex):
        record = "record"
        self.handler.handleError(record)
        assert not m_retry.called, 'LiveLogHandler.retry_socketstream_connection should not have been called'

    @patch('sys.exc_info', return_value=['', 'SOME_OTHER_ERROR', ''])
    @patch('safe_syslog_handler.handlers.SafeSysLogHandler.is_socketstream_and_not_unixsocket', return_value=True)
    @patch('logging.handlers.SysLogHandler.handleError')
    def test_handleError_for_other_exception_should_call_base_class_handleError(self, m_syslg_h, m_is_socket, m_sys_ex):
        record = "record"
        self.handler.handleError(record)
        m_syslg_h.assert_called_once_with(self.handler, record)

    @patch('socket.socket')
    def test_recreate_socket_should_close_socket(self, m_socket):
        self.handler.socket.close()
        mocket_socket = simple_socket_mock()
        self.handler.socket = mocket_socket
        self.handler.recreate_socket()
        mocket_socket.close.assert_called_once()

    @patch('socket.socket')
    def test_recreate_socket_should_create_new_socket_with_same_values(self, m_socket):
        self.handler.socktype = 'sockettype'
        self.handler.recreate_socket()
        m_socket.assert_called_once_with(socket.AF_INET, 'sockettype')

    @patch('safe_syslog_handler.handlers.SafeSysLogHandler.recreate_socket')
    def test_retry_socketstream_connection_should_call_recreate_socket(self, m_recreate):
        self.handler.socket.close()
        self.handler.socket = simple_socket_mock()
        record = 'record'
        self.handler.retry_socketstream_connection(record)
        m_recreate.assert_called_once()

    @patch('safe_syslog_handler.handlers.SafeSysLogHandler.recreate_socket')
    def test_retry_socketstream_connection_should_call_socket_connect(self, m_recreate):
        self.handler.socket.close()
        socket_mock = simple_socket_mock()
        self.handler.socket = socket_mock
        record = 'record'
        self.handler.retry_socketstream_connection(record)
        socket_mock.connect.assert_called_once_with(self.handler.address)

    @patch('logging.handlers.SysLogHandler.handleError')
    @patch('safe_syslog_handler.handlers.SafeSysLogHandler.recreate_socket')
    def test_retry_socketstream_connection_should_let_syslog_handle_errors_in_connection(self, m_recreate, m_sys_log_h):
        self.handler.socket.close()
        socket_mock = simple_socket_mock(connect=Mock(side_effect=socket.error()))
        self.handler.socket = socket_mock
        record = 'record'
        self.handler.retry_socketstream_connection(record)
        m_sys_log_h.assert_called_once_with(self.handler, record)

if __name__ == '__main__':
    sys.exit(unittest.main())
