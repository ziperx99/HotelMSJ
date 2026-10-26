# Modules et librairies
import unittest
from uuid import uuid4
from pydantic import field_validator
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session
from modele.usager import Usager
from modele.type_chambre import TypeChambre
from DTO.usager_dto import UsagerDTO
from metier.usager_metier import (
    creer_usager,
    get_usager_par_id,
    supprimer_usager,
)


# Configuration du moteur de base de données
engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+18+for+SQL+Server',
    connect_args={"TrustServerCertificate": "yes"},
    use_setinputsizes=False
)


class TestSupprimerUsager(unittest.TestCase):

    def test_supprimer_usager(self):

        # Création d'un usager de test
        usager = Usager(
            id_usager=uuid4(),
            prenom="TestPrenom",
            nom="TestNom",
            adresse="123 rue Test",
            mobile="514-555-9999",
            mot_de_passe="test123"
        )

        # Création de l'usager dans la base de données
        usagerCree = creer_usager(UsagerDTO(usager))

        try:

            # Fonction métier
            supprimer_usager(usagerCree.id_usager)

            # Vérification que l'usager n'existe plus dans la base de données
            with self.assertRaises(ValueError):
                get_usager_par_id(usagerCree.id_usager)

        finally:

            # Nettoyage de la base de données au cas où la suppression aurait échoué
            with Session(engine) as session:

                # Recherche de l'usager de test
                stmt = delete(Usager).where(Usager.id_usager == usagerCree.id_usager)

                # Suppression de l'usager de test
                session.execute(stmt)

                # Sauvegarde des modifications dans la base de données
                session.commit()


    def test_supprimer_usager_id_null(self):

        # Vérification qu'un identifiant nul déclenche une erreur
        with self.assertRaises(ValueError):
            supprimer_usager(None)


    def test_supprimer_usager_inexistant(self):

        # Création d'un identifiant qui n'existe pas dans la base de données
        id_inexistant = uuid4()

        # Vérification que la suppression d'un usager inexistant déclenche une erreur
        with self.assertRaises(ValueError):
            supprimer_usager(id_inexistant)