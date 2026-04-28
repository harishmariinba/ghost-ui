import axios from "axios";
import { useState } from "react";

function App() {
  const [response, setResponse] = useState("");
  const [listening, setListening] = useState(false);

  const startListening = () => {
    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = "en-US";

    setListening(true);

    recognition.onresult = async (event) => {
      const text = event.results[0][0].transcript;
      console.log("You said:", text);

      try {
        const res = await axios.post("http://127.0.0.1:8001/command", {
          text: text,
        });

        setResponse(res.data.response);
      } catch (err) {
        console.error("Backend error:", err);
        setResponse("Error connecting to backend");
      }

      setListening(false);
    };

    recognition.onerror = () => {
      setListening(false);
      setResponse("Mic error");
    };

    recognition.start();
  };

  return (
    <div
      style={{
        textAlign: "center",
        marginTop: "100px",
        fontFamily: "Arial",
      }}
    >
      <h1>GHOST UI</h1>

      <button
        onClick={startListening}
        style={{
          fontSize: "30px",
          padding: "25px",
          borderRadius: "50%",
          cursor: "pointer",
          backgroundColor: listening ? "#ff4d4d" : "#333",
          color: "white",
          border: "none",
        }}
      >
        🎙️
      </button>

      <p style={{ marginTop: "20px", fontSize: "18px" }}>
        {listening ? "Listening..." : 'Click the mic to speak a command!'}
      </p>

      <h3 style={{ marginTop: "30px" }}>{response}</h3>
    </div>
  );
}

export default App;