# Modules et librairies
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, model_validator
from modele.reservation import Reservation
from DTO.chambre_dto import ChambreDTO
from DTO.usager_dto import UsagerDTO


class ReservationDTO(BaseModel):
    id_reservation : UUID = Field(custom_error='id_reservation doit être un UUID comportant 36 caractères')
    date_debut_reservation : datetime = Field(custom_error='date_debut_reservation doit avoir un format datetime')
    date_fin_reservation : datetime = Field(custom_error='date_fin_reservation doit avoir un format datetime')
    prix_jour : float = Field(gt=0, custom_error='prix_jour doit être une valeur strictement positive')
    info_reservation : Optional[str] = Field(default=None, custom_error='info_reservation doit être un string valide')
    usager : UsagerDTO
    chambre : Optional[ChambreDTO]

    @model_validator(mode='after')
    def verifier_date_fin_ulterieure(self):
        if(self.date_fin_reservation <= self.date_debut_reservation):
            raise ValueError("La date de fin de la réservation ne peut pas être avant son début")
        return self

    def __init__(self, reservation: Reservation = None, **kwargs):

        if reservation.usager is None:
            raise ValueError("Usager manquant.")

        if reservation is not None:
            super().__init__(id_reservation = reservation.id_reservation,
                            date_debut_reservation = reservation.date_debut_reservation,
                            date_fin_reservation = reservation.date_fin_reservation,
                            prix_jour = reservation.prix_jour,
                            info_reservation = reservation.info_reservation,
                            usager = UsagerDTO(reservation.usager),
                            chambre = ChambreDTO(reservation.chambre))
        else:
                    super().__init__(**kwargs)