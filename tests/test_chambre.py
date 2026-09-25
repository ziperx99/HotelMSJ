import unittest
import logging

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

from modele.chambre import Chambre
from modele.TypeChambre import TypeChambre
from modele.usager import Usager
from modele.reservation import Reservation


logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server',
    use_setinputsizes=False
)


class TestChambre(unittest.TestCase):

    def test_getChambreParNumero(self):

        with Session(engine) as session:

            stmt = select(Chambre).where(
                Chambre.numero_chambre == 243
            )

            chambre = session.execute(stmt).scalar_one()

            # Tester tous les champs
            self.assertEqual(chambre.numero_chambre, 243)
            self.assertIsNone(chambre.autre_informations)
            self.assertTrue(chambre.disponible_reservation)

            self.assertEqual(
                str(chambre.id_chambre).upper(),
                '44030EF8-3137-4CE2-8F7D-FA9D8A707F1C'
            )

            self.assertIsNotNone(chambre.fk_type_chambre)

            # Relation avec TypeChambre
            self.assertEqual(
                chambre.type_chambre.nom_type,
                'queen'
            )

            # Relation avec Reservation
            self.assertEqual(
                len(chambre.reservations),
                1
            )

            self.assertEqual(
                chambre.reservations[0].info_reservation,
                'Reservation test'
            )