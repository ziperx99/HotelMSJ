# Modules et librairies du modèle
from typing import TYPE_CHECKING
from decimal import Decimal
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from modele.chambre import Base
# Import conditionnel pour éviter les importations circulaires
if TYPE_CHECKING:
    from modele.chambre import Chambre


class TypeChambre(Base):
    # Nom de la table dans la bd
    __tablename__ = "type_chambre"

    # Définition des colonnes de la table
    id_type_chambre: Mapped[UUID] = mapped_column(primary_key=True)
    nom_type: Mapped[str]
    prix_plafond: Mapped[Decimal] = mapped_column(nullable=True)
    prix_plancher: Mapped[Decimal]
    description_chambre: Mapped[str] = mapped_column(nullable=True)

    # Relation 1 à N
    chambres: Mapped[list["Chambre"]] = relationship(back_populates="type_chambre")