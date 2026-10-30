from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from metier.chambre_metier import ChambreDTO, TypeChambreDTO, creer_chambre, get_chambre_par_numero, modifier_chambre, supprimer_chambre, creer_type_chambre, rechercher_type_chambre, modifier_type_chambre, supprimer_type_chambre
from DTO.chambre_dto import TypeChambreDTO
from metier.reservation_metier import rechercher_reservation
from DTO.rechercher_reservation_dto import RechercherReservationDTO
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID
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
@app.post("/modifierChambre")
def read_item(chambre: ChambreDTO):
    try:
        return modifier_chambre(chambre)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

# Supprimer Chambre
@app.delete("/supprimerChambre/{id_chambre}")
def read_item(id_chambre: UUID):
    try:
        return supprimer_chambre(id_chambre)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

# Créer Type Chambre
@app.post("/creerTypeChambre")
def read_item(type: TypeChambreDTO):
    try:
        return creer_type_chambre(type)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

# Rechercher Type Chambre
@app.get("/rechercherTypeChambre/{id_type_chambre}")
def read_item(id_type_chambre: UUID):
    try:
        return rechercher_type_chambre(id_type_chambre)
    except ValueError as e:
            return HTTPException(status_code=404, detail=str(e))

# Modifier Type Chambre
@app.post("/modifierTypeChambre")
def read_item(type_chambre: TypeChambreDTO):
    try:
        return modifier_type_chambre(type_chambre)
    except ValueError as e:
            return HTTPException(status_code=404, detail=str(e))

# Supprimer Type Chambre
@app.delete("/supprimerTypeChambre")
def read_item(id_type_chambre: UUID):
    try: 
        return supprimer_type_chambre(id_type_chambre)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))
    
# Créer Usager

# Get Usager par Nom

# Get Usager par ID

# Modifier Usager

# Supprimer Usager


# Créer Réservation

# Rechercher Réservation  #Exemple du prof que j'ai recopié mais pas touché du tout, à checker
@app.post("/rechercherReservation")
def read_item(critere: RechercherReservationDTO):
     try:
          return rechercher_reservation(critere)
     except ValueError as e:
             return HTTPException(status_code=404, detail=str(e))

# Modifier Réservation

# Supprimer Réservation


uvicorn.run(app, host="127.0.0.1", port=8000)