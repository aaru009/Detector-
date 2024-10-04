import React, { useState } from 'react';
import VideoList from './components/VideoList';
import './App.css';  // Custom CSS for styling

function App() {
    const [videos, setVideos] = useState([]);  // Array to store processed video results
    const [query, setQuery] = useState('deepfake');  // Default search query
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const [socket, setSocket] = useState(null);  // WebSocket connection

    // Function to initiate WebSocket connection and listen for messages
    const startWebSocket = () => {
        const ws = new WebSocket(`ws://localhost:8000/ws/analyze?query=${encodeURIComponent(query)}`);
        
        ws.onopen = () => {
            console.log("WebSocket connection established.");
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setVideos(prev => [...prev, data]);  // Append new video results to state
        };

        ws.onerror = (event) => {
            console.error("WebSocket error:", event);
        };

        ws.onclose = () => {
            console.log("WebSocket connection closed.");
        };

        setSocket(ws);  // Set the WebSocket connection in state
    };

    // Function to fetch videos and start the WebSocket connection
    const fetchVideos = () => {
        setLoading(true);
        setError(null);  // Clear previous errors

        startWebSocket();  // Start WebSocket connection for real-time updates
        setLoading(false);
    };

    return (
        <div className="App">
            {/* Video Background */}
            <video autoPlay loop muted className="background-video">
                <source src="/Users/aryanpateriya/Desktop/Live Detection/frontend/public/videos/background.mp4" type="video/mp4" />
                Your browser does not support the video tag.
            </video>

            {/* Logos positioned outside the dashboard */}
            <img 
                src="https://www.newsvoir.com/images/user/logo/_cybernew.JPG" 
                alt="Logo 1" 
                className="logo left-logo" 
            />
            <img 
                src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYT5eWCFTlMppUQaUWPNAJaSBTN6-PjyR5Pg&s" 
                alt="Logo 2" 
                className="logo right-logo" 
            />

            <div className="dashboard">
                <h1>DeepFake Hunter</h1>

                <div className="query-container">
                    <input 
                        type="text" 
                        placeholder="Enter search query" 
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}  // Update query state on input change
                    />
                    <button onClick={fetchVideos}>Analyze</button>  {/* Analyze Button */}
                </div>

                {loading && <p className="loading">Analyzing videos, please wait...</p>}
                {error && <p className="error">Error: {error}</p>}
                <VideoList videos={videos} />
            </div>
        </div>
    );
}

export default App;