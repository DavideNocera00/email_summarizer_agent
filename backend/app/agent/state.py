from typing import TypedDict

class EmailItem(TypedDict):
    id: str
    subject: str
    sender: str
    snippet: str

class AgentState(TypedDict):
    emails: list[EmailItem]
    classified: list[dict]
    digest: str