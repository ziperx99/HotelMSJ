import withAuthentication from "../login/withAuthentication";

const Admin = () => {
    return (
        <>
            <div>COMPOSANTE ADMINISTRATIVE</div>
        </>
    );
};

export default withAuthentication(Admin);
