# Modules et librairies
import unittest
import logging
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from modele.typeChambre import TypeChambre

# Confirguration de base
logging.basicConfig()
# Activation des logs SQLAlchemy
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Configuration du moteur de base de données
engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server',
      use_setinputsizes=False)


class TestTypeChambre(unittest.TestCase):

    def test_getTypeChambre(self):

        # Ouverture d'une session SQLAlchemy
        with Session(engine) as session:

            # Requête : chercher le type de chambre correspondant à l'inscription
            stmt = select(TypeChambre).where(TypeChambre.nom_type == 'queen')
            type_chambre = session.execute(stmt).scalar_one()

            # Vérification des champs simples
            self.assertEqual(type_chambre.nom_type, 'queen')
            self.assertIsNotNone(type_chambre.id_type_chambre)
            self.assertIsNotNone(type_chambre.prix_plancher)

            # prix_plafond peut être NULL
            if type_chambre.prix_plafond is not None:
                self.assertGreaterEqual(type_chambre.prix_plafond, type_chambre.prix_plancher)

            # description_chambre peut être NULL
            if type_chambre.description_chambre is not None:
                self.assertIsInstance(type_chambre.description_chambre, str)

            # Relation avec Chambre
            self.assertIsNotNone(type_chambre.chambres)
            self.assertTrue(
                any(
                    chambre.numero_chambre == 243
                    for chambre in type_chambre.chambres))