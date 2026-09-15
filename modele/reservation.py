from typing import TYPE_CHECKING
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from modele.chambre import Base

if TYPE_CHECKING:
    from modele.chambre import Chambre
    from modele.usager import Usager


class Reservation(Base):
    __tablename__ = "reservation"

    date_fin_reservation: Mapped[datetime]
    date_debut_reservation: Mapped[datetime]
    prix_jour: Mapped[Decimal]

    info_reservation: Mapped[str] = mapped_column(nullable=True)

    id_reservation: Mapped[UUID] = mapped_column(primary_key=True)

    fk_id_usager: Mapped[UUID] = mapped_column(
        ForeignKey("usager.id_usager")
    )

    fk_id_chambre: Mapped[UUID] = mapped_column(
        ForeignKey("chambre.id_chambre"),
        nullable=True
    )

    # Relation N à 1
    usager: Mapped["Usager"] = relationship(
        back_populates="reservations"
    )

    # Relation N à 1
    chambre: Mapped["Chambre"] = relationship(
        back_populates="reservations"
    )