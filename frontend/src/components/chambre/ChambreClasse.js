import {Component} from "react";
import instance from "../../axiosConfig";
import withAuthentication from "../login/withAuthentication";

class Chambre extends Component {
    constructor(props) {
        super(props);
        this.state = {
          chambre: {
            type_chambre : {}
          },
          numero: ""
        };
        this.getChambre = this.getChambre.bind(this);
        this.setResponseData = this.setResponseData.bind(this);
    }

    render() {
        return (
         <>
            <button onClick={this.getChambre}>Rechercher</button>
            <label htmlFor="numero">Numéro chambre : </label>
            <input type="text" id="numero" value={this.state.numero} onChange={ e => this.onChangeInputNumero(e.target.value) } />
            <p> {this.state.chambre.numero_chambre} <br></br>
                {this.state.chambre.type_chambre.nom_type}
            </p>
         </>
        );
    }

    getChambre() {
        instance.get(`/chambres/${this.state.numero}`)
            .then(this.setResponseData)
            .catch(console.log);    
    }

    onChangeInputNumero(data) {
        this.setState({
          numero : data
        });
    }

    setResponseData(response) {
        this.setState({
            chambre: response.data,
        });
    }
}

export default withAuthentication(Chambre);