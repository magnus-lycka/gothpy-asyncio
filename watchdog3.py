import asyncio


def bark(task):
    print('Woof!!!')
    task = asyncio.Task.current_task()
    task.cancel()


async def might_time_out(loop, timeout=3):
    delay = 1
    task = asyncio.Task.current_task()
    while 1:
        watchdog = loop.call_later(timeout, bark, task)
        try:
            await asyncio.sleep(delay)
            watchdog.cancel()
            print('Slept', delay, 'seconds')
        except asyncio.CancelledError:
            print('Ouch...')
            return
        delay *= 2


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(might_time_out(loop))
    print('Done!')
    loop.close()
