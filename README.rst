===============================
Safe Syslog Handler
===============================


.. image:: https://img.shields.io/pypi/v/safe_syslog_handler.svg
        :target: https://pypi.python.org/pypi/safe_syslog_handler

.. image:: https://img.shields.io/travis/intelie/safe_syslog_handler.svg
        :target: https://travis-ci.org/intelie/safe_syslog_handler

.. image:: https://readthedocs.org/projects/safe-syslog-handler/badge/?version=latest
        :target: https://safe-syslog-handler.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status



SafeSysLogHandler recreates the connection to a remote logging server when the connection is lost, avoiding the `[errno 32] Broken Pipe` error which would occur when using the `SysLogHandler`.


* Free software: Apache Software License 2.0
* Documentation: https://safe-syslog-handler.readthedocs.io.

Instalation
-----------

.. code-block:: console

    $ pip install safe_syslog_handler



Usage
------


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

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _example: https://github.com/intelie/safe_syslog_handler/tree/master/example
