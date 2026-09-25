# Modules et librairies
import unittest
import logging
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from modele.chambre import Chambre

# Confirguration de base
logging.basicConfig()
# Activation des logs SQLAlchemy
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Configuration du moteur de base de données
engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server',
      use_setinputsizes=False)


class TestChambre(unittest.TestCase):
    
    def test_getChambreParNumero(self):
        
        # Ouverture d'une session SQLAlchemy
        with Session(engine) as session:
            
            # Requête : chercher la chambre correspondant au numéro
            stmt = select(Chambre).where(Chambre.numero_chambre == 115)
            chambre = session.execute(stmt).scalar_one()
            
            # Vérification des champs simples
            self.assertEqual(chambre.numero_chambre, 115)
            self.assertIsNone(chambre.autre_informations)
            self.assertTrue(chambre.disponible_reservation)
            self.assertEqual(str(chambre.id_chambre).upper(),'8CC1969D-38D8-469B-A5CE-043807402F2F')
            self.assertIsNotNone(chambre.fk_type_chambre)
            
            # Vérification de la relation avec TypeChambre
            self.assertEqual(chambre.type_chambre.nom_type,'queen')

            # Vérification de la relation avec Reservation
            self.assertEqual(len(chambre.reservations), 1)
            self.assertEqual(chambre.reservations[0].info_reservation, 'Reservation test')