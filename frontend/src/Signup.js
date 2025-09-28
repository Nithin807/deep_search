// src/Signup.js
import { useState } from "react";
import { Form, Button, Alert, Spinner } from "react-bootstrap";

function Signup({ onAuth }) {
  const [user_name, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false); // spinner state
  const [message, setMessage] = useState("");    // success/info
  const [error, setError] = useState("");        // error messages

  const handleSignup = async () => {
    setLoading(true);
    setMessage("");
    setError("");

    try {
      const res = await fetch("http://localhost:8000/signup", { // adjust URL if backend differs
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_name, password }), // send username/password as JSON
      });

      const data = await res.json();

      if (!res.ok) {
        // Backend returned an error (422 / 400 / 500...). Show helpful text if present.
        setError(data.detail || data.error || data.message || "Signup failed");
      } else {
        // Successful signup
        const returnedUsername = data.user_name || data.user || data.name || user_name; // tolerant extraction
        const token = data.token || data.access_token || null; // sometimes backend returns token

        if (token) {
          localStorage.setItem("token", token); // 🔹 persist token so we can use it for auth
        }
        if (returnedUsername) {
          localStorage.setItem("username", returnedUsername); // 🔹 persist username
        }

        setMessage(data.message || "Signup successful");

        // Notify parent (App) that auth changed so it can update UI
        if (onAuth) onAuth({ username: returnedUsername, token }); // 🔹 callback to parent
      }
    } catch (err) {
      setError("Signup failed — could not connect to server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {loading ? ( // show full-card spinner while the request is in-flight
        <div className="d-flex justify-content-center align-items-center p-4">
          <Spinner animation="border" role="status" className="me-2" />
          <span>Creating account...</span>
        </div>
      ) : (
        <>
          <Form.Group className="mb-3">
            <Form.Label>Username</Form.Label>
            <Form.Control
              value={user_name}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Password</Form.Label>
            <Form.Control
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
            />
          </Form.Group>

          <Button variant="primary" onClick={handleSignup}>
            Sign up
          </Button>

          {message && <Alert variant="success" className="mt-3">{message}</Alert>}
          {error && <Alert variant="danger" className="mt-3">{error}</Alert>}
        </>
      )}
    </div>
  );
}

export default Signup;
