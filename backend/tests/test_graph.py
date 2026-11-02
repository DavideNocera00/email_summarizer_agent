from app.agent.graph import build_graph
from app.agent.schemas import EmailAnalysis

class FakeAnalyzer:
    def invoke(self, data):
        is_promo = "offerta" in data["subject"].lower()
        return EmailAnalysis(
            summary=f"Riassunto fittizio di: {data['subject']}",
            category="promozionale" if is_promo else "lavoro",
            requires_action=not is_promo,
        )

def test_graph_workflow():
    graph = build_graph(FakeAnalyzer())

    result = graph.invoke(
        {
            "emails": [
                {"id": 1, "sender": "fake@gmail.com", "subject": "Offerta speciale", "snippet": ""},
                {"id": 2, "sender": "real@gmail.com", "subject": "Riunione domani", "snippet": ""},
            ],
            "classified": [],
            "digest": "",
        }
    )

    assert result["classified"][0]["category"] == "promozionale"
    assert result["classified"][1]["requires_action"] is True
    assert result["digest"] == "2 email, di cui 1 richiedono un'azione."