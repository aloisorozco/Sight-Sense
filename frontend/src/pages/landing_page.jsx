import '../App.css';
import NavBar from '../components/nav_bar';
import InfoBar from '../components/intro_component';
import classes from "./landing_page.css"

function AppContainer(){
    return(
        <div className="App-content-container">
            <NavBar />
            <div className={classes.main_container}>
                <InfoBar />
            </div>
        </div>
    )
}

export default AppContainer