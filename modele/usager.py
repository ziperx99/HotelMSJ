# Modules et librairies du modèle
from typing import TYPE_CHECKING
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from modele.chambre import Base
# Import conditionnel pour éviter les importations circulaires
if TYPE_CHECKING:
    from modele.reservation import Reservation


class Usager(Base):
    # Nom de la table dans la bd
    __tablename__ = "usager"

    # Définition des colonnes de la table
    id_usager: Mapped[UUID] = mapped_column(primary_key=True)
    prenom: Mapped[str]
    nom: Mapped[str]
    adresse: Mapped[str]
    mobile: Mapped[str]
    mot_de_passe: Mapped[str]

    # Relation 1 à N
    reservations: Mapped[list["Reservation"]] = relationship(back_populates="usager")