import asyncio


class CoroutineUtils:

    @staticmethod
    def run_async(coroutine):
        loop = asyncio.get_event_loop()
        if not loop.is_running():
            return loop.run_until_complete(coroutine)
        else:
            return asyncio.ensure_future(coroutine)
