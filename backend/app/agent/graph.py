from langgraph.graph import StateGraph, START, END
from app.agent.state import AgentState

def make_classify(analyzer):
    def classify(state: AgentState) -> dict:
        results = []
        for email in state["emails"]:
            analysis = analyzer.invoke(
                {
                    "sender": email["sender"],
                    "subject": email["subject"],
                    "snippet": email["snippet"],
                }
            )
            results.append({**email, **analysis.model_dump()})
        return {"classified": results}

    return classify

def build_digest(state: AgentState) -> dict:
    total = len(state['classified'])
    to_act = sum(1 for e in state['classified'] if e['requires_action'])
    return {"digest": f"{total} email, di cui {to_act} richiedono un'azione."}

def build_graph(analyzer):
    graph = StateGraph(AgentState)
    graph.add_node("classify", make_classify(analyzer))
    graph.add_node("build_digest", build_digest)
    graph.add_edge(START, "classify")
    graph.add_edge("classify", "build_digest")
    graph.add_edge("build_digest", END)
    return graph.compile()