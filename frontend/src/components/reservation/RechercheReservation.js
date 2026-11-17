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
            id_reservation: null,
            id_usager: null,
            id_chambre: null,
            nom: nom,
            prenom: prenom,
            disponible_reservation: null,
            date: null
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
            <div className="container-fonct">
                <div className="header-fonct">
                    <h1>Rechercher une réservation</h1>
                </div>
                <div className="form-fonct">
                    <table>
                        <tbody>
                            <tr>
                                <td><label htmlFor="nom">Nom:</label></td>
                                <td><input type="text" id="nom" value={nom} onChange={(e) => setNom(e.target.value)}/></td>
                            </tr>
                            <tr>
                                <td><label htmlFor="prenom">Prénom:</label></td>
                                <td><input type="text" id="prenom" value={prenom} onChange={(e) => setPrenom(e.target.value)}/></td>
                            </tr>
                        </tbody>
                    </table>
                    <div className="form-button">
                        <button onClick={rechercherReservations}>Rechercher</button>
                        <button onClick={effacerReservations}>Effacer</button>
                    </div>
                </div>
            </div>    





            
            
            {reservations !== undefined && (
                <ListeReservation reservations={reservations} />
            )}
        </>
    );
};

export default withAuthentication(RechercheReservation);
