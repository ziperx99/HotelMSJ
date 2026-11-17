import { useState } from "react";
import instance from "../../axiosConfig";
import withAuthentication from "../login/withAuthentication";

const Chambre = () => {
    const [chambre, setChambre] = useState({
        chambre: {
            type_chambre : {}
          }
    });
    
    const [numero, setNumero] = useState("");

    const getChambre = async () => {
        try {
            const response = await instance.get(`/chambres/${numero}`);
            setChambre(response.data);
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <>
            <button onClick={getChambre}>Rechercher</button>
            <label htmlFor="numero">Numéro chambre : </label>
            <input
                type="text"
                id="numero"
                value={numero}
                onChange={(e) => setNumero(e.target.value)}
            />
            <p>
                {chambre.numero_chambre} <br />
                {chambre.type_chambre?.nom_type}
            </p>
        </>
    );
};

export default withAuthentication(Chambre);
