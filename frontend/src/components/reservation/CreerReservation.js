import { useState } from "react";

var mockReservations = [
    {
        du: "15 décembre 2024",
        au: "24 décembre 2024",
        prix: "129.99",
        client: {
            prenom: "Jean",
            nom: "Saisrien",
            adresse: "1234 rue Des Tulipes, Gaspé",
            mobile: "418-123-4567"
        },
        chambre: {
            numero: "12"
        }
    },
    {
        du: "25 décembre 2024",
        au: "31 décembre 2024",
        prix: "159.99",
        client: {
            prenom: "Paul",
            nom: "Therrien",
            adresse: "6789 rue Des Érables, Matane",
            mobile: "418-456-1234"
        },
        chambre: {
            numero: "324"
        }
    }
]

const CreerReservation = () => {
    const [reservations, setReservations] = useState(mockReservations);
    
    const ajouterReservation = (e) => {

        // TODO: VRAIE INTÉGRATION BACKEND (Et non ajout à une liste "mock")
        // À voir avec le cours du 17 novembre.

        e.preventDefault();

        const form = new FormData(e.target);

        const nouvelleReservation = {
            du: form.get("du"),
            au: form.get("au"),
            prix: form.get("prix"),
            client: {
                prenom: form.get("prenom"),
                nom: form.get("nom"),
                adresse: form.get("adresse"),
                mobile: form.get("mobile"),
            },
            chambre:{
                numero: form.get("noChambre")
            }
        };

        setReservations([...reservations, nouvelleReservation]);

        e.target.reset();
    };

    return (
        <>
            <h1>Ajouter une réservation</h1>

            <form onSubmit={ajouterReservation}>
                <label for="du">Date de début:</label>
                <input type="date" id="du" name="du"></input>
                <br></br>
                <label for="au">Date de fin:</label>
                <input type="date" id="au" name="au"></input>
                <br></br>
                <label for="prix">Prix:</label>
                <input type="text" id="prix" name="prix"></input>
                <br></br>
                <label for="noChambre">Numéro de chambre:</label>
                <input type="number" id="noChambre" name="noChambre"></input>
                <br></br>
                <label for="nom">Nom:</label>
                <input type="text" id="nom" name="nom"></input>
                <br></br>
                <label for="prenom">Prenom:</label>
                <input type="text" id="prenom" name="prenom"></input>
                <br></br>
                <label for="adresse">Adresse:</label>
                <input type="text" id="adresse" name="adresse"></input>
                <br></br>
                <label for="mobile">Mobile:</label>
                <input type="text" id="mobile" name="mobile"></input>
                <br></br>
                <button type="submit">Ajouter</button>
            </form>

            {/* Affichage temporaire test */}
            {reservations.map((reservation,index) => (
                <div key={index}>
                    <p>Du: {reservation.du}</p>
                    <p>Au: {reservation.au}</p>
                    <p>Prix: {reservation.prix}</p>
                    <p>No. chambre: {reservation.chambre.numero}</p>
                    <p>Nom: {reservation.client.nom}</p>
                    <p>Prénom: {reservation.client.prenom}</p>
                    <p>Adresse: {reservation.client.adresse}</p>
                    <p>Mobile: {reservation.client.mobile}</p>
                    <br></br>

                </div>
            ))}
        </>
    );
};

export default CreerReservation;


