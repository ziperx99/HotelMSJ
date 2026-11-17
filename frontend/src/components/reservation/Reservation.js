import { useState } from "react";

function Reservation({ reservation }) {
  const [isClientVisible, setIsClientVisible] = useState(false);
  const [isChambreVisible, setIsChambreVisible] = useState(false);

  return (
    <>    
      <h4>{reservation.dateDebut} au {reservation.dateFin}</h4>
      <p>{reservation.prixParJour} par jour</p>
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
        </p>
        {/* TODO:  Ajouter un bouton afin de basculer en mode edition ou lecture seul */}
      </div>
      {/* TODO:  Programmer la composante lorsqu'en mode édition */}
    </>
  );
}

export default Reservation;