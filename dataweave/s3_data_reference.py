from typing import List


class S3DataReference:
    def __init__(self, s3_url: str, keys: List[str]):
        self.s3_url = s3_url
        self.keys = keys

    def __repr__(self):
        return f"S3DataReference(s3_url={self.s3_url}, keys={self.keys})"
