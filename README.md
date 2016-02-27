ork
===

Ork is a distributed task orchestrator for Python.

It allows you to run potentially resource intensive tasks across one or more
machines, create task workflows and schedule periodic tasks.

It uses [Redis](http://redis.io/) to coordinate message passing between tasks,
but in the future other backends might be added.


Setup
-----
```
pip install ork
```

This should make the `ork` command available in your `$PATH`. Run `ork --help`
for more information.


Usage
-----

TBA


Why?
----

There are already plenty of distributed task systems for Python. Listed below
are some of the more popular ones, and the drawbacks of each that led me to
write ork.

- [Celery](http://www.celeryproject.org/): undoubtedly the most popular and
  battle-tested one.
  Drawbacks:
  - Large feature set at the expense of a large and complex codebase, and
    steep learning/debugging/tweaking curve. Most Celery deployments need only a
    fraction of its features, but getting it up and running and maintaining is a
    daunting task.
  - Limited and confusing task orchestration features. Sure, [chains and
    chords](http://docs.celeryproject.org/en/latest/userguide/canvas.html)
    get you half-way there, but any [advanced workflows involving
    sub-tasks](https://github.com/celery/celery/issues/1887) are difficult or
    impossible to achieve.
- [RQ](http://python-rq.org/): small and simple.
  Drawbacks:
  - No sophisticated task orchestration features. You can make one job depend on
    another, but it's not possible to create workflows as with Celery.
  - The API, while simple, still requires the user to know about Redis,
    "queues", "jobs", "workers", etc. This can be accomplished with a friendlier
    user interface.
- [Huey](http://huey.readthedocs.org/en/latest/): similar to RQ in purpose,
  small and lightweight.
  Drawbacks:
  - As with RQ, it lacks any task orchestration features.

So, ork aims to achieve a mix of the above:

- API simplicity and user-friendliness of RQ and Huey.
- Powerful orchestration principles exceeding those of Celery, making complex
  workflows simple to read and write.

Now, as with any software, there are drawbacks:

- I am not a distributed computing expert by any stretch of the imagination. My
  CS fundamentals are rusty, at best, and I've never truly used Redis
  professionally. I'm just a Python user who was frustrated by Celery's
  limitations, RabbitMQ/AMQP's complexities, and didn't find anything else that
  fulfills my needs above.
- Needless to say, this was prototyped in a weekend and you surely don't want it
  running anywhere yet. But feel free to spread the word and contribute!


Configuration
-------------

TBA


License
-------

[MIT](LICENSE)
