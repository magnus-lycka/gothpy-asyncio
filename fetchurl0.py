import aiohttp
import asyncio

async def fetch(session, url):
    with aiohttp.Timeout(10, loop=session.loop):
        async with session.get(url) as response:
            return await response.text()

async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        url = 'http://python.org'
        html = await fetch(session, url)
        print(url, len(html))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    t0 = loop.time()
    loop.run_until_complete(main(loop))
    t1 = loop.time()
    print(t1 - t0)
