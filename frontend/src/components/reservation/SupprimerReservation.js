import { useState } from "react";
import instance from "../../axiosConfig";
import withAuthentication from "../login/withAuthentication";

const SupprimerReservation = () => {

    const [feedbackFormulaire, setfeedbackFormulaire] = useState("");
    const [erreur, setErreur] = useState(false);
    
    const supprimerReservation = async (e) => {

        e.preventDefault();

        const form = new FormData(e.target);
        const id_reservation = form.get("id_reservation")

        try {
            const response = await instance.delete(`/supprimerReservation/${id_reservation}`);
            setfeedbackFormulaire("Réservation supprimée avec succès!");
            setErreur(false);
            e.target.reset();

        } catch (error) {
            console.log(error);
            setfeedbackFormulaire("Erreur lors de la suppression de la réservation. Veuillez réessayer.");
            setErreur(true);
        }
    };

    return (
        <>
            <div className="container-fonct">
                <div className="header-fonct">
                    <h1>Supprimer une réservation</h1>
                </div>
                <div className="form-fonct">

                    <form onSubmit={supprimerReservation}>
                        <table>
                            <tbody>
                                <tr>
                                    <td><label htmlFor="id_reservation">ID Réservation:</label></td>
                                    <td><input type="text" id="id_reservation" name="id_reservation" required></input></td>
                                </tr>
                            </tbody>
                        </table>
                        <div className="form-button">
                            <button type="submit">Supprimer</button>
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

export default withAuthentication(SupprimerReservation);

