from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, model_validator


class CreerReservationDTO(BaseModel):
    date_debut_reservation: datetime
    date_fin_reservation: datetime
    prix_jour: float = Field(gt=0)
    info_reservation: Optional[str] = None
    id_usager: UUID
    numero_chambre: int = Field(ge=0)

    @model_validator(mode="after")
    def verifier_dates(self):
        if self.date_fin_reservation <= self.date_debut_reservation:
            raise ValueError("La date de fin doit être après la date de début.")
        return self