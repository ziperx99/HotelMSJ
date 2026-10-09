from typing import Optional
from pydantic import BaseModel
from modele.usager import Usager
from uuid import UUID


class UsagerDTO(BaseModel):
    id_usager: Optional[UUID] = None
    prenom: str
    nom: str
    adresse: str
    mobile: str
    mot_de_passe: str

    def __init__(self, usager: Usager):
        super().__init__(
            id_usager=usager.id_usager,
            prenom=usager.prenom,
            nom=usager.nom,
            adresse=usager.adresse,
            mobile=usager.mobile,
            mot_de_passe=usager.mot_de_passe
        )