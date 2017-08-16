import asyncio


def bark():
    print('Woof!!!')
    FUTURE.cancel()


async def might_time_out(loop, timeout=3):
    delay = 1
    while 1:
        watchdog = loop.call_later(timeout, bark)
        await asyncio.sleep(delay)
        watchdog.cancel()
        print('Slept', delay, 'seconds')
        delay *= 2


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    global FUTURE
    FUTURE = asyncio.ensure_future(might_time_out(loop))
    loop.run_until_complete(FUTURE)
    print('Done!')
    loop.close()
