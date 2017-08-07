# gothpy-asyncio
GothPy presentation / demonstration August 2017

Notes: 
 - Parallelism 101
 - Generator recap...
   - def ... return
   - def ... yield
   - async def await
   - async def await & yield?
 - The seven functions you need:
   - asyncio.get_event_loop()
   - loop.create_task()
   - loop.run_until_complete()
   - loop.run_forever()
   - asyncio.gather()
   - loop.run_in_executor()
   - loop.close()
 - asyncio & https://github.com/aio-libs
 - Python 3.4 vs Python 3.5
   - @coroutine / yield from vs. async / await.
 - New in Python 3.6:
   - asyncio API changed and labeled stable
   - PEP 525: Asynchronous Generators
   - PEP 530: Asynchronous Comprehensions
 - Event loop implementations:
   - https://docs.python.org/3/library/asyncio-eventloops.html
   - https://github.com/MagicStack/uvloop
   
    "Man that thing is complex and it keeps getting more complex. I do not have the mental capacity to casually work with asyncio."
     -- Armin Ronacher
 
