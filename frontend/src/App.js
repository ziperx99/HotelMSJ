import Reservation from './components/reservation/ReservationFonction';
import logo from './logo.svg';
import './App.css';
import RechercheReservation from './components/reservation/RechercheReservationFonction';

const reservation1 = {
  du: "15 décembre 2024",
  au: "24 décembre 2024",
  prix: "129.99",
  client: {
    prenom: "Jean",
    nom: "Saisrien",
    adresse: "1234 rue Des Tulipes, Gaspé",
    mobile: "418-123-4567"
  },
  chambre: {
    numero: "12"
  }
}

const reservation2 = {
  du: "25 décembre 2024",
  au: "31 décembre 2024",
  prix: "159.99",
  client: {
    prenom: "Paul",
    nom: "Therrien",
    adresse: "6789 rue Des Érables, Matane",
    mobile: "418-456-1234"
  },
  chambre: {
    numero: "324"
  }
}

function App() {
  return (
    <>
      <RechercheReservation/>
    </>
  );
}

export default App;



