import { useState, useEffect } from "react";
import { Form, Button, Spinner } from "react-bootstrap";
import { v4 as uuidv4 } from "uuid";

function Chat() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(uuidv4());
  const [chatHistory, setChatHistory] = useState([]);
  const [sessions, setSessions] = useState([]);

  const userName = localStorage.getItem("username");

  // Fetch sessions when component loads
  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const res = await fetch(`http://localhost:8000/sessions/${userName}`);
        const data = await res.json();
        setSessions(data.sessions || []);
      } catch (err) {
        console.error("Failed to fetch sessions", err);
      }
    };
    if (userName) fetchSessions();
  }, [userName]);

  const fetchHistory = async (sid) => {
    try {
      const res = await fetch(`http://localhost:8000/messages/${userName}/${sid}`);
      const data = await res.json();
      setChatHistory(data.messages || []);
    } catch (err) {
      console.error("Failed to fetch history", err);
      setChatHistory([]);
    }
  };

  const handleChat = async () => {
    if (!message.trim()) return;
    setLoading(true);

    setChatHistory((prev) => [...prev, { role: "user", content: message }]);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_name: userName,
          session_id: sessionId,
          message: message,
        }),
      });

      const data = await res.json();
      const assistantReply = data.answer || "No response";

      setChatHistory((prev) => [
        ...prev,
        { role: "assistant", content: assistantReply },
      ]);
    } catch (err) {
      setChatHistory((prev) => [
        ...prev,
        { role: "assistant", content: "Chat failed. Try again." },
      ]);
    } finally {
      setLoading(false);
      setMessage("");
    }
  };

  const handleNewChat = () => {
    const newSession = uuidv4();
    setSessionId(newSession);
    setChatHistory([]);
    setMessage("");
    setSessions((prev) => [...prev, newSession]);
  };

  const handleSessionChange = (sid) => {
    setSessionId(sid);
    fetchHistory(sid); // 🔹 fetch history when selecting old session
  };

  return (
    <div>
      {/* Session dropdown + New Chat */}
      <div className="d-flex justify-content-between align-items-center mb-3">
        <Form.Select
          value={sessionId}
          onChange={(e) => handleSessionChange(e.target.value)}
          style={{ width: "70%" }}
        >
          {sessions.map((s) => (
            <option key={s} value={s}>
              {s.slice(0, 8)}...
            </option>
          ))}
          {!sessions.includes(sessionId) && (
            <option value={sessionId}>{sessionId.slice(0, 8)}...</option>
          )}
        </Form.Select>

        <Button variant="secondary" size="sm" onClick={handleNewChat}>
          New Chat
        </Button>
      </div>

      {/* Chat history box */}
      <div
        className="border rounded p-3 mb-3"
        style={{ minHeight: "200px", maxHeight: "300px", overflowY: "auto" }}
      >
        {chatHistory.length === 0 && (
          <p className="text-muted">No messages yet. Start the conversation!</p>
        )}
        {chatHistory.map((msg, idx) => (
          <div
            key={idx}
            className={`mb-2 p-2 rounded ${
              msg.role === "user"
                ? "bg-primary text-white text-end"
                : "bg-light text-dark text-start"
            }`}
          >
            <strong>{msg.role === "user" ? "You" : "Assistant"}:</strong>{" "}
            {msg.content}
          </div>
        ))}
      </div>

      {/* Input + send */}
      {loading ? (
        <div className="d-flex justify-content-center align-items-center p-3">
          <Spinner animation="border" role="status" className="me-2" />
          <span>Thinking...</span>
        </div>
      ) : (
        <div className="d-flex">
          <Form.Control
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type a message..."
            className="me-2"
          />
          <Button variant="primary" onClick={handleChat}>
            Send
          </Button>
        </div>
      )}
    </div>
  );
}

export default Chat;
