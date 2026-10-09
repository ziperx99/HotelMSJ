from typing import Any, Optional
from pydantic import BaseModel, Field, model_validator, field_validator
from modele.reservation import Reservation
from datetime import datetime
from DTO.chambreDTO import ChambreDTO
from DTO.usagerDTO import UsagerDTO
from uuid import UUID

class ReservationDTO(BaseModel):
    id_reservation : UUID = Field(custom_error='id_reservation doit être un UUID comportant 36 caractères')
    date_debut_reservation : datetime = Field(custom_error='date_debut_reservation doit avoir un format datetime')
    date_fin_reservation : datetime = Field(custom_error='date_fin_reservation doit avoir un format datetime')
    prix_jour : float = Field(ge=0, custom_error='prix_jour doit être une valeur positive')
    info_reservation : Optional[str] = Field(default=None, custom_error='info_reservation doit être un string valide')
    usager : UsagerDTO
    chambre : Optional[ChambreDTO]

    def __init__(self, reservation: Reservation = None):
        super().__init__(id_reservation = reservation.id_reservation,
                        date_debut_reservation = reservation.date_debut_reservation,
                        date_fin_reservation = reservation.date_fin_reservation,
                        prix_jour = reservation.prix_jour,
                        info_reservation = reservation.info_reservation,
                        usager = UsagerDTO(reservation.usager),
                        chambre = ChambreDTO(reservation.chambre))
                         