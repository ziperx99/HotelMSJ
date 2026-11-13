import { useState } from "react";
import ListeReservation from "./ListeReservation";

const RechercheReservation = () => {
    const [reservations, setReservations] = useState(undefined);
    
    const rechercheReservations = () => {
        setReservations(mockReservations);
    };

    const effacerReservations = () => {
        setReservations([]);
    };

    return (
        <>
            <h1>Rechercher des réservations</h1>
            <button onClick={rechercheReservations}>Rechercher</button>
            <button onClick={effacerReservations}>Effacer</button>
            {reservations !== undefined && (
                <ListeReservation reservations={reservations} />
            )}
        </>
    );
};

export default RechercheReservation;

const mockReservations = [
    {
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
    },
    {
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
]