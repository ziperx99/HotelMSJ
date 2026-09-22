# Modules et librairies du modèle
from typing import TYPE_CHECKING
from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# Imports conditionnels pour éviter les importations circulaires
if TYPE_CHECKING:
    from modele.typeChambre import TypeChambre
    from modele.reservation import Reservation


class Base(DeclarativeBase):
    pass


class Chambre(Base):
    # Nom de la table dans la bd
    __tablename__ = "chambre"

    # Définition des colonnes de la table
    id_chambre: Mapped[UUID] = mapped_column(primary_key=True)
    numero_chambre: Mapped[int]
    disponible_reservation: Mapped[bool]
    autre_informations: Mapped[str] = mapped_column(nullable=True)

    # Identification des clés étrangères
    fk_type_chambre: Mapped[UUID] = mapped_column(ForeignKey("type_chambre.id_type_chambre"), nullable=True)

    # Relation N à 1
    type_chambre: Mapped["TypeChambre"] = relationship(back_populates="chambres")

    # Relation 1 à N
    reservations: Mapped[list["Reservation"]] = relationship(back_populates="chambre")