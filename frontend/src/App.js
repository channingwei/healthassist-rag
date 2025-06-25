import { useState, useEffect } from "react";
import "./App.css";

// Get API URL from environment variable or default to localhost
const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5001";

function App() {
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [healthTips, setHealthTips] = useState([]);
  const [showTips, setShowTips] = useState(false);

  useEffect(() => {
    // Load health tips on component mount
    fetchHealthTips();
  }, []);

  const fetchHealthTips = async () => {
    try {
      const response = await fetch(`${API_URL}/health-tips`);
      const data = await response.json();
      if (data.tips) {
        setHealthTips(data.tips);
      }
    } catch (error) {
      console.error("Failed to fetch health tips:", error);
    }
  };

  const askBot = async () => {
    if (!question.trim() || loading) return;

    setLoading(true);
    const userQuestion = question;

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userQuestion }),
      });

      const data = await response.json();
      
      if (data.error) {
        setMessages([
          ...messages,
          { role: "user", text: userQuestion },
          { role: "bot", text: `Error: ${data.error}`, isError: true },
        ]);
      } else {
        setMessages([
          ...messages,
          { role: "user", text: userQuestion },
          { 
            role: "bot", 
            text: data.answer, 
            sources: data.sources || [],
            timestamp: new Date().toLocaleTimeString()
          },
        ]);
      }
    } catch (error) {
      setMessages([
        ...messages,
        { role: "user", text: userQuestion },
        { 
          role: "bot", 
          text: "Sorry, I'm having trouble connecting to the server. Please try again later.", 
          isError: true 
        },
      ]);
    } finally {
      setLoading(false);
      setQuestion("");
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      askBot();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🏥 HealthAssist</h1>
        <p>Your AI-powered health information assistant</p>
      </header>

      <div className="main-container">
        <div className="sidebar">
          <div className="health-tips-section">
            <h3>💡 Health Tips</h3>
            <button 
              className="tips-toggle"
              onClick={() => setShowTips(!showTips)}
            >
              {showTips ? "Hide Tips" : "Show Tips"}
            </button>
            
            {showTips && (
              <div className="tips-list">
                {healthTips.slice(0, 8).map((tip, index) => (
                  <div key={index} className="tip-item">
                    {tip}
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="quick-actions">
            <h3>Quick Questions</h3>
            <button 
              onClick={() => setQuestion("How much water should I drink daily?")}
              className="quick-question"
            >
              💧 Daily Water Intake
            </button>
            <button 
              onClick={() => setQuestion("How much exercise do I need?")}
              className="quick-question"
            >
              🏃‍♂️ Exercise Guidelines
            </button>
            <button 
              onClick={() => setQuestion("How to improve sleep quality?")}
              className="quick-question"
            >
              😴 Sleep Tips
            </button>
            <button 
              onClick={() => setQuestion("When should I see a doctor?")}
              className="quick-question"
            >
              🚨 When to Seek Care
            </button>
          </div>
        </div>

        <div className="chat-container">
          <div className="chat-header">
            <h2>Chat with HealthAssist</h2>
            <button onClick={clearChat} className="clear-chat">
              Clear Chat
            </button>
          </div>

          <div className="chat-window">
            {messages.length === 0 && (
              <div className="welcome-message">
                <h3>Welcome to HealthAssist! 👋</h3>
                <p>Ask me any health-related questions, and I'll provide you with evidence-based information.</p>
                <p><strong>Remember:</strong> This is for informational purposes only. Always consult healthcare professionals for medical advice.</p>
              </div>
            )}
            
            {messages.map((msg, i) => (
              <div key={i} className={`message ${msg.role} ${msg.isError ? 'error' : ''}`}>
                <div className="message-header">
                  <strong>{msg.role === "user" ? "You" : "HealthAssist"}</strong>
                  {msg.timestamp && <span className="timestamp">{msg.timestamp}</span>}
                </div>
                <div className="message-content">
                  {msg.text}
                </div>
                {msg.sources && msg.sources.length > 0 && (
                  <div className="sources">
                    <small>Sources: {msg.sources.join(", ")}</small>
                  </div>
                )}
              </div>
            ))}
            
            {loading && (
              <div className="message bot loading">
                <div className="message-header">
                  <strong>HealthAssist</strong>
                </div>
                <div className="message-content">
                  <div className="loading-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="input-container">
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a healthcare question... (Press Enter to send)"
              disabled={loading}
              rows="2"
            />
            <button 
              onClick={askBot} 
              disabled={loading || !question.trim()}
              className="send-button"
            >
              {loading ? "Sending..." : "Send"}
            </button>
          </div>
        </div>
      </div>

      <footer className="app-footer">
        <p>
          ⚠️ <strong>Medical Disclaimer:</strong> This information is for educational purposes only. 
          Always consult with qualified healthcare professionals for medical advice, diagnosis, or treatment.
        </p>
      </footer>
    </div>
  );
}

export default App;
