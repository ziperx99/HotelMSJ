# Modules et librairies
from decimal import Decimal
from typing import TYPE_CHECKING, List
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
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