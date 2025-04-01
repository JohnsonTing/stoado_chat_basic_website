import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');
  const [result, setResult] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/classify', { message });
      setResult(response.data.result);
      console.log(response.data.result);
    } catch (error) {
      console.error('Error:', error);
      setResult('Error classifying message');
    }
  };

  return (
    <div className="App">
      <h1>Message Chatbox</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Enter a message"
          required
        />
        <button type="Send">Send</button>
      </form>
      <h2>Result: {result}</h2>
    </div>
  );
}

export default App;
