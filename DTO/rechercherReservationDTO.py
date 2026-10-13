from typing import Optional
from pydantic import BaseModel, Field, model_validator
from uuid import UUID
from datetime import datetime

class RechercherReservationDTO(BaseModel):
    id_reservation: Optional[UUID] = Field(default = None, custom_error='id_reservation doit être un UUID comportant 36 caractères')
    id_usager: Optional[UUID] = Field(default = None, custom_error='id_usager doit être un UUID comportant 36 caractères')
    id_chambre: Optional[UUID] = Field(default = None, custom_error='id_chambre doit être un UUID comportant 36 caractères')
    nom: Optional[str] = Field(default = None, max_length = 50, custom_error = 'Nom a une limite de 50 caractères')
    prenom: Optional[str] = Field(default = None, max_length = 50, custom_error = 'Prénom a une limite de 50 caractères')
    disponible_reservation : Optional[bool] = Field(default = None, custom_error='disponible_reservation doit être un bool')
    date: Optional[datetime] = Field(default = None, custom_error = 'La date doit être valide')

    @model_validator(mode='after')
    def verifier_nom_et_prenom_ensemble(self):
        if (self.nom is not None and self.prenom is None) or (self.nom is None and self.prenom is not None):
            raise ValueError("Le nom et prénom doivent tous deux présents ou absents")
        return self