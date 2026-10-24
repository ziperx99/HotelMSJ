# Modules et librairies
import unittest
from uuid import uuid4
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session
from modele.usager import Usager
from DTO.usager_dto import UsagerDTO
from metier.usager_metier import (
    creer_usager,
    get_usager_par_id,
)


# Configuration du moteur de base de données
engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+18+for+SQL+Server',
    connect_args={"TrustServerCertificate": "yes"},
    use_setinputsizes=False
)


class TestRechercherUsagerParId(unittest.TestCase):

    def test_rechercher_usager_par_id(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="TestPrenom",
            nom="TestNom",
            adresse="123 rue Test",
            mobile="514-555-9999",
            mot_de_passe="test123"
        )

        usagerCree = creer_usager(UsagerDTO(usager))

        usagerTrouve = get_usager_par_id(usagerCree.id_usager)

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


    def test_rechercher_usager_par_id_none(self):

        with self.assertRaises(ValueError):
            get_usager_par_id(None)


    def test_rechercher_usager_par_id_inexistant(self):

        with self.assertRaises(ValueError):
            get_usager_par_id(uuid4())


if __name__ == "__main__":
    unittest.main()