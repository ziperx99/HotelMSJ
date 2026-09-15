from typing import List, TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped, relationship, mapped_column

from modele.chambre import Base

if TYPE_CHECKING:
    from modele.reservation import Reservation


class Usager(Base):
    __tablename__ = "usager"

    prenom: Mapped[str]
    nom: Mapped[str]
    adresse: Mapped[str]
    mobile: Mapped[str]
    mot_de_passe: Mapped[str]

    id_usager: Mapped[UUID] = mapped_column(primary_key=True)

    # Relation 1 à N
    reservations: Mapped[List["Reservation"]] = relationship(
        back_populates="usager"
    )