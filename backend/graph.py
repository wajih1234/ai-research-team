from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from planner import plan
from researcher import research 
from critic import critique
from writer import write_report

class State(TypedDict):
    topic: str
    questions: list[str]
    findings: list[dict]
    reviews: list[str]
    report : str


def planner_node(state: State):
    text = plan(state["topic"])
    questions = [q.strip() for q in text.split("\n") if q.strip()]
    return {"questions": questions}
def researcher_node(state: State):
    findings = [research(q) for q in state["questions"]]
    return {"findings": findings}

def critic_node(state: State):
    reviews = [critique(f) for f in state["findings"]]
    return {"reviews": reviews}
def writer_node(state: State):
    report = write_report(state["topic"], state["findings"])
    return {"report": report}



builder = StateGraph(State)
builder.add_node("planner", planner_node)
builder.add_node("researcher", researcher_node)
builder.add_node("critic", critic_node)
builder.add_node("writer", writer_node)
builder.add_edge(START, "planner")
builder.add_edge("planner", "researcher")
builder.add_edge("researcher", "critic")
builder.add_edge("critic", "writer")
builder.add_edge("writer", END)
graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke({"topic": "electric cars in Tunisia"})
    print(result["report"])