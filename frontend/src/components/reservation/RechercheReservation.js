import { useState } from "react";
import ListeReservation from "./ListeReservation";
import instance from "../../axiosConfig";
import withAuthentication from "../login/withAuthentication";

const RechercheReservation = () => {
    const [reservations, setReservations] = useState([]);
    const [idReservation, setIdReservation] = useState(null);
    const [idUsager, setIdUsager] = useState(null);
    const [idChambre, setIdChambre] = useState(null);
    const [nom, setNom] = useState(null);
    const [prenom, setPrenom] = useState(null);
    const [disponibleSeulement, setDisponibleSeulement] = useState(false);
    const [date, setDate] = useState(null);
    const [feedbackFormulaire, setfeedbackFormulaire] = useState("");
    const [erreur, setErreur] = useState(false);

    const rechercherReservations = async () => {

        setfeedbackFormulaire("");
        setErreur(false);

        const requestData = {
            id_reservation: idReservation || null,
            id_usager: idUsager || null,
            id_chambre: idChambre || null,
            nom: nom || null,
            prenom: prenom || null,
            disponible_reservation: disponibleSeulement ? true : null,
            date: date || null
        };

        try {
            const response = await instance.post("/rechercherReservation", requestData);
            setReservations(response.data);
            if (response.data.length > 0) {
                setfeedbackFormulaire("Affichage des " + response.data.length + " résultat(s) de recherche.")
            }
            else if (response.data.length == 0) {
                setfeedbackFormulaire("Aucun résultat de recherche trouvé.")
            }

            setErreur(false);
        } catch (error) {
            console.log(error);
            let messageErreur = "Erreur lors de la recherche.";

            if (error.response){
                const detail = error.response.data.detail;

                if (Array.isArray(detail)) {
                    messageErreur = detail.map(err => err.msg.replace("Value error, ", ""));
                } else if (typeof detail === "string") {
                    messageErreur = detail;
                } 
 
            } else {
                messageErreur = error.message;
            }

            setfeedbackFormulaire("Erreur :\n" + messageErreur);
            setErreur(true);
        }
    };

    const effacerReservations = () => {
        setReservations([]);
        setIdReservation("");
        setIdUsager("");
        setIdChambre("");
        setNom("");
        setPrenom("");
        setDisponibleSeulement(null);
        setDate("")
        setErreur(false);
        setfeedbackFormulaire("");
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
                                <td><label htmlFor="idReservation">ID réservation:</label></td>
                                <td><input type="text" id="idReservation" value={idReservation} onChange={(e) => setIdReservation(e.target.value)}/></td>
                            </tr>
                            <tr>
                                <td><label htmlFor="idUsager">ID usager:</label></td>
                                <td><input type="text" id="idUsager" value={idUsager} onChange={(e) => setIdUsager(e.target.value)}/></td>
                            </tr>
                            <tr>
                                <td><label htmlFor="idChambre">ID chambre:</label></td>
                                <td><input type="text" id="idChambre" value={idChambre} onChange={(e) => setIdChambre(e.target.value)}/></td>
                            </tr>
                            <tr>
                                <td><label htmlFor="nom">Nom:</label></td>
                                <td><input type="text" id="nom" value={nom} onChange={(e) => setNom(e.target.value)}/></td>
                            </tr>
                            <tr>
                                <td><label htmlFor="prenom">Prénom:</label></td>
                                <td><input type="text" id="prenom" value={prenom} onChange={(e) => setPrenom(e.target.value)}/></td>
                            </tr>
                            <tr>
                                <td><label htmlFor="date">Date:</label></td>
                                <td><input type="date" id="date" value={date} onChange={(e) => setDate(e.target.value)}/></td>
                            </tr>
                            <tr>
                                <td><label htmlFor="disponibleSeulement">Chambres disponibles:</label></td>
                                <td><input type="checkbox" id="disponibleSeulement" checked={disponibleSeulement} onChange={(e) => setDisponibleSeulement(e.target.checked)}/></td>
                            </tr>
                        </tbody>
                    </table>
                    <div className="form-button">
                        <button onClick={rechercherReservations}>Rechercher</button>
                        <button onClick={effacerReservations}>Effacer</button>
                    </div>
                </div>
            </div>
            {feedbackFormulaire && (
                <div className={`feedbackFormulaire ${erreur ? "erreur" : "succes"}`}>
                    <p>{feedbackFormulaire}</p>
                </div>
            )}    
            
            {reservations !== undefined && (
                <ListeReservation reservations={reservations} />
            )}
        </>
    );
};

export default withAuthentication(RechercheReservation);
