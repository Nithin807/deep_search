import { useState } from "react";
import { Container, Card, Button } from "react-bootstrap";
import Upload from "./Upload";
import Query from "./Query";
import Signup from "./Signup";
import Login from "./Login";
import Chat from "./Chat";

function App() {
  // check if user is stored in localStorage
  const [user, setUser] = useState(localStorage.getItem("username") || null);

  const handleAuth = ({ username }) => {
    setUser(username || null);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    setUser(null);
  };

  return (
    <Container className="py-5">
      <h1 className="text-center mb-5 text-primary">RAG Tool UI</h1>

      {user ? (
        <>
          {/* Welcome + Logout */}
          <Card className="p-4 mb-4 shadow-sm">
            <h2 className="mb-3">Welcome, {user}</h2>
            <Button variant="outline-danger" onClick={handleLogout}>
              Logout
            </Button>
          </Card>

          {/* Upload feature */}
          <Card className="p-4 mb-4 shadow-sm">
            <h2 className="mb-3">Upload Document</h2>
            <Upload />
          </Card>

          {/* Query feature */}
          {/* <Card className="p-4 shadow-sm"> */}
            {/* <h2 className="mb-3">Ask a Question</h2> */}
            {/* <Query /> */}
          {/* </Card> */}

          {/* Chat feature */}
          <Card className="p-4 mt-4 shadow-sm">
            <h2 className="mb-3">Chat with AI</h2>
            <Chat />
          </Card>
        </>
      ) : (
        <>
          {/* Signup form */}
          <Card className="p-4 mb-4 shadow-sm">
            <h2 className="mb-3">Sign up</h2>
            <Signup onAuth={handleAuth} />
          </Card>

          {/* Login form */}
          <Card className="p-4 shadow-sm">
            <h2 className="mb-3">Login</h2>
            <Login onAuth={handleAuth} />
          </Card>
        </>
      )}
    </Container>
  );
}

export default App;

