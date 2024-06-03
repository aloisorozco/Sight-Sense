import React, { useState, useEffect } from 'react';
import axios from 'axios'; //Could be usefull to use axios for future API calls - so keep the import and comment as a reminder
import './App.css';

import NavBar from './components/nav_bar'
import ContentContainer from './components/content_container';

function App() {

  return (
    <div className="App">
      <NavBar />
      <ContentContainer/>
    </div>
  );
}

export default App;
