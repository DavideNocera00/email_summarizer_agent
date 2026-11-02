from typing import Literal
from pydantic import BaseModel

class EmailAnalysis(BaseModel):
    summary: str
    category: Literal["lavoro", "personale", "promozionale", "notifica"]
    requires_action: bool