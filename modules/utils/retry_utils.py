import asyncio
import logging


class RetryUtils:

    @staticmethod
    async def retry_with_backoff(
            func, max_retries: int = 3, backoff: float = 1.0, *args, **kwargs
    ):
        """
        Retry a function with exponential backoff.
        """
        for attempt in range(max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(backoff * (2 ** attempt))