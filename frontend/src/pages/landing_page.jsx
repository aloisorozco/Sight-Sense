import '../App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import classes from "./landing_page.module.css"
import first_img from "../temp.jpg"

const GIT_LINK = "https://github.com/aloisorozco/Sight-Sense"
const INFO_LINK = "https://docs.google.com/presentation/d/1C5H3wk-y2OcS29OanowiGo0SP1mMGMjuPSlAPMM4oDk/edit#slide=id.g4dfce81f19_0_45"

function LandingPage() {

    let redirectGit = () =>{
        window.location.href = GIT_LINK
    }
    
    let redirectInfo =() =>{
        window.location.href = INFO_LINK
    }
    

    return (
        <div className="App-content-container">
            <div className={`${classes.text} ${classes.parent} `}>
                <span className={`${classes.titleText}`}>👓 Sight Sence: AI - Powered Doorbell </span>
                <span>Providing a reliable, lightweight and cheap, open source alternative to enjoy AI powered doorbell without cashing out on Amazon ;)</span>
            </div>

            <div className={`${classes.btns}`}>
                    <button type="button" onClick={redirectGit} className={`btn btn-primary btn-lg ${classes.mainButtons}`}>Repo</button>
                    <button type="button" onClick={redirectInfo} className={`btn btn-outline-secondary btn-lg ${classes.mainButtons}`}>More Details</button>
                
            </div>

            <div>
                <img src={first_img} alt="sad hamster" className={`rounded float-left img-fluid ${classes.img}`}/>
            </div>
           
            <div className={`${classes.parent}`}>
                <div className={`${classes.text} ${classes.textLeft}`}>
                    <span className={`${classes.titleText}`}>Smart Security, Featherlight Performance</span>
                    <span>Utilising the lightweight and fine-tuned YoloV8 model, this doorbell runs natively on all devices. This means, you don't have to worry about your data being streamed to the cloud for computing. Not only is your property safe, but so is your digital privacy.</span>
                </div>
            </div>
        </div>
    )
}

export default LandingPage