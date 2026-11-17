import { useState } from "react";
import { useNavigate } from "react-router-dom";
import instance from "../../axiosConfig";

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const getToken = async () => {
        try {
            const response = await instance.post(
                "/token",
                {
                    username,
                    password
                },
                {
                    headers: { "Content-Type": "application/x-www-form-urlencoded" }
                }
            );

            localStorage.setItem(
                "AUTH_TOKEN",
                `${response.data.token_type} ${response.data.access_token}`
            );
            navigate("/rechercherReservation");
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <>
            <br />
            <label htmlFor="usager">Usager : </label>
            <input
                type="text"
                id="usager"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <br />
            <label htmlFor="motdepasse">Mot de passe : </label>
            <input
                type="password"
                id="motdepasse"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <br />
            <button onClick={getToken}>Se connecter</button>
        </>
    );
};

export default Login;