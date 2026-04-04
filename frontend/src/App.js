import React, { useState } from "react";
import axios from "axios";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

function App() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("planner");

  const generate = async () => {
    if (!prompt) return;

    setLoading(true);
    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/generate",
        null,
        { params: { prompt } }
      );
      setResult(res.data);
      setActiveTab("planner");
    } catch (err) {
      console.error(err);
      alert("Error connecting to backend");
    }
    setLoading(false);
  };

  const tabs = [
    "planner",
    "developer",
    "reviewer",
    "tester",
    "debugger"
  ];

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>🤖 AI Engineer Agent</h1>

      {/* INPUT */}
      <div style={styles.inputContainer}>
        <input
          style={styles.input}
          placeholder="Describe what you want to build..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />

        <button style={styles.button} onClick={generate}>
          Generate
        </button>
      </div>

      {loading && <p>⏳ Generating...</p>}

      {result && (
        <>
          {/* SUMMARY */}
          <div style={styles.summary}>
            <h3>✅ {result.summary.task}</h3>
            <p>Status: {result.summary.status}</p>
          </div>

          {/* TABS */}
          <div style={styles.tabs}>
            {tabs.map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                style={{
                  ...styles.tab,
                  background:
                    activeTab === tab ? "#22c55e" : "#1e293b"
                }}
              >
                {tab.toUpperCase()}
              </button>
            ))}
          </div>

          {/* CONTENT */}
          <div style={styles.content}>
            {activeTab !== "debugger" ? (
              <pre style={styles.text}>
                {result.agents[activeTab]}
              </pre>
            ) : (
              <SyntaxHighlighter
                language="python"
                style={oneDark}
                customStyle={{ borderRadius: "10px" }}
              >
                {result.agents.debugger}
              </SyntaxHighlighter>
            )}
          </div>

          {/* EXECUTION */}
          <div style={styles.execution}>
            <h3>⚙️ Execution</h3>
            <p><b>Type:</b> {result.execution.type}</p>
            <p><b>Status:</b> {result.execution.status}</p>
            <p><b>Message:</b> {result.execution.message}</p>
            <p><b>Error:</b> {result.execution.error || "None"}</p>
          </div>
        </>
      )}
    </div>
  );
}

const styles = {
  container: {
    background: "#020617",
    minHeight: "100vh",
    color: "white",
    padding: "40px",
    fontFamily: "sans-serif"
  },
  title: {
    marginBottom: "20px"
  },
  inputContainer: {
    display: "flex",
    gap: "10px",
    marginBottom: "20px"
  },
  input: {
    flex: 1,
    padding: "12px",
    borderRadius: "8px",
    border: "none"
  },
  button: {
    padding: "12px 20px",
    borderRadius: "8px",
    border: "none",
    background: "#22c55e",
    color: "white",
    cursor: "pointer"
  },
  summary: {
    background: "#1e293b",
    padding: "15px",
    borderRadius: "10px",
    marginBottom: "20px"
  },
  tabs: {
    display: "flex",
    gap: "10px",
    marginBottom: "10px"
  },
  tab: {
    padding: "10px",
    borderRadius: "8px",
    border: "none",
    color: "white",
    cursor: "pointer"
  },
  content: {
    background: "#0f172a",
    padding: "15px",
    borderRadius: "10px",
    minHeight: "200px"
  },
  text: {
    whiteSpace: "pre-wrap"
  },
  execution: {
    marginTop: "20px",
    background: "#1e293b",
    padding: "15px",
    borderRadius: "10px"
  }
};

export default App;