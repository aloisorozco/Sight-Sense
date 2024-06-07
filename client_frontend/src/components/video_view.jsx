import { useState, useEffect } from "react";
import socketIOClient from 'socket.io-client';
// import axios from 'axios';
import classes from "./main_view.module.css"
import 'bootstrap/dist/css/bootstrap.min.css';

const ENDPOINT = "http://127.0.0.1:5500"

function MainScreen(props) {

    const [frame, setFrame] = useState(null);

    useEffect(() => {
        const socket = socketIOClient(ENDPOINT);

        socket.on("connect", (data) => {
            console.log(data);
          });

        socket.on('frame', (data) => {
            setFrame(data)
        });

        return () => {
            socket.disconnect();
        };
    }, []);
    

    return (
        <div className={`shadow mr-auto ${classes.view_container}`}>
            {props.stream_stat ? <img src={`data:image/jpeg;base64,${frame}`} alt="Stream Loading..." /> : <span>Server is not on/ some issue arrised</span>}
        </div>
    )
}

export default MainScreen