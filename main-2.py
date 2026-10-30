from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from metier.chambre_metier import creer_chambre, creer_type_chambre, get_chambre_par_numero, ChambreDTO, TypeChambreDTO
from DTO.chambre_dto import TypeChambreDTO
from metier.reservation_metier import rechercher_reservation
from DTO.rechercher_reservation_dto import RechercherReservationDTO
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Créer Chambre
@app.post("/creerChambre")
def read_item(chambre: ChambreDTO):
     try:
          return creer_chambre(chambre)
     except ValueError as e:
             return HTTPException(status_code=404, detail=str(e))

# Get Chambre par numéro
@app.get("/chambres/{no_chambre}")
def read_item(no_chambre: int):
    try:
        return get_chambre_par_numero(no_chambre)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

# Modifier Chambre


# Supprimer Chambre






# Créer Type Chambre
@app.post("/creerTypeChambre/")
def read_item(type: TypeChambreDTO):
    try:
        return creer_type_chambre(type)
    except ValueError as e:
            return HTTPException(status_code=404, detail=str(e))

# Rechercher Type Chambre

# Modifier Type Chambre

# Supprimer Type Chambre




    
# Créer Usager

# Get Usager par Nom

# Get Usager par ID

# Modifier Usager

# Supprimer Usager


# Créer Réservation

# Rechercher Réservation
@app.post("/rechercherReservation")
def read_item(critere: RechercherReservationDTO):
     try:
          return rechercher_reservation(critere)
     except ValueError as e:
             return HTTPException(status_code=404, detail=str(e))

# Modifier Réservation

# Supprimer Réservation


uvicorn.run(app, host="127.0.0.1", port=8000)