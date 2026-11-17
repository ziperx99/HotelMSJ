import { useState } from "react";
import ListeReservation from "./ListeReservation";
import instance from "../../axiosConfig";
import withAuthentication from "../login/withAuthentication";

const RechercheReservation = () => {
    const [reservations, setReservations] = useState([]);
    const [nom, setNom] = useState("");
    const [prenom, setPrenom] = useState("");

    const rechercherReservations = async () => {
        const requestData = {
            idReservation: null,
            idUsager: null,
            idChambre: null,
            nom: nom,
            prenom: prenom
        };

        try {
            const response = await instance.post("/rechercherReservation", requestData);
            setReservations(response.data);
        } catch (error) {
            console.log(error);
        }
    };

    const effacerReservations = () => {
        setReservations([]);
        setNom("");
        setPrenom("");
    };

    return (
        <>
            <button onClick={rechercherReservations}>Rechercher</button>
            <button onClick={effacerReservations}>Effacer</button>
            <br />
            <label htmlFor="nom">Nom:</label>
            <input
                type="text"
                id="nom"
                value={nom}
                onChange={(e) => setNom(e.target.value)}
            />
            <label htmlFor="prenom">Prénom:</label>
            <input
                type="text"
                id="prenom"
                value={prenom}
                onChange={(e) => setPrenom(e.target.value)}
            />

            {reservations !== undefined && (
                <ListeReservation reservations={reservations} />
            )}
        </>
    );
};

export default withAuthentication(RechercheReservation);
