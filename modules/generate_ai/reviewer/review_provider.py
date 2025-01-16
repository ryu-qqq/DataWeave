import logging
from typing import List, Optional

from modules.generate_ai.models.code import Code
from modules.generate_ai.reviewer.java_reviwer import java_reviewer
from modules.generate_ai.reviewer.reviewer import Reviewer


class ReviewerProvider:

    def __init__(self, reviewers: List[Reviewer]):
        self.reviewers = reviewers

    def get_reviewer(self, code: Code) -> Optional[Reviewer]:
        for reviewer in self.reviewers:
            if reviewer.supports(code):
                return reviewer

        logging.warning(f"No reviewer found for code type: {code.code_type}")
        return None


reviewer_provider = ReviewerProvider(reviewers=[java_reviewer])