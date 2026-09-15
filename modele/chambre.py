from typing import List, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column

if TYPE_CHECKING:
    from modele.TypeChambre import TypeChambre
    from modele.reservation import Reservation


class Base(DeclarativeBase):
    pass


class Chambre(Base):
    __tablename__ = "chambre"

    numero_chambre: Mapped[int]
    disponible_reservation: Mapped[bool]
    autre_informations: Mapped[str] = mapped_column(nullable=True)

    id_chambre: Mapped[UUID] = mapped_column(primary_key=True)

    fk_type_chambre: Mapped[UUID] = mapped_column(
        ForeignKey("type_chambre.id_type_chambre"),
        nullable=True
    )

    # Relation N à 1
    type_chambre: Mapped["TypeChambre"] = relationship(
        back_populates="chambres"
    )

    # Relation 1 à N
    reservations: Mapped[List["Reservation"]] = relationship(
        back_populates="chambre"
    )