from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, model_validator, field_validator


class CreerReservationDTO(BaseModel):
    date_debut_reservation: datetime
    date_fin_reservation: datetime
    prix_jour: float
    info_reservation: Optional[str] = None
    id_usager: UUID
    numero_chambre: int

    @field_validator("id_usager", mode="before")
    @classmethod
    def verifier_id_usager(cls, valeur):
        try:
            uuid = UUID(str(valeur))
            if len(str(valeur)) != 36:
                raise ValueError()
            return uuid
        except (ValueError, TypeError, AttributeError):
            raise ValueError("L'ID usager doit être un UUID valide de 36 caractères.")

    @field_validator("numero_chambre")
    @classmethod
    def verifier_numero_chambre(cls, valeur):
        if valeur < 0:
            raise ValueError("Le numéro de chambre doit être un entier positif.")
        return valeur

    @model_validator(mode="after")
    def verifier_dates(self):
        if self.date_fin_reservation <= self.date_debut_reservation:
            raise ValueError("La date de fin doit être après la date de début.")
        return self

    @model_validator(mode="after")
    def verifier_prix(self):
        if self.prix_jour <= 0:
            raise ValueError("Le prix doit être une valeur positive.")
        return self
