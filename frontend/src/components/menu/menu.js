import { Outlet, Link } from "react-router-dom";

const Menu = () => {
    const logout = () => {
        localStorage.removeItem("AUTH_TOKEN");
    };

    return (
        <>
            <Link to="/chambre">Chambre</Link>
            <br />
            <Link to="/client">Client</Link>
            <br />
            <Link to="/admin">Administration</Link>
            <br />
            <Link to="/rechercherReservation">Réservations</Link>
            <br />
            <Link to="/login">Connexion</Link>
            <br />
            <Link to="/login" onClick={logout}>Déconnexion</Link>
            <br />
            <br />
            <Outlet />
        </>
    );
};

export default Menu;