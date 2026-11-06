from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from metier.chambre_metier import ChambreDTO, TypeChambreDTO, creer_chambre, get_chambre_par_numero, modifier_chambre, supprimer_chambre, creer_type_chambre, rechercher_type_chambre, modifier_type_chambre, supprimer_type_chambre
from DTO.chambre_dto import TypeChambreDTO
from DTO.usager_dto import UsagerDTO
from DTO.rechercher_reservation_dto import RechercherReservationDTO
from DTO.creer_reservation_dto import CreerReservationDTO
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID
import uvicorn
from metier.usager_metier import (
    creer_usager, 
    get_usager_par_nom, 
    get_usager_par_id, 
    modifier_usager, 
    supprimer_usager
)
from metier.reservation_metier import (
    creer_reservation,
    rechercher_reservation,
    modifier_reservation,
    supprimer_reservation
)
from DTO.reservation_dto import ReservationDTO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------- SECTION CHAMBRE ----------------

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


# -------------- SECTION CHAMBRE ----------------

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

    
# -------------- SECTION USAGER ----------------
    
# Créer Usager (confirmé que ça fonctionne avec le Swagger UI)
@app.post("/creerUsager")
def read_item(usager: UsagerDTO):
    try:
        return creer_usager(usager)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))


# Get Usager par Nom (confirmé que ça fonctionne avec le Swagger UI)
@app.get("/usagers/nom/{nom}")
def read_item(nom: str):
    try:
        return get_usager_par_nom(nom)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))


# Get Usager par ID (confirmé que ça fonctionne avec le Swagger UI)
@app.get("/usagers/{id_usager}")
def read_item(id_usager: UUID):
    try:
        return get_usager_par_id(id_usager)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))


# Modifier Usager (confirmé que ça fonctionne avec le Swagger UI)
@app.post("/modifierUsager")
def read_item(usager: UsagerDTO):
    try:
        return modifier_usager(usager)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))


# Supprimer Usager (confirmé que ça fonctionne avec le Swagger UI)
@app.delete("/supprimerUsager/{id_usager}")
def read_item(id_usager: UUID):
    try:
        return supprimer_usager(id_usager)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))


# -------------- SECTION RÉSERVATION ----------------

# Créer Réservation
@app.post("/creerReservation")
def creer_reservation_api(reservation: CreerReservationDTO):
     try:
          return creer_reservation(reservation)
     except ValueError as e:
          raise HTTPException(status_code=400, detail=str(e))

# Rechercher Réservation  #Exemple du prof que j'ai recopié mais pas touché du tout, à checker 
# Yo Jo! J'ai modifié un peu pour fit ma façon d'écrire mon code mais ça revient au même que read_item, juste plus facile pour débuggé ;)
@app.post("/rechercherReservation")
def rechercher_reservation_api(critere: RechercherReservationDTO):
     try:
          return rechercher_reservation(critere)
     except ValueError as e:
             raise HTTPException(status_code=404, detail=str(e))

# Modifier Réservation
@app.put("/modifierReservation")
def modifier_reservation_api(reservation: ReservationDTO):
     try:
          modifier_reservation(reservation)

          return {"message": "Réservation modifiée avec succès."}
     except ValueError as e:
          raise HTTPException(status_code=404, detail=str(e))
     
# Supprimer Réservation
@app.delete("/supprimerReservation/{id_reservation}")
def supprimer_reservation_api(id_reservation: UUID):
     try:
          supprimer_reservation(id_reservation)
          return{"message": "Réservation supprimée avec succès."}
     except ValueError as e:
          raise HTTPException(status_code=404, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)