from pydantic import BaseModel
from typing import List

class FailedFilter(BaseModel):
    filter: str
    reason: str

class HardFilterResult(BaseModel):
    passed: bool
    status: str
    failed_filters: List[FailedFilter] = []
    warnings: List[str] = []
