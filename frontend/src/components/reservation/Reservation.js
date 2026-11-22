import { useState } from "react";
import instance from "../../axiosConfig";
import withAuthentication from "../login/withAuthentication";

function Reservation({ reservation }) {
  const [isClientVisible, setIsClientVisible] = useState(false);
  const [isChambreVisible, setIsChambreVisible] = useState(false);
  const [modeEdition, setModeEdition] = useState(false);
  const [feedbackFormulaire, setfeedbackFormulaire] = useState("");
  const [erreur, setErreur] = useState(false);

  const [dateDebut, setDateDebut] = useState(new Date(reservation.date_debut_reservation).toLocaleDateString("fr-CA"));
  const [dateFin, setDateFin] = useState(new Date(reservation.date_fin_reservation).toLocaleDateString("fr-CA"));
  const [prixJour, setPrixJour] = useState(reservation.prix_jour);
  const [infoReservation, setInfoReservation] = useState(reservation.info_reservation);
  const [idClient, setIdClient] = useState(reservation.usager.id_usager);
  const [noChambre, setNoChambre] = useState(reservation.chambre.numero_chambre);
  
  const modifierReservation = async () => {

        setfeedbackFormulaire("");
        setErreur(false);

        const modificationReservation = {
            id_reservation: reservation.id_reservation,
            date_debut_reservation: new Date(dateDebut).toISOString(),
            date_fin_reservation: new Date(dateFin).toISOString(),
            prix_jour: prixJour,
            info_reservation: infoReservation,
            usager: {
              id_usager: idClient,
              prenom: reservation.usager.prenom,
              nom: reservation.usager.nom,
              adresse: reservation.usager.adresse,
              mobile: reservation.usager.mobile,
              mot_de_passe: reservation.usager.mot_de_passe
            },
            chambre: {
              idChambre: reservation.chambre.idChambre,
              numero_chambre: noChambre,
              disponible_reservation: reservation.chambre.disponible_reservation,
              autre_informations: reservation.chambre.autre_informations,
              type_chambre: {
                id_type_chambre: reservation.chambre.type_chambre.id_type_chambre,
                nom_type: reservation.chambre.type_chambre.nom_type,
                prix_plafond: reservation.chambre.type_chambre.prix_plafond,
                prix_plancher: reservation.chambre.type_chambre.prix_plancher,
                description_chambre: reservation.chambre.type_chambre.description_chambre
              }
            },
        }

        try {
            const response = await instance.post("/modifierReservation", modificationReservation);
            setfeedbackFormulaire("Réservation modifiée avec succès!\n Veuillez relancer la recherche pour voir les nouvelles données.")
            setErreur(false);


            
            setModeEdition(false);
        } catch (error) {
            console.log(error);

            let messageErreur = "Erreur lors de la modification de la réservation.";

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

  return (
    <>
      <div className="container-reservation">
        {/* Affichage du mode lecture seule */}
        {!modeEdition ? (
          <div>
            <div className="header-fonct">
              <h1>Résultat de recherche</h1>
            </div>
            <table>
              <tbody>
                <tr>
                  <td>Date de début:</td>
                  <td>{new Date(reservation.date_debut_reservation).toLocaleDateString("fr-CA")}</td>
                </tr>
                <tr>
                  <td>Date de fin:</td>
                  <td>{new Date(reservation.date_fin_reservation).toLocaleDateString("fr-CA")}</td>
                </tr>
                <tr>
                  <td>Prix par jour:</td>
                  <td>{reservation.prix_jour}$</td>
                </tr>
                <tr>
                  <td>Informations:</td>
                  <td>{(reservation.info_reservation ? reservation.info_reservation : "Non" )}</td>
                </tr>
                <tr>
                  <td>
                    <div className="form-button">
                      <button onClick={() => setIsClientVisible(!isClientVisible)}>
                        Informations client
                      </button>
                    </div>
                  </td>
                </tr>
                <tr hidden={!isClientVisible}>
                  <td>Nom:</td>
                  <td>{reservation.usager.prenom} {reservation.usager.nom}</td>
                </tr>
                <tr hidden={!isClientVisible}>
                  <td>Adresse:</td>
                  <td>{reservation.usager.adresse}</td>
                </tr>
                <tr hidden={!isClientVisible}>
                  <td>Mobile:</td>
                  <td>{reservation.usager.mobile}</td>
                </tr>
                <tr>
                  <td>
                    <div className="form-button">
                      <button onClick={() => setIsChambreVisible(!isChambreVisible)}>
                        Informations chambre
                      </button>
                    </div>
                  </td>
                </tr>
                <tr hidden={!isChambreVisible}>
                  <td>Numéro de chambre:</td>
                  <td>{reservation.chambre.numero_chambre}</td>
                </tr>
                <tr hidden={!isChambreVisible}>
                  <td>Disponibilité:</td>
                  <td>{(reservation.chambre.disponible_reservation ? "Oui" : "Non")}</td>
                </tr>
                <tr hidden={!isChambreVisible}>
                  <td>Autres informations:</td>
                  <td>{(reservation.chambre.autre_informations ? reservation.chambre.autre_informations : "Non" )}</td>
                </tr>
                <tr hidden={!isChambreVisible}>
                  <td>Image:</td>
                  <td><img src={`chambre${reservation.chambre.type_chambre.nom_type}.jpeg`} alt={"Chambre" + reservation.chambre.numero_chambre} /></td>
                </tr>
              </tbody>
            </table>
            <div className="form-button">
              <button className="button-mode-edition" onClick={() => setModeEdition(true)}>
                Modifier
              </button>
            </div>

            {/* Ancien code exemple, je le laisse là pour le moment à titre d'exemple mais l'affichage ci-haut est la version retravaillée par moi. -Jo */}
            {/*

            <h4>Du {reservation.date_debut_reservation} au {reservation.date_fin_reservation}</h4>
            <p>{reservation.prix_jour}$ par jour</p>
            <div>
              <button className="button-info" onClick={() => setIsClientVisible(!isClientVisible)}>
                {reservation.usager.prenom} {reservation.usager.nom}
              </button>
              <p hidden={!isClientVisible}>
                {reservation.usager.adresse}
                <br />
                {reservation.usager.mobile}
              </p>
              
              <br />
              <button className="button-info" onClick={() => setIsChambreVisible(!isChambreVisible)}>
                Chambre {reservation.chambre.numero_chambre}
              </button>
              <p hidden={!isChambreVisible}>
                <img src={`chambre${reservation.chambre.type_chambre.nom_type}.jpeg`} alt={"Chambre" + reservation.chambre.numero_chambre} />
                <br />
                {reservation.chambre.disponible_reservation}
                <br />
                {reservation.chambre.autre_informations}
              </p>

            </div>
            */}

          </div>
        ) : ( 
        <div>
          {/* Affichage du mode édition */}
            <div className="header-fonct">
              <h1>Modifier une réservation</h1>
            </div>
                <div className="form-fonct">
                    <table>
                        <tbody>
                            <tr>
                                <td><label htmlFor="date_debut_reservation">Date de début:</label></td>
                                <td><input type="date" id="date_debut_reservation" name="date_debut_reservation" value={dateDebut} onChange={(e) => setDateDebut(e.target.value)} required></input></td>
                            </tr>
                            <tr>
                                <td><label htmlFor="date_fin_reservation">Date de fin:</label></td>
                                <td><input type="date" id="date_fin_reservation" name="date_fin_reservation" value={dateFin} onChange={(e) => setDateFin(e.target.value)} required></input></td>
                            </tr>
                            <tr>
                                <td><label htmlFor="prix_jour">Prix par jour:</label></td>
                                <td><input type="text" id="prix_jour" name="prix_jour" value={prixJour} onChange={(e) => setPrixJour(e.target.value)} required></input></td>
                            </tr>
                            <tr>
                                <td><label htmlFor="noChambre">Numéro de chambre:</label></td>
                                <td><input type="number" id="noChambre" name="noChambre" value={noChambre} onChange={(e) => setNoChambre(e.target.value)} required></input></td>
                            </tr>
                            <tr>
                                <td><label htmlFor="id_usager">ID Usager:</label></td>
                                <td><input type="text" id="id_usager" name="id_usager" value={idClient} onChange={(e) => setIdClient(e.target.value)} required></input></td>
                            </tr>
                            <tr>
                                <td><label htmlFor="info_reservation">Informations réservation:</label></td>
                                <td><textarea id="info_reservation" name="info_reservation" rows="4" cols="50" value={infoReservation} onChange={(e) => setInfoReservation(e.target.value)}></textarea></td>
                            </tr>
                        </tbody>
                    </table>
                    <div className="form-button">
                        <button onClick={modifierReservation}>Soumettre</button>
                        <button className="button-mode-edition" onClick={() => setModeEdition(false)}>Annuler</button>
                    </div>
                </div>
        </div>    
        )}
        
      </div> 
      {feedbackFormulaire && (
        <div className={`feedbackFormulaire ${erreur ? "erreur" : "succes"}`}>
            <p>{feedbackFormulaire}</p>
        </div>
      )}
    </>
  );
}

{/* TODO:  CSS de l'affichage des réservations */}

export default withAuthentication(Reservation);