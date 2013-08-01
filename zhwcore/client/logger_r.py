from __future__ import absolute_import

from Queue import Queue, Full
import threading
import logging

from scribe.scribe import Client as ScribeClient
from scribe.scribe import LogEntry, ResultCode

from zhwcore.client.thrift_r import get_thrift_client

class LogHandler(logging.Handler):
    """
    i want to log the msg to backend logger
    but do not need the lock.so overwrite lock method

    """

    def __init__(self, logger, level=logging.NOTSET):
        self._logger = logger
        logging.Handler.__init__(self, level)

    def createLock(self):
        pass

    def acquire(self):
        pass

    def release(self):
        pass

    def emit(self, record):
        msg = self.format(record)
        self._logger.Log(msg)

def _gen_py_logger(logstream, name, level=logging.DEBUG):
    formatter = logging.Formatter('time:%(asctime)s level:%(levelname)s msg:%(message)s')
    py_handler = LogHandler(logstream)
    py_handler.setFormatter(formatter)
    py_logger = logging.getLogger(name)
    py_logger.addHandler(py_handler)
    py_logger.setLevel(level)
    return py_logger

class LoggerConsumer(object):
    __slots__ = ('_q', '_host', '_port', '_scribe', '_consumer')
    def __init__(self, q, host, port):
        self._q = q
        self._host = host
        self._port = port
        self._scribe = get_thrift_client(cls=ScribeClient, hosts=['%s:%d' % (self._host, int(self._port))], max_conn_num=1)

    def run(self):
        self._create_consumer()

    def join(self):
        self._consumer.join()

    def _create_consumer(self):
        self._consumer = threading.Thread(target=self._consume_worker)
        self._consumer.setDaemon(True)
        self._consumer.start()

    def _consume_worker(self):
        while True:
            try:
                (category, msg) = self._q.get()
                print 'category:',category, 'msg:',msg
                log_entry = LogEntry(category=category, message=self._encode_msg_str(msg))
                result = self._scribe.Log(messages=[log_entry])
                if result != ResultCode.OK:
                    print result
            except Exception,e:
                print e

    def _encode_msg_str(self, msg):
        if isinstance(msg, str):
            return msg
        else:
            return msg.encode('utf-8')


class LoggerWrapper(object):
    __slots__ = ('_q', '_category')
    def __init__(self, q, category):
        self._q = q
        self._category = category

    def Log(self, msg):
        try:
            _q.put_nowait((self._category, msg))
        except Full:
            print 'queue is full, drop msg'


_q = Queue(maxsize=100000)
logger_consumer = LoggerConsumer(q=_q, host='127.0.0.1', port=1463)

def get_logger_client(logger_name):
    if logger_name not in logger_clients:
        logger_clients[logger_name] = LoggerWrapper(q=_q, category=logger_name)
    return logger_clients[logger_name]


def get_pylogger_client(logger_name, level):
    if (logger_name, level) not in pylogger_clients:
        logstream = LoggerWrapper(q=_q, category=logger_name)
        pylogger_clients[(logger_name, level)] = _gen_py_logger(logstream, logger_name, level=level)
    return pylogger_clients[(logger_name, level)]


logger_clients = {}
pylogger_clients = {}

if __name__ == '__main__':
    xxx = get_logger_client('xxx')
    xxx.Log('log stream')

    pyxxx = get_pylogger_client('pyxxx', logging.DEBUG)
    pyxxx.info('py log stream')

    logger_consumer.run()
    logger_consumer.join()
