# Modules et librairies
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, model_validator, field_validator


class RechercherReservationDTO(BaseModel):
    id_reservation: Optional[UUID] = None
    id_usager: Optional[UUID] = None
    id_chambre: Optional[UUID] = None
    nom: Optional[str] = Field(default = None, max_length = 50, custom_error = 'Nom a une limite de 50 caractères')
    prenom: Optional[str] = Field(default = None, max_length = 50, custom_error = 'Prénom a une limite de 50 caractères')
    disponible_reservation : Optional[bool] = Field(default = None, custom_error='disponible_reservation doit être un bool')
    date: Optional[datetime] = Field(default = None, custom_error = 'La date doit être valide')

    @model_validator(mode='after')
    def verifier_nom_et_prenom_ensemble(self):
        if (self.nom is not None and self.prenom is None) or (self.nom is None and self.prenom is not None):
            raise ValueError("Le nom et prénom doivent tous deux être présents ou absents")
        return self

    @field_validator("id_reservation", mode="before")
    @classmethod
    def verifier_id_reservation(cls, valeur):
        if valeur is None:
            return valeur

        try:
            uuid = UUID(str(valeur))
            if len(str(valeur)) != 36:
                raise ValueError()
            return uuid

        except (ValueError, TypeError, AttributeError):
            raise ValueError("L'ID de réservation doit être un UUID valide de 36 caractères.")

    @field_validator("id_usager", mode="before")
    @classmethod
    def verifier_id_usager(cls, valeur):
        if valeur is None:
            return valeur

        try:
            uuid = UUID(str(valeur))
            if len(str(valeur)) != 36:
                raise ValueError()
            return uuid

        except (ValueError, TypeError, AttributeError):
            raise ValueError("L'ID Usager doit être un UUID valide de 36 caractères.")

    @field_validator("id_chambre", mode="before")
    @classmethod
    def verifier_id_chambre(cls, valeur):
        if valeur is None:
            return valeur

        try:
            uuid = UUID(str(valeur))
            if len(str(valeur)) != 36:
                raise ValueError()
            return uuid

        except (ValueError, TypeError, AttributeError):
            raise ValueError("L'ID Chambre doit être un UUID valide de 36 caractères.")
