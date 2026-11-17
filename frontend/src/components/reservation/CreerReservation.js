import { useState } from "react";
import instance from "../../axiosConfig";
import withAuthentication from "../login/withAuthentication";

const CreerReservation = () => {

    const [feedbackFormulaire, setfeedbackFormulaire] = useState("");
    const [erreur, setErreur] = useState(false);
    
    const ajouterReservation = async (e) => {

        e.preventDefault();

        setfeedbackFormulaire("");
        setErreur(false);

        const form = new FormData(e.target);

        const nouvelleReservation = {
            date_debut_reservation: new Date(form.get("date_debut_reservation")).toISOString(),
            date_fin_reservation: new Date(form.get("date_fin_reservation")).toISOString(),
            prix_jour: Number(form.get("prix_jour")),
            info_reservation: form.get("info_reservation"),
            id_usager: form.get("id_usager"),
            numero_chambre: form.get("noChambre")
            }

        try {
            const response = await instance.post("/creerReservation", nouvelleReservation);
            setfeedbackFormulaire("Réservation créée avec succès!")
            setErreur(false);
            e.target.reset();
        } catch (error) {
            console.log(error);
            setfeedbackFormulaire("Erreur lors de l'ajout de la réservation. Veuillez réessayer.");
            setErreur(true);
        }
    };

    return (
        <> 
            <div className="container-fonct">
                <div className="header-fonct">
                    <h1>Ajouter une réservation</h1>
                </div>
                <div className="form-fonct">
                    <form onSubmit={ajouterReservation}>
                        <table>
                            <tbody>
                                <tr>
                                <td><label htmlFor="date_debut_reservation">Date de début:</label></td>
                                <td><input type="date" id="date_debut_reservation" name="date_debut_reservation" required></input></td>
                                </tr>
                                <tr>
                                <td><label htmlFor="date_fin_reservation">Date de fin:</label></td>
                                <td><input type="date" id="date_fin_reservation" name="date_fin_reservation" required></input></td>
                                </tr>
                                <tr>
                                <td><label htmlFor="prix_jour">Prix par jour:</label></td>
                                <td><input type="text" id="prix_jour" name="prix_jour" required></input></td>
                                </tr>
                                <tr>
                                <td><label htmlFor="noChambre">Numéro de chambre:</label></td>
                                <td><input type="number" id="noChambre" name="noChambre" required></input></td>
                                </tr>
                                <tr>
                                <td><label htmlFor="id_usager">ID Usager:</label></td>
                                <td><input type="text" id="id_usager" name="id_usager" required></input></td>
                                </tr>
                                <tr>
                                <td><label htmlFor="info_reservation">Informations supplémentaires:</label></td>
                                <td><textarea id="info_reservation" name="info_reservation" rows="4" cols="50"></textarea></td>
                                </tr>
                            </tbody>
                        </table>
                        <div className="form-button">
                            <button type="submit">Ajouter</button>
                        </div>
                    </form>
                </div>
            </div>
            {feedbackFormulaire && (
                <div className={`feedbackFormulaire ${erreur ? "erreur" : "succes"}`}>
                    <p>{feedbackFormulaire}</p>
                </div>
            )}
        </>
    );
};

export default withAuthentication(CreerReservation);


