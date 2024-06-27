import '../App.css';
import React, { useState } from 'react';
import MainScreen from './video_view';
import SettingsScreen from './settings'
import NavBar from './nav_bar'

function ContentContainer(){

    const [frame, setFrame] = useState()
    const [isStreaming, setIsStreaming] = useState()

    const handleButtonPress = (data) =>{
        setFrame(data.frame)
        setIsStreaming(data.start)
    }
    
    return(
        <div className="App-views-container">
            <MainScreen frame={frame} start={isStreaming}/>
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