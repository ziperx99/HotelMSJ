import RechercheReservation from "./components/reservation/RechercheReservation";
import CreerReservation from "./components/reservation/CreerReservation";
import SupprimerReservation from "./components/reservation/SupprimerReservation";
import Client from "./components/client/Client";
import Admin from "./components/admin/admin";
import Menu from "./components/menu/menu";
import Chambre from "./components/chambre/Chambre";
import Login from "./components/login/Login";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import logo from "./hotel_logo2.png";

function App() {
  return (    
     <BrowserRouter>        
        <ApplicationLogo/>
        <br/>
          <Routes>
            <Route path="/" element={<Menu />} >
              <Route path="/login" index element={<Login />} />
              <Route path="/rechercherReservation" element={<RechercheReservation />} />
              <Route path="/creerReservation" element={<CreerReservation />} />
              <Route path="/supprimerReservation" element={<SupprimerReservation />} />
              <Route path="/chambre" element={<Chambre />} />
              <Route path="/client" element={<Client />} />
              <Route path="/admin" element={<Admin />} />
            </Route>
          </Routes>
      </BrowserRouter>
  );
}

function ApplicationLogo() {
  return <img src={logo} alt="Logo de l'hotel" className="centre" />
}

export default App;