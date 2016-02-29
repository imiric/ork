import importlib
import functools
import multiprocessing as mp


from .brokers import get_broker
from .config import load_config


_TASK_NAME_PREFIX = 'ork'


def task(name=''):
    def _outer_wrapper(wrapped_task):
        def delay(*args, **kwargs):
            task_name = '{}:{}'.format(
                _TASK_NAME_PREFIX,
                name or '{}.{}'.format(
                    wrapped_task.__module__,
                    wrapped_task.__name__))
            config = load_config()
            t = Task(task_name, get_broker(config), wrapped_task,
                     *args, **kwargs)
            t.start()
            return t

        wrapped_task.delay = delay

        @functools.wraps(wrapped_task)
        def _wrapper(*args, **kwargs):
            return wrapped_task(*args, **kwargs)
        return _wrapper
    return _outer_wrapper


class Task:
    def __init__(self, name, broker, task=None, *args, **kwargs):
        self.name = name
        self._broker = broker
        self._task = task
        self._process = mp.Process(target=self._work, args=args, kwargs=kwargs)

    def __repr__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.name)

    def get(self):
        """Return the result of this task

        This is a blocking method.

        """
        return self._broker.get(self.name)

    def start(self):
        """Start a worker subprocess for this task"""
        self._process.start()

    def _work(self, *args, **kwargs):
        """Process the task's inputs and store its result in a queue

        This is a blocking method.

        """
        inputs = list(args[:])
        for i, inp in enumerate(inputs):
            if isinstance(inp, Task):
                inputs[i] = inp.get()

        result = self._task(*inputs)

        if result:
            self._broker.set(self.name, result)


def load_tasks(config):
    for tmod in config:
        importlib.import_module(tmod)
