import { useState } from "react";
import { Button, Form, Alert,Spinner } from "react-bootstrap";

function Upload() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setMessage(data.message || "File uploaded!");
    setLoading(false);
  };

  return (
    <div>
      {loading ? (<div className="d-flex justify-content-center align-items-center p-4">
          <Spinner animation="border" role="status" className="me-2" />
          <span>Uploading...</span>
        </div>):(<>
      <Form.Group controlId="formFile" className="mb-3">
        <Form.Control
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
        />
      </Form.Group>
      <Button variant="primary" onClick={handleUpload}>
        Upload
      </Button>
      {message && <Alert variant="success" className="mt-3">{message}</Alert>}
      </>)}
    </div>
  );
}

export default Upload;
