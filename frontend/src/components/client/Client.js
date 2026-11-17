import withAuthentication from "../login/withAuthentication";

const Client = () => {
    return (
        <>
            <div>COMPOSANTE CLIENT</div>
        </>
    );
};

export default withAuthentication(Client);