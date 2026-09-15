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


class TestTypeChambre(unittest.TestCase):

    def test_getTypeChambre(self):

        with Session(engine) as session:

            stmt = select(TypeChambre).where(
                TypeChambre.nom_type == 'queen'
            )

            type_chambre = session.execute(stmt).scalar_one()

            # Tester tous les champs
            self.assertEqual(
                type_chambre.nom_type,
                'queen'
            )

            self.assertIsNotNone(
                type_chambre.id_type_chambre
            )

            self.assertIsNotNone(
                type_chambre.prix_plancher
            )

            # prix_plafond peut être NULL
            if type_chambre.prix_plafond is not None:
                self.assertGreaterEqual(
                    type_chambre.prix_plafond,
                    type_chambre.prix_plancher
                )

            # description_chambre peut être NULL
            if type_chambre.description_chambre is not None:
                self.assertIsInstance(
                    type_chambre.description_chambre,
                    str
                )

            # Relation avec Chambre
            self.assertIsNotNone(
                type_chambre.chambres
            )

            self.assertTrue(
                any(
                    chambre.numero_chambre == 243
                    for chambre in type_chambre.chambres
                )
            )