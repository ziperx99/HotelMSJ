# Modules et librairies
import unittest
import logging
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from DTO.chambreDTO import ChambreDTO
from metier.chambreMetier import modifierChambre
from modele.chambre import Chambre
from modele.TypeChambre import TypeChambre
from uuid import uuid4

# Configuration de base
logging.basicConfig()
# Activation des logs SQLAlchemy
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Configuration du moteur de base de données
engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server',
    use_setinputsizes=False)


class TestChambre(unittest.TestCase):

    def test_modifierChambre(self):
    
        # Ouverture d'une session SQLAlchemy
        with Session(engine) as session:
            
            # Récupération de la chambre
            stmt = select(Chambre).where(Chambre.numero_chambre == 115)

            # Exécution de la requête
            chambre = session.execute(stmt).scalar_one()
            
            if chambre is None:
                raise ValueError("La chambre n'existe pas")
            
            # Sauvegarde de l'état initial
            ancienne_info = chambre.autre_informations
            ancienne_disponibilite = chambre.disponible_reservation

            # Création du DTO avec les informations de la chambre
            chambreDTO = ChambreDTO(chambre)

            # Modification des informations dans le DTO
            chambreDTO.autre_informations = "Chambre en rénovation"
            chambreDTO.disponible_reservation = False

            # Modification de la chambre avec la fonction métier
            modifierChambre(chambreDTO)

            # Relecture
            stmt = select(Chambre).where(Chambre.numero_chambre == 115)
            chambre_modifiee = session.execute(stmt).scalar_one()

            # Vérifications
            self.assertEqual(chambre_modifiee.autre_informations, "Chambre en rénovation")
            self.assertFalse(chambre_modifiee.disponible_reservation)

            # Nettoyage : retour aux données originales
            chambre_modifiee.autre_informations = ancienne_info
            chambre_modifiee.disponible_reservation = ancienne_disponibilite
            session.commit()

            # Vérification du nettoyage
            stmt = select(Chambre).where(Chambre.numero_chambre == 115)
            chambre_nettoyee = session.execute(stmt).scalar_one()
            
            # Vérification des champs modifiés
            self.assertEqual(chambre_nettoyee.autre_informations, ancienne_info)
            self.assertEqual(chambre_nettoyee.disponible_reservation, ancienne_disponibilite)
            
            
    def test_modifierChambreInexistante(self):
    
        # Création d'une chambre uniquement pour tester
        chambre = Chambre()

        # On donne volontairement un identifiant qui n'existe pas dans la BD
        chambre.id_chambre = uuid4()
        chambre.numero_chambre = 9999
        chambre.disponible_reservation = True
        chambre.autre_informations = "Test"

        # Récupération d'un type de chambre existant dans la BD
        with Session(engine) as session:
            stmt = select(TypeChambre)
            type_chambre = session.execute(stmt).scalars().first()
        
            if type_chambre is None:
                raise ValueError("Aucun type de chambre n'existe dans la BD")

        # Association du type de chambre à la chambre de test
        chambre.type_chambre = type_chambre

        # Création du DTO
        chambreDTO = ChambreDTO(chambre)

        # Vérifier que la modification d'une chambre inexistante déclenche une erreur
        with self.assertRaises(ValueError):
            modifierChambre(chambreDTO)