from typing import TypedDict

class EmailItem(TypedDict):
    id: str
    subject: str
    sender: str
    snippet: str

class ClassifiedEmail(EmailItem):
    category: str
    summary: str
    requires_action: bool

class AgentState(TypedDict):
    emails: list[EmailItem]
    classified: list[ClassifiedEmail]
    digest: str