from typing import List, TYPE_CHECKING
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Mapped, relationship, mapped_column

from modele.chambre import Base

if TYPE_CHECKING:
    from modele.chambre import Chambre


class TypeChambre(Base):
    __tablename__ = "type_chambre"

    nom_type: Mapped[str]
    prix_plafond: Mapped[Decimal] = mapped_column(nullable=True)
    prix_plancher: Mapped[Decimal]
    description_chambre: Mapped[str] = mapped_column(nullable=True)

    id_type_chambre: Mapped[UUID] = mapped_column(primary_key=True)

    # Relation 1 à N
    chambres: Mapped[List["Chambre"]] = relationship(
        back_populates="type_chambre"
    )