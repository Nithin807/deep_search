import { useState } from "react";
import { Form, Button, Alert, Spinner } from "react-bootstrap";

function Login({ onAuth }) {
  const [user_name, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    setLoading(true);
    setMessage("");
    setError("");

    try {
      const res = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_name, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || data.error || "Login failed");
      } else {
        const returnedUsername = data.username || user_name;
        const token = data.token || data.access_token || null;

        if (token) localStorage.setItem("token", token);
        if (returnedUsername) localStorage.setItem("username", returnedUsername);

        setMessage("Login successful");
        if (onAuth) onAuth({ username: returnedUsername, token });
      }
    } catch (err) {
      setError("Login failed — server not reachable");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {loading ? (
        <div className="d-flex justify-content-center align-items-center p-4">
          <Spinner animation="border" role="status" className="me-2" />
          <span>Logging in...</span>
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

          <Button variant="success" onClick={handleLogin}>
            Login
          </Button>

          {message && <Alert variant="success" className="mt-3">{message}</Alert>}
          {error && <Alert variant="danger" className="mt-3">{error}</Alert>}
        </>
      )}
    </div>
  );
}

export default Login;
