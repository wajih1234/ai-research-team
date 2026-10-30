import { useState } from "react";
import ReactMarkdown from "react-markdown";
const AGENTS = ["planner", "researcher", "critic", "writer"];
function App() {
  const [topic, setTopic] = useState("");
  const [events, setEvents] = useState([]);
  const [report, setReport] = useState("");
  const [running, setRunning] = useState(false);
  const [questions, setQuestions] = useState([]);
  const start = () => {
    setEvents([]);
    setReport("");
    setRunning(true);
    setQuestions([]);
    const source = new EventSource(
      `http://127.0.0.1:8000/stream?topic=${encodeURIComponent(topic)}`
    );
    source.onmessage = (e) => {
      const data = JSON.parse(e.data);
      if (data.agent === "planner") setQuestions(data.update.questions);
      if (data.agent === "writer") setReport(data.update.report);
      if (data.agent === "done") { source.close(); setRunning(false); };
      setEvents((prev) => [...prev, data.agent]);
    };
    source.onerror = () => { source.close(); setRunning(false); };
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>AI Research Team</h1>
      <input
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder="Enter a topic"
      />
      <button onClick={start}>Start</button>
      <div style={{ display: "flex", gap: 10, justifyContent: "center", margin: "20px 0" }}>
        {AGENTS.map((a) => {
          const current = AGENTS.find((x) => !events.includes(x));
          const status = events.includes(a)
            ? "✅ done"
            : running && a === current
            ? "⏳ working..."
            : "💤 waiting";
          return (
            <div key={a} style={{ border: "1px solid #ccc", borderRadius: 8, padding: 12, minWidth: 120 }}>
              <b>{a}</b>
              <div>{status}</div>
            </div>
          );
        })}
      </div>
            {questions.length > 0 && (
        <div style={{ textAlign: "left" }}>
          <h3>Research questions</h3>
          <ol>
            {questions.map((q, i) => (
              <li key={i}>{q}</li>
            ))}
          </ol>
        </div>
      )}
           <div style={{ textAlign: "left" }}>
        <ReactMarkdown>{report}</ReactMarkdown>
      </div>
    </div>
  );
}

export default App;