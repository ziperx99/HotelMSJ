import unittest

from uuid import uuid4

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, delete

from modele.usager import Usager
from DTO.usagerDTO import UsagerDTO

from metier.usagerMetier import (
    creerUsager,
    getUsagerParId
)


engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+18+for+SQL+Server',
    connect_args={
        "TrustServerCertificate": "yes"
    },
    use_setinputsizes=False
)


class test_getUsagerParId(unittest.TestCase):

    def test_getUsagerParId(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="TestPrenom",
            nom="TestNom",
            adresse="123 rue Test",
            mobile="514-555-9999",
            mot_de_passe="test123"
        )

        usagerCree = creerUsager(
            UsagerDTO(usager)
        )

        usagerTrouve = getUsagerParId(
            usagerCree.id_usager
        )

        self.assertEqual(
            usagerTrouve.id_usager,
            usagerCree.id_usager
        )

        self.assertEqual(
            usagerTrouve.prenom,
            "TestPrenom"
        )

        self.assertEqual(
            usagerTrouve.nom,
            "TestNom"
        )

        self.assertEqual(
            usagerTrouve.adresse,
            "123 rue Test"
        )

        self.assertEqual(
            usagerTrouve.mobile.strip(),
            "514-555-9999"
        )

        self.assertEqual(
            usagerTrouve.mot_de_passe.strip(),
            "test123"
        )

        # Nettoyer la BD
        with Session(engine) as session:

            stmt = delete(Usager).where(
                Usager.id_usager == usagerCree.id_usager
            )

            session.execute(stmt)
            session.commit()


    def test_getUsagerParIdNone(self):

        with self.assertRaises(ValueError):
            getUsagerParId(None)


    def test_getUsagerParIdInexistant(self):

        with self.assertRaises(ValueError):
            getUsagerParId(uuid4())


if __name__ == "__main__":
    unittest.main()