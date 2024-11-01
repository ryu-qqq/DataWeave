import requests

from dataweave.session_manager import SessionManager


class SyncSessionManager(SessionManager):
    def __init__(self):
        self.session = None

    def create_session(self):
        if not self.session:
            self.session = requests.Session()
        return self.session

    def close_session(self):
        if self.session:
            self.session.close()
            self.session = None
