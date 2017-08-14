:title: GothPy: Coroutines with async and await
:data-transition-duration: 500
:css: gothpy-asyncio.css
:skip-help: true


----

:data-scale: 6


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

:data-scale: 1
:data-x: -4000
:data-y: -2500

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

:data-rotate: 180
:data-x: r2000
:data-y: r0

Jag fick en liten idé...
========================

.. raw:: html

    <div align="center">
    <iframe width="853" height="480" src="https://www.youtube.com/embed/2cMbmG8t8vY?rel=0&amp;controls=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>
    </div>

----

:data-rotate: 0


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

:data-x: r-8000
:data-y: r1000

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

:data-x: r2000
:data-y: r0

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

:data-transition-duration: 0

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


:data-x: r-8000
:data-y: r1200
:data-rotate: 30

Timeline
========

* Python 2.x std lib: asyncore & asynchat
* Python 2.x 3rd party: Greenlets, Twisted etc
* Python 3.4: asyncio (provisional), @asyncio.coroutine & yield from
* Python 3.5: async & await syntax
* Python 3.6: asyncio extended & stable. Async generators & comprehensions.


----

:data-x: r8000
:data-y: r0
:data-rotate: 45

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

:data-x: r-8000
:data-y: r1200
:data-rotate: -45

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

.. _uvloop: https://github.com/MagicStack/uvloop
.. _libuv: https://github.com/libuv/libuv

----

:data-x: r8000
:data-y: r0
:data-rotate: -45

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

:data-x: r-8000
:data-y: r1200
:data-rotate: 0

uvloop
======

.. raw:: html

    <div align="center">
    <img src="uvloop_performance.png" width="1053" height="385" />
    </div>

https://github.com/MagicStack/uvloop

----

:data-x: r2000
:data-y: r0


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

Futures
=======

* Encapsulates the asynchronous execution of a callable.
* Almost compatible with concurrent.futures.Future.

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

Tasks
=====

"Subclass of Future. Wrapper around coroutine to schedule it for execution.

A task is responsible for executing a coroutine object in an event loop.

If the wrapped coroutine yields from a future, the task suspends the execution
of the wrapped coroutine and waits for the completion of the future.

When the future is done, the execution of the wrapped coroutine restarts with
the result or the exception of the future."

----

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

:data-x: r-8000
:data-y: r1000

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

:data-x: r2000
:data-y: r0

Threadpool interface
====================


If you can't avoid blocking I/O, you can hand over work to
a concurrent.futures.ThreadPoolExecutor or
a concurrent.futures.ProcessPoolExecutor.


.. code:: python

    loop.run_in_executor(executor, func, *args)

----

Too confusing?
==============


    *"Man that thing is complex and it keeps getting more complex.
    I do not have the mental capacity to casually work with asyncio."*

         -- Armin Ronacher

http://lucumr.pocoo.org/2016/10/30/i-dont-understand-asyncio/


    Why is he mixing multi-threading with asyncio?

----

Example: mail2alert
===================

https://github.com/magnus-lycka/mail2alert


----

References
==========

- https://github.com/pyenv/pyenv-installer
- https://docs.python.org/3/library/asyncio.html
- https://github.com/aio-libs
- https://github.com/magnus-lycka/mail2alert
- https://github.com/magnus-lycka/gothpy-asyncio
- https://github.com/MagicStack/uvloop
- http://lucumr.pocoo.org/2016/10/30/i-dont-understand-asyncio/
