import React, { useState } from "react";
import { Client } from "@gradio/client";

function App() {
  const [url, setUrl] = useState("");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input || !url) return;

    const userMsg = { role: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      // Connect to the Gradio client
      const client = await Client.connect("TharaKavin/Web-Rag");
      
      // Predict using the /predict endpoint
      const result = await client.predict("/predict", {
        url: url,  // Required: The website URL (string)
        question: userMsg.text,  // Required: The question (string)
      });

      // The result.data is a string (the answer from the "🤖 Answer" Textbox)
      const answer = result.data || "No response from model";

      const botMsg = {
        role: "bot",
        text: answer,
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "❌ API error" },
      ]);
    }

    setLoading(false);
  };

  return (
    <div style={{ maxWidth: "700px", margin: "auto", padding: "20px" }}>
      <h2>🤖 Web RAG Chatbot</h2>

      {/* URL Input */}
      <input
        type="text"
        placeholder="Enter Website URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "10px",
        }}
      />

      {/* Chat Box */}
      <div
        style={{
          height: "400px",
          overflowY: "auto",
          border: "1px solid #ccc",
          padding: "10px",
          borderRadius: "10px",
          marginBottom: "10px",
          background: "#f9f9f9",
        }}
      >
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              textAlign: msg.role === "user" ? "right" : "left",
              marginBottom: "10px",
            }}
          >
            <span
              style={{
                display: "inline-block",
                padding: "10px",
                borderRadius: "15px",
                background:
                  msg.role === "user" ? "#007bff" : "#e5e5ea",
                color: msg.role === "user" ? "#fff" : "#000",
                maxWidth: "70%",
              }}
            >
              {msg.text}
            </span>
          </div>
        ))}

        {loading && (
          <div style={{ textAlign: "left" }}>
            <span>🤖 Thinking...</span>
          </div>
        )}
      </div>

      {/* Input */}
      <div style={{ display: "flex", gap: "10px" }}>
        <input
          type="text"
          placeholder="Ask something..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{ flex: 1, padding: "10px" }}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />

        <button onClick={sendMessage} style={{ padding: "10px 20px" }}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;