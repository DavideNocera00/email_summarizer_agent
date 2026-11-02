from langgraph.graph import StateGraph, START, END
from app.agent.state import AgentState

def classify(state: AgentState) -> dict:
    classified = []
    for email in state['emails']:
        is_promo = "offerta" in email['subject'].lower()
        classified.append(
            {**email, "category": "promozionale" if is_promo else "altro"}
        )
    return {"classified": classified}

def build_digest(state: AgentState) -> dict:
    promo = sum(1 for e in state['classified'] if e['category'] == 'promozionale')
    total = len(state['classified'])
    return {"digest": f"{total} email, di cui {promo} promozionali."}

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("classify", classify)
    graph.add_node("build_digest", build_digest)
    graph.add_edge(START, "classify")
    graph.add_edge("classify", "build_digest")
    graph.add_edge("build_digest", END)
    return graph.compile()