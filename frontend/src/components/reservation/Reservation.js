import { useState } from "react";

function Reservation({ reservation }) {
  const [isClientVisible, setIsClientVisible] = useState(false);
  const [isChambreVisible, setIsChambreVisible] = useState(false);

  return (
    <>    
      <h4>Du {reservation.date_debut_reservation}. au {reservation.date_fin_reservation}</h4>
      <p>{reservation.prix_jour}$ par jour</p>
      <div>
        <button 
          className="button-info" 
          onClick={() => setIsClientVisible(!isClientVisible)}
        >
          {reservation.usager.prenom} {reservation.usager.nom}
        </button>
        <p hidden={!isClientVisible}>
          {reservation.usager.adresse}
          <br />
          {reservation.usager.mobile}
        </p>
        
        <br />
        <button 
          className="button-info" 
          onClick={() => setIsChambreVisible(!isChambreVisible)}
        >
          Chambre {reservation.chambre.numero_chambre}
        </button>
        <p hidden={!isChambreVisible}>
          <img src={`chambre${reservation.chambre.type_chambre.nom_type}.jpeg`} alt={"Chambre" + reservation.chambre.numero_chambre} />
          <br />
          {reservation.chambre.disponible_reservation}
          <br />
          {reservation.chambre.autre_informations}
        </p>
        {/* TODO PD:  Ajouter un bouton afin de basculer en mode edition ou lecture seul */}
      </div>
      {/* TODO PD:  Programmer la composante lorsqu'en mode édition */}
    </>
  );
}

{/* TODO JO:  CSS de l'affichage des réservations */}

export default Reservation;