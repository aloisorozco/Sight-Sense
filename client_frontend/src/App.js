import React, { useState, useEffect } from 'react';
import axios from 'axios'; //Could be usefull to use axios for future API calls - so keep the import and comment as a reminder
import './App.css';

function App() {
  const [frameSrc, setFrameSrc] = useState('');

  const vide_url = "http://127.0.0.1:5500/video_feed"

  return (
    <div className="App">
      <header className="App-header">
        <h1>Video Stream</h1>
        <img src={vide_url} alt="stream" />
      </header>
    </div>
  );
}

export default App;
