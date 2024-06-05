import { useState, useEffect, useCallback } from "react";
import axios from 'axios';
import classes from "./main_view.module.css"
import 'bootstrap/dist/css/bootstrap.min.css';

function MainScreen(props) {

    const [frameURL, setFrameURL] = useState("")

    const fecthFrame = useCallback(async () =>{
        
        if(props.stream_url){
            try{
                const url = props.stream_url + "/video_feed"
                let res = await axios.get(url, {
                    responseType: 'blob'
                })
    
                const objectUrl = URL.createObjectURL(res.data);
                setFrameURL(objectUrl)
    
            }catch(err){
                console.log(err)
            }
        } 
    })

    useEffect(() => {
        fecthFrame()
        const interval = setInterval(() =>{
            fecthFrame()
        }, 500)

        return () => {
            clearInterval(interval)
        }

    }, [fecthFrame])

    return (
        <div className={`shadow mr-auto ${classes.view_container}`}>
            {props.stream_stat ?  <img src={frameURL} alt="Stream Loading..." /> : <span>Server is not on/ some issue arrised</span>}
        </div>
    )
}

export default MainScreen