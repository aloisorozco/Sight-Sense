import React, { useEffect, useState } from 'react';
import axios from 'axios';
import io from 'socket.io-client';
import classes from "./main_view.module.css"
import 'bootstrap/dist/css/bootstrap.min.css';

const VIDEO_URL = "http://127.0.0.1:5500/"

function updateTextInput(event, setter) {
    setter(event.target.value);
}

async function checkServerStatus() {

    return axios.get(VIDEO_URL + "status").then((res) => {
        return res
    }).catch((err) => {
        console.log(err)
        return false
    })

}

async function endStream(socket) {

    return new Promise((resolve, reject) => {
        socket.emit('end_stream')
        socket.on('stream_exit_res', (data) => {
            resolve(data)
        })
    })

}

async function joinStream(socket) {

    return new Promise((resolve, reject) => {
        socket.emit('join_stream')
        socket.on('join_stream_confirmation', (data) => { resolve(data) })
    })
}

function SettingsScreen(props) {

    const [numUnknownPpl, setNumUnknownPpl] = useState(0);
    const [estimatedPerson, setEstimatedPerson] = useState("");

    const [personInView, setPersonInView] = useState(false);

    const [webSocket, setWebSocket] = useState(null)
    const [start, setStart] = useState(false);

    useEffect(() => {
        if (!webSocket) {
            const socket = io(VIDEO_URL)
            setWebSocket(socket)

            return () => {
                socket.disconnect()
            }
        }
    }, [])

    async function startStream() {
        let stat = await checkServerStatus()

        if (stat) {
            setStart(true)

            let res = null
            await joinStream(webSocket).then((data) => {
                res = data
            })

            if (res == 200) {

                webSocket.on("frame", (data) => {
                    console.log('frame recieved')
                    props.sendData({
                        frame: data,
                        start: true,
                    })
                })

            } else {
                console.log("Cant connect to serwer - I am going to break my monitaur I swaer")
            }
        }
    }

    async function stopStream() {
        let end = await endStream(webSocket)

        if (end == 200) {
            setStart(false)
            props.sendData({
                frame: null,
                start: false,
            })
        } else {
            console.log("Issue disconnecting from the stream - ch-ch-chat is this real??")
        }
    }

    return (
        <div className={`shadow mr-auto ${classes.settings_container}`}>

            <div className={classes.settings_selections}>
                <label id="conf" htmlFor="customRange1" className="form-label"># Unknown People detected: {numUnknownPpl} </label>
            </div>

            <div className={classes.settings_selections}>
                <label htmlFor="customRange2" className="form-label">Estimated Person: {estimatedPerson} </label>
            </div>


            <div className={`${classes.main_btn_container}`}>
                <button onClick={startStream} type="button" className={`btn btn-success btn-lg`} disabled={!personInView}>Authenticate</button>

                {start ?
                    <button onClick={stopStream} type="button" className={`btn btn-primary btn-lg ${classes.main_btn}`}>Stop</button> :
                    <button onClick={startStream} type="button" className={`btn btn-primary btn-lg ${classes.main_btn}`}>Apply & Start</button>}

            </div>

        </div>
    )
}

export default SettingsScreen