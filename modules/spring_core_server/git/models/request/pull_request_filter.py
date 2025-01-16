from typing import Optional, Dict
from pydantic import BaseModel

from modules.spring_core_server.git.models.git_enums import GitType, MergeStatus, ReviewStatus
from modules.spring_core_server.models.spring_enums import Sort
from modules.spring_core_server.spring_utils import StringUtils


class PullRequestFilterDto(BaseModel):
    git_type: GitType
    status: Optional[MergeStatus]
    review_status: Optional[ReviewStatus]
    page_size: Optional[int]
    page_number: Optional[int]
    cursor_id: Optional[int]
    sort: Optional[Sort]

    def to_query_params(self) -> Dict[str, str]:
        """
        Converts the DTO to a dictionary for query parameters, excluding None values.
        """
        params = self.dict(exclude_none=True)
        return StringUtils.convert_to_camel_case(params)
