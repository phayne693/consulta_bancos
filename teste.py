import asyncio
import concurrent.futures
from twocaptcha import TwoCaptcha

async def captchaSolver(api_key, sitekey_v2, url):
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, lambda: TwoCaptcha(api_key).normal(sitekey_v2, url))
        return result

if __name__ == "__main__":
    asyncio.run(captchaSolver())