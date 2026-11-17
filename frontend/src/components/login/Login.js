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
            <div className="container-fonct">
                <div className="header-fonct">
                    <h1>Connexion</h1>
                </div>
                <div className="form-fonct">
                    <table>
                        <tbody>
                            <tr>
                                <td><label htmlFor="usager">Usager : </label></td>
                                <td><input type="text" id="usager" value={username} onChange={(e) => setUsername(e.target.value)}/></td>
                            </tr>
                            <tr>
                                <td><label htmlFor="motdepasse">Mot de passe : </label></td>
                                <td><input type="password" id="motdepasse" value={password} onChange={(e) => setPassword(e.target.value)}/></td>
                            </tr>
                        </tbody>
                    </table>
                    <div className="form-button">
                        <button onClick={getToken}>Se connecter</button>
                    </div>
                </div>
            </div>    
        </>
    );
};

export default Login;