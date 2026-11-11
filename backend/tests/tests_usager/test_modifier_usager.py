# Modules et librairies
import unittest
from uuid import uuid4
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session
from modele.usager import Usager
from DTO.usager_dto import UsagerDTO
from metier.usager_metier import (
    creer_usager,
    modifier_usager,
)


# Configuration du moteur de base de données
engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+18+for+SQL+Server',
    connect_args={"TrustServerCertificate": "yes"},
    use_setinputsizes=False
)


class TestModifierUsager(unittest.TestCase):

    def test_modifier_usager(self):

        # Créer l'usager
        usager = Usager(
            id_usager=uuid4(),
            prenom="TestPrenom",
            nom="TestNom",
            adresse="123 rue Test",
            mobile="514-555-9999",
            mot_de_passe="test123"
        )

        usagerCree = creer_usager(UsagerDTO(usager))

        # Modifier les informations
        usagerModifie = Usager(
            id_usager=usagerCree.id_usager,
            prenom="NouveauPrenom",
            nom="NouveauNom",
            adresse="456 rue Test",
            mobile="514-555-1111",
            mot_de_passe="nouveau123"
        )

        resultat = modifier_usager(UsagerDTO(usagerModifie))

        self.assertEqual(
            resultat.id_usager,
            usagerCree.id_usager
        )

        self.assertEqual(
            resultat.prenom,
            "NouveauPrenom"
        )

        self.assertEqual(
            resultat.nom,
            "NouveauNom"
        )

        self.assertEqual(
            resultat.adresse,
            "456 rue Test"
        )

        self.assertEqual(
            resultat.mobile.strip(),
            "514-555-1111"
        )

        self.assertEqual(
            resultat.mot_de_passe.strip(),
            "nouveau123"
        )

        # Nettoyer la BD
        with Session(engine) as session:

            stmt = delete(Usager).where(
                Usager.id_usager == usagerCree.id_usager
            )

            session.execute(stmt)
            session.commit()


    def test_modifier_usager_id_vide(self):

        usager = Usager(
            id_usager=None,
            prenom="TestPrenom",
            nom="TestNom",
            adresse="123 rue Test",
            mobile="514-555-9999",
            mot_de_passe="test123"
        )

        with self.assertRaises(ValueError):
            modifier_usager(UsagerDTO(usager))


    def test_modifier_usager_prenom_vide(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="",
            nom="TestNom",
            adresse="123 rue Test",
            mobile="514-555-9999",
            mot_de_passe="test123"
        )

        with self.assertRaises(ValueError):
            modifier_usager(UsagerDTO(usager))


    def test_modifier_usager_nom_vide(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="TestPrenom",
            nom="",
            adresse="123 rue Test",
            mobile="514-555-9999",
            mot_de_passe="test123"
        )

        with self.assertRaises(ValueError):
            modifier_usager(UsagerDTO(usager))


    def test_modifier_usager_adresse_vide(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="TestPrenom",
            nom="TestNom",
            adresse="",
            mobile="514-555-9999",
            mot_de_passe="test123"
        )

        with self.assertRaises(ValueError):
            modifier_usager(UsagerDTO(usager))


    def test_modifier_usager_mobile_vide(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="TestPrenom",
            nom="TestNom",
            adresse="123 rue Test",
            mobile="",
            mot_de_passe="test123"
        )

        with self.assertRaises(ValueError):
            modifier_usager(UsagerDTO(usager))


    def test_modifier_usager_mot_de_passe_vide(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="TestPrenom",
            nom="TestNom",
            adresse="123 rue Test",
            mobile="514-555-9999",
            mot_de_passe=""
        )

        with self.assertRaises(ValueError):
            modifier_usager(UsagerDTO(usager))


    def test_modifier_usager_inexistant(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="TestPrenom",
            nom="TestNom",
            adresse="123 rue Test",
            mobile="514-555-9999",
            mot_de_passe="test123"
        )

        with self.assertRaises(ValueError):
            modifier_usager(UsagerDTO(usager))


if __name__ == "__main__":
    unittest.main()