import { useState } from "react";

function App() {
  const [topic, setTopic] = useState("");
  const [events, setEvents] = useState([]);
  const [report, setReport] = useState("");
  const start = () => {
    setEvents([]);
    setReport("");
    const source = new EventSource(
      `http://127.0.0.1:8000/stream?topic=${encodeURIComponent(topic)}`
    );
    source.onmessage = (e) => {
      const data = JSON.parse(e.data);
      if (data.agent === "writer") setReport(data.update.report);
      if (data.agent === "done") source.close();
      setEvents((prev) => [...prev, data.agent]);
    };
    source.onerror = () => source.close();
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
      <ul>
        {events.map((agent, i) => (
          <li key={i}>{agent} finished</li>
        ))}
      </ul>
      <pre style={{ whiteSpace: "pre-wrap", textAlign: "left" }}>{report}</pre>
    </div>
  );
}

export default App;