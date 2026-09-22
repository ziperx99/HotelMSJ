# Modules et librairies
import unittest
import logging
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from modele.usager import Usager
from decimal import Decimal

# Confirguration de base
logging.basicConfig()
# Activation des logs SQLAlchemy
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Configuration du moteur de base de données
engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server', 
    use_setinputsizes=False)


class TestUsager(unittest.TestCase):

    def test_getUsager(self):

        # Ouverture d'une session SQLAlchemy
        with Session(engine) as session:

            # Requête : chercher l'usager correspondant à l'inscription
            stmt = select(Usager).where(Usager.prenom == 'Sarah')
            usager = session.execute(stmt).scalar_one()

            # Vérification des champs simples
            self.assertEqual(usager.prenom, 'Sarah')
            self.assertEqual(usager.nom, 'Brooke')
            self.assertEqual(usager.adresse, '1234 Avenue Quelquechose')
            self.assertEqual(usager.mobile.strip(), '123-456-7890')
            self.assertEqual(usager.mot_de_passe.strip(), 'JEsuisunPW')
            self.assertEqual(str(usager.id_usager).upper(), '35455AFA-89A5-49E8-82EC-CDA2A441F1DA') 

            # Vérification de la relation avec Reservation
            self.assertEqual(len(usager.reservations),1)
            self.assertEqual(usager.reservations[0].info_reservation, 'Reservation test')
            self.assertEqual(usager.reservations[0].prix_jour, Decimal('199.99'))