from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.agent.schemas import EmailAnalysis
from app.config import settings

PROMPT = ChatPromptTemplate.from_template(
    """Analizza la seguente mail.
     
    Mittente: {sender}
    Oggetto: {subject}
    Anteprima: {snippet}

    Scrivi un riassunto conciso in italiano, scegliendo la categoria e indicando se è richiesta
    un'azione da parte del destinatario.
       """
)

def build_analyzer():
    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        api_key=settings.google_api_key,
        temperature=0,
    )
    return PROMPT | llm.with_structured_output(EmailAnalysis)
