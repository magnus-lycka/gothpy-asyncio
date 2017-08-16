import asyncio


def bark(loop):
    print('Woof!!!')
    loop.stop()


async def might_time_out(loop, timeout=3):
    delay = 1
    while 1:
        watchdog = loop.call_later(timeout, bark, loop)
        await asyncio.sleep(delay)
        watchdog.cancel()
        print('Slept', delay, 'seconds')
        delay *= 2


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(might_time_out(loop))
    print('Done!')
    loop.close()
