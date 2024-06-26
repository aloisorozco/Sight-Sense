import './App.css';
import AppContainer from './pages/camera';
import NavBar from './components/nav_bar';
import LandingPage from "./pages/landing_page"

function App() {

  return (
    <div className="App">
      <NavBar />
      <LandingPage />
    </div>
  );
}

export default App;
