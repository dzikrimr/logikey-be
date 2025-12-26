from pydantic import BaseModel
from typing import List, Optional

class LogicRequest(BaseModel):
    text: str

class LogicResponse(BaseModel):
    input: str
    label: str
    explanation: Optional[str] = None
    is_fallacy: bool
    counter_arguments: List[str] = []
    status: str