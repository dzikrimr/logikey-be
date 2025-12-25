from pydantic import BaseModel
from typing import List, Optional

class LogicRequest(BaseModel):
    text: str

class LogicResponse(BaseModel):
    fallacy: Optional[str] = None
    suggestion: Optional[str] = None
    explanation: Optional[str] = None
    counter_arguments: List[str] = []
    status: str