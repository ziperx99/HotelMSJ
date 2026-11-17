import {Navigate} from 'react-router-dom';

const withAuthentication = (Component) => {
    const Wrapper = (props) => {
      const isAuthenticated = localStorage.AUTH_TOKEN ? true : false;
      
      return (
            isAuthenticated ? <Component {...props} /> : <Navigate to="/login"  />
        );
    };
    return Wrapper;
  };

  export default withAuthentication;