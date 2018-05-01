import aiohttp
import asyncio

async def fetch(session, url):
    with aiohttp.Timeout(10, loop=session.loop):
        async with session.get(url) as response:
            return await response.text()

URLs = ['http://python.org', 'http://www.youtube.com', 'http://svt.se', 'http://travis-ci.org', 'http://google.com',
        'http://github.com', 'http://www.kickstarter.com', 'http://www.meetup.com', 'http://gp.se', 'http://dn.se']

async def main(loop, url):
    async with aiohttp.ClientSession(loop=loop) as session:
        html = await fetch(session, url)
        print(url, len(html))
        return url

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    t0 = loop.time()
    whole_bunch = asyncio.wait([main(loop, u) for u in URLs])
    loop.run_until_complete(whole_bunch)
    t1 = loop.time()
    print(list(whole_bunch))
    print(t1 - t0)
