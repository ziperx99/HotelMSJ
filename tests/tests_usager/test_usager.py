import unittest
import logging

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

from modele.chambre import Chambre
from modele.TypeChambre import TypeChambre
from modele.usager import Usager
from modele.reservation import Reservation
from decimal import Decimal


logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server',
    use_setinputsizes=False
)


class TestUsager(unittest.TestCase):

    def test_getUsager(self):

        with Session(engine) as session:

            stmt = select(Usager).where(
                Usager.prenom == 'Melissa'
            )

            usager = session.execute(stmt).scalar_one()

            # Tester tous les champs
            self.assertEqual(
                usager.prenom,
                'Melissa'
            )

            self.assertEqual(
                usager.nom,
                'Test'
            )

            self.assertEqual(
                usager.adresse,
                '123 rue Test'
            )

            self.assertEqual(
                usager.mobile.strip(),
                '514-555-1234'
            )

            self.assertEqual(
                usager.mot_de_passe.strip(),
                'test123'
            )

            self.assertEqual(
                str(usager.id_usager).upper(),
                '63E31298-1879-4856-8CB1-F57353271602'
            )

            # Relation avec Reservation
            self.assertEqual(
                len(usager.reservations),
                1
            )

            self.assertEqual(
                usager.reservations[0].info_reservation,
                'Reservation test'
            )

            self.assertEqual(
                usager.reservations[0].prix_jour,
                Decimal('199.99')
            )