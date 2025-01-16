import logging
from typing import List, Optional

from modules.generate_ai.models.code import Code
from modules.generate_ai.tester.java_tester import java_tester
from modules.generate_ai.tester.tester import Tester


class TesterProvider:

    def __init__(self, testers: List[Tester]):
        self.testers = testers

    def get_reviewer(self, code: Code) -> Optional[Tester]:
        for tester in self.testers:
            if tester.supports(code):
                return tester

        logging.warning(f"No reviewer found for code type: {code.code_type}")
        return None


tester_provider = TesterProvider(testers=[java_tester])
