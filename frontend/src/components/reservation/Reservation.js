import { useState } from "react";

function Reservation({ reservation }){
    const [isClientVisible, setIsClientVisible] = useState(false);
    const [isChambreVisible, setIsChambreVisible] = useState(false);

    return (
        <>
            <h4>{reservation.du} au {reservation.au}</h4>
            <p>{reservation.prix} par jour</p>
            <div>
                <button
                    className="button-info"
                    onClick={() => setIsClientVisible(!isClientVisible)}
                >
                    {reservation.client.prenom} {reservation.client.nom}
                </button>
                <p hidden={!isClientVisible}>
                    {reservation.client.adresse}
                    <br />
                    {reservation.client.mobile}
                </p>

                <br />
                <button
                    className="button-info"
                    onClick={() => setIsChambreVisible(!isChambreVisible)}
                >
                    Chambre {reservation.chambre.numero}
                </button>
                <p hidden={!isClientVisible}>
                </p>
            </div>
        </>
    );
}

export default Reservation;
