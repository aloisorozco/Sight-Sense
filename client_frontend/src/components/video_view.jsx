import classes from "./video_view.module.css"
import 'bootstrap/dist/css/bootstrap.min.css';

function MainScreen() {
    const vide_url = "http://127.0.0.1:5500/video_feed"

    return (
        <div className={`shadow mr-auto ${classes.view_container}`}>
            <img src={vide_url} alt="stream" />
        </div>
    )
}

export default MainScreen