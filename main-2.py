from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from metier.chambre_metier import ChambreDTO, TypeChambreDTO, creer_chambre, get_chambre_par_numero, modifier_chambre, supprimer_chambre, creer_type_chambre, rechercher_type_chambre, modifier_type_chambre, supprimer_type_chambre
from DTO.chambre_dto import TypeChambreDTO
from DTO.rechercher_reservation_dto import RechercherReservationDTO
from DTO.creer_reservation_dto import CreerReservationDTO
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID
import uvicorn

from metier.reservation_metier import (
    creer_reservation,
    rechercher_reservation,
    modifier_reservation,
    supprimer_reservation
)
from DTO.reservation_dto import ReservationDTO

#Exemples du prof
fake_users_db = {
     "johndoe": {
          "username": "johndoe",
          "full_name": "John Doe",
          "email": "johndoe@example.com",
          "hashed_password": "fakehashedsecret"
     },
     "alice": {
          "username": "alice",
          "full_name": "Alice Wonderson",
          "email": "alice@example.com",
          "hashed_password": "fakehashedsecret2"
     }
}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
     user_dict = fake_users_db.get(form_data.username)
     if not user_dict:
          raise HTTPException(status_code=400, detail="Incorrect username or password")
     user = UserInDB(**user_dict)
     hashed_password = fake_hash_password(form_data.password)
     if not hashed_password:
          raise HTTPException(status_code=400, detail="Incorrect username or password")

     return {"access_token": user.username, "token_type": "bearer"}

def fake_hash_password(password:str):
     return "fakehashed" + password

def fake_decode_token(token):
     user = get_user(fake_users_db, token)
     return user

def get_user(db, username: str):
     if username in db:
          user_dict = db[username]
          return UserInDB(**user_dict)

class User(BaseModel):
     username: str
     email: str | None = None
     full_name: str | None = None

class UserInDB(User):
     hashed_password: str

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
     user = fake_decode_token(token)
     if not user:
          raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Invalid authentication credentials",
               headers={"WWW-Authenticate": "Bearer"},
          )
     return user
     

# Créer Chambre
@app.post("/creerChambre")
def read_item(chambre: ChambreDTO, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        return creer_chambre(chambre)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

# Get Chambre par numéro
@app.get("/chambres/{no_chambre}")
def read_item(no_chambre: int, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        return get_chambre_par_numero(no_chambre)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

# Modifier Chambre
@app.post("/modifierChambre")
def read_item(chambre: ChambreDTO, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        return modifier_chambre(chambre)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

# Supprimer Chambre
@app.delete("/supprimerChambre/{id_chambre}")
def read_item(id_chambre: UUID, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        return supprimer_chambre(id_chambre)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

# Créer Type Chambre
@app.post("/creerTypeChambre")
def read_item(type: TypeChambreDTO, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        return creer_type_chambre(type)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

# Rechercher Type Chambre
@app.get("/rechercherTypeChambre/{id_type_chambre}")
def read_item(id_type_chambre: UUID, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        return rechercher_type_chambre(id_type_chambre)
    except ValueError as e:
            return HTTPException(status_code=404, detail=str(e))

# Modifier Type Chambre
@app.post("/modifierTypeChambre")
def read_item(type_chambre: TypeChambreDTO, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        return modifier_type_chambre(type_chambre)
    except ValueError as e:
            return HTTPException(status_code=404, detail=str(e))

# Supprimer Type Chambre
@app.delete("/supprimerTypeChambre")
def read_item(id_type_chambre: UUID, current_user: Annotated[User, Depends(get_current_user)]):
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