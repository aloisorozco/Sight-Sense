import React, { useState } from 'react';
import axios from 'axios';
import classes from "./main_view.module.css"
import 'bootstrap/dist/css/bootstrap.min.css';

const VIDEO_URL = "http://127.0.0.1:5500"

function updateTextInput(event, setter) {
    setter(event.target.value);
}

async function checkServerStatus() {
    let res = await axios.get(VIDEO_URL + "/status")
    return res === 200
}

function SettingsScreen(props) {

    const [confidencePercentage, setConfidencePercentage] = useState(0);
    const [updateRate, setUpdateRate] = useState(0);
    const [messagePerUpdate, setMessagePerUpdate] = useState(0);
    const [hazardObjectThreshold, setHazardObjectSizeThreshold] = useState(0);

    const [start, setStart] = useState(false);
    
    const startStream = () => {
        let stat = checkServerStatus()
        setStart(true)

        props.sendData({
            stream_status: stat,
            vaide_url: VIDEO_URL,
        })
    }

    const stopStream = () => {
        
        setStart(false)

        props.sendData({
            stream_status: false,
            vaide_url: VIDEO_URL,
        })
    }

    return (
        <div className={`shadow mr-auto ${classes.settings_container}`}>

            <div className={classes.settings_selections}>
                <label id="conf" htmlFor="customRange1" className="form-label">Confidence Percentage: {confidencePercentage} </label>
                <input type="range" className="form-range" value={confidencePercentage} min="0" max="5" step="1" id="customRange1" onChange={(e) => updateTextInput(e, setConfidencePercentage)}></input>
            </div>

            <div className={classes.settings_selections}>
                <label htmlFor="customRange2" className="form-label">Update Rate (sec/update): {updateRate} </label>
                <input type="range" className="form-range" value={updateRate} min="0" max="5" step="1" id="customRange2" onChange={(e) => updateTextInput(e, setUpdateRate)}></input>
            </div>

            <div className={classes.settings_selections}>
                <label htmlFor="customRange3" className="form-label">Message Per Update: {messagePerUpdate} </label>
                <input type="range" className="form-range" value={messagePerUpdate} min="0" max="5" step="1" id="customRange3" onChange={(e) => updateTextInput(e, setMessagePerUpdate)}></input>
            </div>

            <div className={classes.settings_selections}>
                <label htmlFor="customRange4" className="form-label">Hazard Object Percentage Threshold: {hazardObjectThreshold} </label>
                <input type="range" className="form-range" value={hazardObjectThreshold} min="0" max="5" step="1" id="customRange4" onChange={(e) => updateTextInput(e, setHazardObjectSizeThreshold)}></input>
            </div>


            {start ? 
                <button onClick={stopStream} type="button" className={`btn btn-primary btn-lg ${classes.apply_btn}`}>Stop</button>:
                <button onClick={startStream} type="button" className={`btn btn-primary btn-lg ${classes.apply_btn}`}>Apply & Start</button> }

        </div>
    )
}

export default SettingsScreen