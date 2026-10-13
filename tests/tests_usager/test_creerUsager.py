import unittest

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, delete

from modele.usager import Usager
from DTO.usagerDTO import UsagerDTO
from metier.usagerMetier import creerUsager
from uuid import uuid4


engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+18+for+SQL+Server',
    connect_args={
        "TrustServerCertificate": "yes"
    },
    use_setinputsizes=False
)


class test_creerUsager(unittest.TestCase):

    def test_creerUsager(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="TestPrenom",
            nom="TestNom",
            adresse="123 rue Test",
            mobile="514-555-9999",
            mot_de_passe="test123"
        )

        usagerDTO = UsagerDTO(usager)

        usagerDTOCree = creerUsager(usagerDTO)

        self.assertIsNotNone(
            usagerDTOCree.id_usager
        )

        self.assertEqual(
            usagerDTOCree.prenom,
            "TestPrenom"
        )

        self.assertEqual(
            usagerDTOCree.nom,
            "TestNom"
        )

        self.assertEqual(
            usagerDTOCree.adresse,
            "123 rue Test"
        )

        self.assertEqual(
            usagerDTOCree.mobile.strip(),
            "514-555-9999"
        )

        self.assertEqual(
            usagerDTOCree.mot_de_passe.strip(),
            "test123"
        )

        # Vérifier que l'usager est dans la BD
        with Session(engine) as session:

            stmt = select(Usager).where(
                Usager.id_usager == usagerDTOCree.id_usager
            )

            usagerBD = session.execute(
                stmt
            ).scalar_one_or_none()

            self.assertIsNotNone(usagerBD)

        # Nettoyer la BD
        with Session(engine) as session:

            stmt = delete(Usager).where(
                Usager.id_usager == usagerDTOCree.id_usager
            )

            session.execute(stmt)
            session.commit()


    def test_creerUsagerPrenomVide(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="",
            nom="TestNom",
            adresse="123 rue Test",
            mobile="514-555-9999",
            mot_de_passe="test123"
        )

        with self.assertRaises(ValueError):
            creerUsager(UsagerDTO(usager))


    def test_creerUsagerNomVide(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="TestPrenom",
            nom="",
            adresse="123 rue Test",
            mobile="514-555-9999",
            mot_de_passe="test123"
        )

        with self.assertRaises(ValueError):
            creerUsager(UsagerDTO(usager))


    def test_creerUsagerAdresseVide(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="TestPrenom",
            nom="TestNom",
            adresse="",
            mobile="514-555-9999",
            mot_de_passe="test123"
        )

        with self.assertRaises(ValueError):
            creerUsager(UsagerDTO(usager))


    def test_creerUsagerMobileVide(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="TestPrenom",
            nom="TestNom",
            adresse="123 rue Test",
            mobile="",
            mot_de_passe="test123"
        )

        with self.assertRaises(ValueError):
            creerUsager(UsagerDTO(usager))


    def test_creerUsagerMotDePasseVide(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="TestPrenom",
            nom="TestNom",
            adresse="123 rue Test",
            mobile="514-555-9999",
            mot_de_passe=""
        )

        with self.assertRaises(ValueError):
            creerUsager(UsagerDTO(usager))


if __name__ == "__main__":
    unittest.main()