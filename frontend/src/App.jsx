import { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");

  const askAI = async (e) => {
    e.preventDefault();
    const res = await fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    const data = await res.json();
    setAnswer(data.answer);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>AskAI 2025</h1>
      <form onSubmit={askAI}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question..."
          style={{ width: "300px" }}
        />
        <button type="submit">Ask</button>
      </form>
      {answer && (
        <div style={{ marginTop: "1rem" }}>
          <h3>Answer:</h3>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}

export default App;
