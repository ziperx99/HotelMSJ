from pydantic import BaseModel, Field, model_validator, field_validator
from modele.usager import Usager
from uuid import UUID

class UsagerDTO(BaseModel):
    id_usager: UUID = Field(custom_error='id_usager doit être un UUID comportant 36 caractères')
    prenom: str = Field(max_length=50, custom_error='prenom a une limite de 50 caractères')
    nom: str = Field(max_length=50, custom_error='nom a une limite de 50 caractères')
    adresse: str = Field(max_length=100, custom_error='adresse a une limite de 100 caractères')
    mobile: str = Field(max_length=15, custom_error='mobile a une limite de 15 caractères')
    mot_de_passe: str = Field(max_length=60, custom_error='mot_de_passe a une limite de 60 caractères')

    def __init__(self, usager: Usager = None):
        super().__init__(
            id_usager=usager.id_usager,
            prenom=usager.prenom,
            nom=usager.nom,
            adresse=usager.adresse,
            mobile=usager.mobile,
            mot_de_passe=usager.mot_de_passe
        )