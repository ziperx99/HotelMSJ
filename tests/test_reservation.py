# Modules et librairies
import unittest
import logging
from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from modele.reservation import Reservation

# Confirguration de base
logging.basicConfig()
# Activation des logs SQLAlchemy
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Configuration du moteur de base de données
engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server',
      use_setinputsizes=False)


class TestReservation(unittest.TestCase):
    
    def test_getReservationParId(self):
        
        # Ouverture d'une session SQLAlchemy
        with Session(engine) as session:
            
            # Requête : chercher la réservation correspondant à l'inscription
            stmt = select(Reservation).where(Reservation.info_reservation == 'Reservation test')
            reservation = session.execute(stmt).scalar_one()
            
            # Vérification des champs simples
            self.assertEqual(reservation.date_debut_reservation, datetime(2026, 10, 1))
            self.assertEqual(reservation.date_fin_reservation, datetime(2026, 10, 5))
            self.assertEqual(reservation.prix_jour, Decimal('199.99'))
            self.assertEqual(reservation.info_reservation, 'Reservation test')
            self.assertIsNotNone(reservation.id_reservation)
            self.assertEqual(str(reservation.fk_id_usager).upper(), '35455AFA-89A5-49E8-82EC-CDA2A441F1DA')
            self.assertEqual(str(reservation.fk_id_chambre).upper(), '8CC1969D-38D8-469B-A5CE-043807402F2F')

            # Vérification de la relation avec Usager
            self.assertEqual(reservation.usager.prenom, 'Sarah')
            self.assertEqual(reservation.usager.nom,'Brooke')

            # Vérification de la relation avec Chambre
            assert reservation.chambre is not None
            self.assertEqual(reservation.chambre.numero_chambre, 115)

            # Vérification de la relation entre Chambre et TypeChambre
            self.assertEqual(reservation.chambre.type_chambre.nom_type, 'queen')