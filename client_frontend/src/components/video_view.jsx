import { useState, useEffect } from "react";
// import axios from 'axios';
import classes from "./main_view.module.css"
import 'bootstrap/dist/css/bootstrap.min.css';

function MainScreen(props) {

    const [frame, setFrame] = useState();

    useEffect(() =>{

        if(props.frame && props.start){
            setFrame(props.frame)
        }
    
    }, [props.frame])


    return (
        <div className={`shadow mr-auto ${classes.view_container}`}>
            {props.start ? <img src={`data:image/jpeg;base64,${frame}`} alt="Stream Loading..." /> : <span>Server is not on/ some issue arrised</span>}
        </div>
    )
}

export default MainScreen