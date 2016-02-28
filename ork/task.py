import importlib
import functools
import multiprocessing as mp

import redis

from .config import load_config


_TASK_NAME_PREFIX = 'ork'


def task(name=''):
    def _outer_wrapper(wrapped_task):
        @functools.wraps(wrapped_task)
        def _wrapper(*args, **kwargs):
            task_name = '{}:{}'.format(
                _TASK_NAME_PREFIX,
                name or '{}.{}'.format(
                    wrapped_task.__module__,
                    wrapped_task.__name__))
            t = Task(task_name, wrapped_task, *args, **kwargs)
            t.start()
            return t
        return _wrapper
    return _outer_wrapper


class Task:
    def __init__(self, name, task=None, *args, **kwargs):
        self.name = name
        self._config = load_config()['broker']['redis']
        self._task = task
        self._process = mp.Process(target=self._work, args=args, kwargs=kwargs)

    def __repr__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.name)

    def get(self):
        """Return the result of this task

        This is a blocking method.

        """
        r = self._redis_conn()
        res = r.brpop(self.name)
        return res[1].decode()

    def start(self):
        """Start a worker subprocess for this task"""
        self._process.start()

    def _redis_conn(self):
        if getattr(self, '_conn', None):
            return self._conn
        self._conn = redis.StrictRedis(host=self._config['host'],
                                       port=self._config['port'])
        return self._conn

    def _work(self, *args, **kwargs):
        """Process the task's inputs and store its result in a queue

        This is a blocking method.

        """
        r = self._redis_conn()

        inputs = list(args[:])
        for i, inp in enumerate(inputs):
            if isinstance(inp, Task):
                # XXX: Consider using BRPOPLPUSH for improved reliability.
                inputs[i] = inp.get()

        result = self._task(*inputs)

        if result:
            r.rpush(self.name, result)


def load_tasks(config):
    for tmod in config:
        importlib.import_module(tmod)
