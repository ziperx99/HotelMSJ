import axios from "axios";

const instance = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    headers: {
        "Content-Type" : "application/json"
    }
});

/* Intercepteur permettant d'ajouter le token d'authentification à toutes les requêtes
HTTP s'il est présent de le storage local (Si l'utilisateur courant est déjà authentifié). */
instance.interceptors.request.use(function (config) {
    const token = localStorage.AUTH_TOKEN;
    config.headers.Authorization =  token ? token : '';
    return config;
});

export default instance;