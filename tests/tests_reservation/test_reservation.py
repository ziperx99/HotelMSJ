import unittest
import logging

from datetime import datetime
from decimal import Decimal

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


class TestReservation(unittest.TestCase):

    def test_getReservation(self):

        with Session(engine) as session:

            stmt = select(Reservation).where(
                Reservation.info_reservation == 'Reservation test'
            )

            reservation = session.execute(stmt).scalar_one()

            # Tester tous les champs
            self.assertEqual(
                reservation.date_debut_reservation,
                datetime(2026, 10, 1)
            )

            self.assertEqual(
                reservation.date_fin_reservation,
                datetime(2026, 10, 5)
            )

            self.assertEqual(
                reservation.prix_jour,
                Decimal('199.99')
            )

            self.assertEqual(
                reservation.info_reservation,
                'Reservation test'
            )

            self.assertIsNotNone(
                reservation.id_reservation
            )

            self.assertEqual(
                str(reservation.fk_id_usager).upper(),
                '63E31298-1879-4856-8CB1-F57353271602'
            )

            self.assertEqual(
                str(reservation.fk_id_chambre).upper(),
                '44030EF8-3137-4CE2-8F7D-FA9D8A707F1C'
            )

            # Relation avec Usager
            self.assertEqual(
                reservation.usager.prenom,
                'Melissa'
            )

            self.assertEqual(
                reservation.usager.nom,
                'Test'
            )

            # Relation avec Chambre
            self.assertEqual(
                reservation.chambre.numero_chambre,
                243
            )

            # Chambre -> TypeChambre
            self.assertEqual(
                reservation.chambre.type_chambre.nom_type,
                'queen'
            )