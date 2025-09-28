import { useState } from "react";
import { Button, Form, Alert,Spinner } from "react-bootstrap";

function Query() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleQuery = async () => {
    setLoading(true);
    setAnswer("");
    try{
    const res = await fetch("http://localhost:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: question }),
    });
    const data = await res.json();
    setAnswer(data.answer || "No answer received.");
    }catch(error){
      setAnswer("Error fetching answer.");
    }
    finally{
      setLoading(false);
    }
  };

  return (
    <div>
      {loading ? ( // 🔹 added spinner overlay
        <div className="d-flex justify-content-center align-items-center p-4">
          <Spinner animation="border" role="status" className="me-2" />
          <span>Processing...</span>
        </div>
      ) : (
        <>
      <Form.Group className="mb-3">
        <Form.Control
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Type your question"
        />
      </Form.Group>
      <Button variant="success" onClick={handleQuery}>
        Ask
      </Button>
      {answer && (
        <Alert variant="info" className="mt-3">
          <strong>Answer:</strong> {answer}
        </Alert>
      )}
      </>
    )}
    </div>
  );
}

export default Query;
