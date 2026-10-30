from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from fastapi.responses import StreamingResponse
from graph import graph

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/research")
def run_research(topic: str):
    result = graph.invoke({"topic": topic})
    return {"report": result["report"]}

@app.get("/stream")
def stream_research(topic: str):
    def events():
        for step in graph.stream({"topic": topic}, stream_mode="updates"):
            for node, update in step.items():
                yield f"data: {json.dumps({'agent': node, 'update': update})}\n\n"
        yield 'data: {"agent": "done"}\n\n'
    return StreamingResponse(events(), media_type="text/event-stream")