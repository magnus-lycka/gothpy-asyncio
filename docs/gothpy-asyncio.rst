:title: GothPy: Coroutines with async and await
:data-transition-duration: 500
:css: gothpy-asyncio.css
:skip-help: false

----

{{ layout.set() }}
{{ layout.children(6, 6, skip=[(1, 2), (2, 2), (3, 2), (4, 2), (1, 3), (2, 3), (3, 3), (4, 3)]) }}

Coroutines with async and await
===============================

*Sweat your CPUs!*
------------------

GothPy 2017-08-23
-----------------

Magnus_ Lyckå_
--------------

.. _Magnus: https://github.com/magnus-lycka
.. _Lyckå: https://www.linkedin.com/in/lycka/

----

{{ layout.set() }}

**IRQ**
=======

----

{{ layout.set() }}

GoCD notifications weren't enough...
====================================

.. raw:: html

    <div align="center">
    <img src="gocd_notifications.png" width="735" height="177" />
    </div>

* Email the whole team about broken and fixed builds.
* Notify on all pipelines in a group.
* If X is in our group, we also need alerts on X-release-x.y.z in the release group.
* Notified in slack instead?

----

{{ layout.set(data_rotate=180) }}

Jag fick en liten idé...
========================

.. raw:: html

    <div align="center">
    <iframe width="853" height="480" src="https://www.youtube.com/embed/2cMbmG8t8vY?rel=0&amp;controls=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>
    </div>

----

{{ layout.set(data_rotate=0) }}

Idea...
=======

* Mail all alerts in GoCD to a special address.
* Intercept all mail from GoCD in special proxy.
* Apply special rules on mails to the special address, pass other mail to the "real" mail server.
* This led to writing mail2alert_

.. raw:: html

    <div align="center">
    <img src="https://raw.githubusercontent.com/magnus-lycka/mail2alert/master/static/mail2alert_logo.png" />
    </div>

.. _mail2alert: https://github.com/magnus-lycka/mail2alert

----

{{ layout.set() }}

Standard library smtpd
======================

This module offers several classes to implement SMTP (email) servers.
---------------------------------------------------------------------


*The aiosmtpd package is a recommended replacement for this module. It is based on asyncio and provides a more straightforward API. smtpd should be considered deprecated.*

Asyncio???
----------

----

{{ layout.set() }}


mail2alert - simplified sequence diagram
========================================

::

    +--------+   +----------+   +--------+   +-----------+
    |Notifyer|   |Mail2alert|   |REST API|   |Mail Server|
    +---+----+   +----+-----+   +----+---+   +------+----+
        |             |              |              |
       +++ SEND      +++             |              |
       | +---------->| | GET        +++             |
       | |           | +----------->| |             |
       | |           | |  200 {...} | |
       | |           | |<-----------+ |             |
       | |           | |            +-+             |
       | |           | | SEND                      +++
       | |           | |-------------------------->| |
       | |           | |                       ACK | + - - -
       | |       ACK | |<--------------------------| |
       | |<----------+ |                           +-+
       +-+           +-+

----

{{ layout.set() }}

Concurrent execution of multiple tasks
======================================

- Preemptive multitasking (OS scheduler)

  - Multiprocessing: Protected but heavy...
  - Multithreading: Faster but hard to debug and still some overhead...

- Cooperative Multitasking (event loop)

  - Callbacks: Code flows backwards? (Example_)
  - Coroutines: ???

.. _Example: https://hackedbellini.org/development/writing-asynchronous-python-code-with-twisted-using-inlinecallbacks/

----

{{ layout.set() }}

Coroutine benefits compared with...
===================================

Processes
    Much less overhead. Always switch context at optimal time.

Threads
    Less overhead. Easier to debug. Always switch context at optimal time.

Callbacks
    Source code easier to read. Flows like non-concurrent code.

*But it can only utilize one CPU core!*
---------------------------------------

----

{{ layout.set() }}

Functions, Generators, Coroutines
=================================

.. code:: python


    def my_function(x):
        return x + 1


    def my_generator(x):
        for i in range(x):
            yield i


    async def my_coroutine(x):
        loop = asyncio.get_event_loop()
        t0 = loop.time()
        await asyncio.sleep(x)
        t1 = loop.time()
        print(t0, t1)

----

{{ layout.set() }}

Python Function
===============

.. code:: python

    >>> def my_function(x):
    ...     return x + 1
    ...
    >>> my_function
    <function my_function at 0x7f2e4b07eea0>
    >>> my_function(3)
    4
    >>>

----

{{ layout.set() }}

Python Generator
================

.. code:: python

    >>> def my_generator(x):
    ...     for i in range(x):
    ...         yield i
    ...
    >>> my_generator
    <function my_generator at 0x7f2e49a09840>
    >>> g = my_generator(2)
    >>> g
    <generator object my_generator at 0x7f2e460bf2b0>
    >>> next(g)
    0
    >>> next(g)
    1
    >>> next(g)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    StopIteration
    >>>

----

{{ layout.set() }}

Python 3.5+ coroutine
=====================

.. code:: python

    >>> import asyncio
    >>> async def my_coroutine(x):
    ...     loop = asyncio.get_event_loop()
    ...     t0 = loop.time()
    ...     await asyncio.sleep(x)
    ...     t1 = loop.time()
    ...     print(t0, t1)
    ...
    >>> my_coroutine
    <function my_coroutine at 0x7f2e49a09840>
    >>> c = my_coroutine(3)
    >>> c
    <coroutine object my_coroutine at 0x7f2e460bf2b0>
    >>> loop = asyncio.get_event_loop()
    >>> loop.run_until_complete(c)
    94327.881889242 94330.884326
    >>>

----

{{ layout.set() }}

Python 3.4 coroutine
====================

.. code:: python

    >>> import asyncio
    >>> @asyncio.coroutine
    >>> def my_coroutine(x):
    ...     loop = asyncio.get_event_loop()
    ...     t0 = loop.time()
    ...     yield from asyncio.sleep(x)
    ...     t1 = loop.time()
    ...     print(t0, t1)
    ...
    >>> my_coroutine
    <function my_coroutine at 0x7f2e459519d8>
    >>> c = my_coroutine(4)
    >>> c
    <generator object my_coroutine at 0x7f2e460bf3b8>
    >>> loop = asyncio.get_event_loop()
    >>> loop.run_until_complete(c)
    95398.736966465 95402.738235799
    >>>

*Don't use this!*

----

{{ layout.set() }}

Timeline
========

* Python 2.x std lib: asyncore & asynchat
* Python 2.x 3rd party: Greenlets, Twisted, gevent etc
* Python 3.4: asyncio (provisional), @asyncio.coroutine
* Python 3.5: async & await syntax (Borrowed from C# / VB.NET)
* Python 3.6: asyncio extended & stable. Async generators & comprehensions.
* Python 3.7: ??? (Simplifications and better docs?) https://www.youtube.com/watch?v=2ZFFv-wZ8_g

----

{{ layout.set() }}
{{ layout.children(6, 11, use=[(2, 3), (3, 3), (4, 3), (5, 3), (2, 4), (2, 5), (3, 5), (4, 5), (3, 6), (4, 6), (3,7), (3, 8)]) }}

Asyncio concepts
================

* Event loops
* Transports
* Protocols
* Futures, Tasks & Coroutines
* Async generators & comprehensions
* Synchronization primitives
* Threadpool interface


----

{{ layout.set() }}

Event Loops
===========

 * The central execution device

  * Register, execute & cancel delayed calls
  * Create client and server transports
  * Launch subprocesses
  * Delegate costly function calls to threadpools

 * Several implementations

  * SelectorEventLoop - Default, limited to sockets in Windows
  * ProactorEventLoop - Only Windows, IOCP
  * uvloop_ - 3rd party, based on libuv_
  * tokio_ - 3rd party, based on Rust event loop tokio-rs_.



.. _uvloop: https://github.com/MagicStack/uvloop
.. _libuv: https://github.com/libuv/libuv
.. _tokio: https://pypi.python.org/pypi/tokio
.. _tokio-rs: https://tokio.rs/

----

{{ layout.set() }}

Event Loop objects
==================

.. code:: python

    loop = asyncio.get_event_loop()

    loop.create_task( coroutine )

    loop.run_until_complete( coroutine or task )

    loop.run_forever()

    loop.call_*( function, *args)

    loop.time()

    loop.stop()

    loop.close()

    ...

----

{{ layout.set() }}

Event Loop Hello World
======================

.. code:: python

    import asyncio

    def hello_world(loop):
        print('Hello World')
        loop.stop()

    loop = asyncio.get_event_loop()

    # Schedule a call to hello_world()
    loop.call_soon(hello_world, loop)

    # Blocking call interrupted by loop.stop()
    loop.run_forever()
    loop.close()

----

{{ layout.set() }}

uvloop
======

.. raw:: html

    <div align="center">
    <img src="uvloop_performance.png" width="1053" height="385" />
    </div>

https://github.com/MagicStack/uvloop

----

{{ layout.set() }}

Transports & Protocols
======================

Borrowed from Twisted

Transports
    E.g. TCP, UDP, Pipes

Protocols
    E.g. HTTP, echo

You're likely to stick to standard transports, but to subclass asyncio.Protocol unless you just use HTTP etc.
There are examples_ in the docs.

.. _examples: https://docs.python.org/3/library/asyncio-protocol.html#protocol-examples

----

{{ layout.set() }}

Futures
=======

* Encapsulates the asynchronous execution of a callable.
* Almost compatible with concurrent.futures.Future.
* Methods: .cancel(), .cancelled(), .set_result(), .result(), .done()

.. code:: python

    import asyncio

    async def slow_operation(future):
        await asyncio.sleep(1)
        future.set_result('Future is done!')

    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    asyncio.ensure_future(slow_operation(future))
    loop.run_until_complete(future)
    print(future.result())
    loop.close()

----

{{ layout.set() }}

Tasks
=====

"Subclass of Future. Wrapper around coroutine to schedule it for execution.

A task is responsible for executing a coroutine object in an event loop.

If the wrapped coroutine yields from a future, the task suspends the execution
of the wrapped coroutine and waits for the completion of the future.

When the future is done, the execution of the wrapped coroutine restarts with
the result or the exception of the future."

----

{{ layout.set() }}
{{ layout.children(3, 3, use=[(1, 2)]) }}

Handle
======

class asyncio.Handle
    A callback wrapper object returned by loop.call_soon(), loop.call_soon_threadsafe(), loop.call_later(), and loop.call_at().

cancel()
    Cancel the call. If the callback is already canceled or executed, this method has no effect.

----

{{ layout.set() }}


Event Loop Hello World
======================

.. code:: python

    import asyncio

    def hello_world(loop):
        print('Hello World')
        loop.stop()

    loop = asyncio.get_event_loop()

    # Schedule a call to hello_world()
    handle = loop.call_soon(hello_world, loop)

    # we could...
    handle.cancel()

    # Blocking call interrupted by loop.stop()
    loop.run_forever()
    loop.close()


----

{{ layout.set() }}

Async generators and comprehension
==================================

.. code:: python


    async def ticker(delay, to):
        for i in range(to):
            yield i
            await asyncio.sleep(delay)


    result = [i async for i in aiter() if i % 2]


    result = [await fun() for fun in funcs if await condition()]


----

{{ layout.set() }}


Async for???
============

.. code:: python


    async for i in f():
        ....

VS

.. code:: python


    for i in await f():
        ....

----

{{ layout.set() }}


Synchronization primitives
==========================

Locks
    - Lock
    - Event
    - Condition

Semaphores
    - Semaphore
    - BoundedSemaphore

Very similar to those in the threading module,
but since there is no preemptive scheduling,
they aren't needed so often.

----

{{ layout.set() }}

Threadpool interface
====================


If you can't avoid blocking I/O, you can hand over work to
a concurrent.futures.ThreadPoolExecutor or
a concurrent.futures.ProcessPoolExecutor.


.. code:: python

    loop.run_in_executor(executor, func, *args)

----

{{ layout.set() }}

Asynchronous Context Managers
=============================

A context manager which is able to suspend execution in its enter and exit methods.

.. code:: python

    class AsyncContextManager:
        async def __aenter__(self):
            await log('entering context')

        async def __aexit__(self, exc_type, exc, tb):
            await log('exiting context')

...

.. code:: python

    async def commit(session, data):
        ...

        async with session.transaction():
            ...
            await session.update(data)
            ...

----

{{ layout.set() }}

Don't use blocking I/O!
=======================

* No socket.*
* No select.*
* No subprocess.*
* No os.waitpid
* No threading.*
* No multiprocessing.*
* No time.sleep

*Use async replacements!*

----

{{ layout.set() }}

Split up all long loops!
========================

*Or use the threadpool etc*
---------------------------

----

{{ layout.set() }}

Too confusing?
==============


    *"Man that thing is complex and it keeps getting more complex.
    I do not have the mental capacity to casually work with asyncio."*

         -- Armin Ronacher

http://lucumr.pocoo.org/2016/10/30/i-dont-understand-asyncio/


    Why is he mixing multi-threading with asyncio?

----

{{ layout.set() }}

Callback soup considered harmful
================================

    *Your async/await functions are dumplings of local structure
    floating on top of callback soup, and this has far-reaching
    implications for the simplicity and correctness of your code.*

        -- Nathaniel J. Smith

https://vorpus.org/blog/some-thoughts-on-asynchronous-api-design-in-a-post-asyncawait-world/

----

{{ layout.set() }}
{{ layout.children(3, 12, use=[(1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8)]) }}

Minimal knowledge...
====================

* asyncio.get_event_loop()
* loop.create_task()
* loop.run_until_complete()
* loop.run_forever()
* asyncio.gather()
* loop.run_in_executor()
* loop.close()

----

{{ layout.set() }}

asyncio.get_event_loop()
========================

*You know this by now...*

----

{{ layout.set() }}

loop.create_task(coroutine)
===========================

Schedule the execution of a coroutine object.

Wrap it in a task object and return that task.

----

{{ layout.set() }}

loop.run_until_complete(coroutine)
==================================

Pass in a coroutine or a future(task).

----

{{ layout.set() }}

loop.run_forever()
==================

After you created tasks...

----

{{ layout.set() }}

asyncio.gather(coroutines_or_futures, ...)
==========================================

Return a future aggregating results from the given coroutine objects or futures.

.. code:: python

    import asyncio

    async def factorial(name, number):
        f = 1
        for i in range(2, number+1):
            print("Task %s: Compute factorial(%s)..." % (name, i))
            await asyncio.sleep(1)
            f *= i
        print("Task %s: factorial(%s) = %s" % (name, number, f))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    ))
    loop.close()

----

{{ layout.set() }}

loop.run_in_executor(executor, function, args, ...)
===================================================

Call a function in an Executor (pool of threads or pool of processes). By default, an event loop uses a thread pool executor (ThreadPoolExecutor).

Returns a coroutine.

----

{{ layout.set() }}

Some code examples...
=====================

* Watchdog
* Parallel fetch
* https://github.com/magnus-lycka/mail2alert

----

{{ layout.set() }}

Some networking libraries
=========================

* https://github.com/aio-libs/aiohttp
* https://github.com/aio-libs/aiosmtpd
* https://github.com/channelcat/sanic


* https://github.com/aio-libs/aiozmq
* https://github.com/Polyconseil/aioamqp
* https://github.com/aio-libs/aiokafka

----

{{ layout.set() }}

Not only networking...
======================

* https://github.com/magicstack/asyncpg
* https://github.com/aio-libs/aiomysql
* https://github.com/mongodb/motor
* https://github.com/elastic/elasticsearch-py-async
* https://github.com/aio-libs/aioredis
* https://github.com/aio-libs/aiomcache

* https://github.com/Tinche/aiofiles/
* https://github.com/aio-libs/aiobotocore
* https://github.com/aio-libs/aiodocker

----

{{ layout.set() }}

Testing with asyncio
====================

* https://blog.miguelgrinberg.com/post/unit-testing-asyncio-code
* https://asynctest.readthedocs.io/en/latest/
* https://github.com/pytest-dev/pytest-asyncio
* http://aiohttp.readthedocs.io/en/stable/testing.html
* https://github.com/magnus-lycka/mail2alert/tree/master/src/test

----

{{ layout.set() }}

Debugging with asyncio
======================

.. code:: python

    if args.verbose:
        logging.getLogger('asyncio').setLevel(logging.DEBUG)

        # Enable debugging
        event_loop.set_debug(True)

        # Make the threshold for "slow" tasks very very small for
        # illustration. The default is 0.1, or 100 milliseconds.
        event_loop.slow_callback_duration = 0.001

        # Report all mistakes managing asynchronous resources.
        warnings.simplefilter('always', ResourceWarning)

...

.. code:: bash

    $ export PYTHONASYNCIODEBUG=1

- https://pymotw.com/3/asyncio/debugging.html
- https://github.com/aio-libs/aiomonitor

----

{{ layout.set() }}

References
==========

- https://docs.python.org/3/library/asyncio.html
- https://github.com/aio-libs
- https://github.com/magnus-lycka/mail2alert
- https://github.com/magnus-lycka/gothpy-asyncio
- https://github.com/MagicStack/uvloop
- http://lucumr.pocoo.org/2016/10/30/i-dont-understand-asyncio/
- https://pymotw.com/3/asyncio/
- https://github.com/timofurrer/awesome-asyncio
- https://www.youtube.com/watch?v=2ZFFv-wZ8_g
