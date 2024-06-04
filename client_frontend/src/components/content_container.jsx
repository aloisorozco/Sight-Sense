import '../App.css';
import React, { useState } from 'react';
import MainScreen from './video_view';
import SettingsScreen from './settings'
import NavBar from './nav_bar'

function ContentContainer(){

    const [streamOk, setStreamOk] = useState(false)
    const [videoURL, setVideoURL] = useState("")

    const handleButtonPress = (data) =>{
        setStreamOk(data.stream_status)
        setVideoURL(data.vaide_url)
    }
    
    return(
        <div className="App-views-container">
            <MainScreen stream_stat={streamOk} url={videoURL} />
            <SettingsScreen sendData={handleButtonPress}/>
        </div>
    )
}

function AppContainer(){
    return(
        <div className="App-content-container">
            <NavBar />
            <ContentContainer />
        </div>
    )
}

export default AppContainer