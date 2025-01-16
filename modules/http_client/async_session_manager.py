import aiohttp

from modules.http_client.session_manager import SessionManager


class AsyncSessionManager(SessionManager):
    def __init__(self):
        self.session = None

    async def create_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close_session(self):
        if self.session:
            await self.session.close()
            self.session = None
