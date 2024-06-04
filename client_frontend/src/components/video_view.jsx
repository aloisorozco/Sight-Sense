import classes from "./main_view.module.css"
import 'bootstrap/dist/css/bootstrap.min.css';

function MainScreen(props) {

    return (
        <div className={`shadow mr-auto ${classes.view_container}`}>
            {props.stream_stat ?  <img src={props.url + "/video_feed"} alt="Stream Loading..." /> : <span>Server is not on/ some issue arrised</span>}
        </div>
    )
}

export default MainScreen