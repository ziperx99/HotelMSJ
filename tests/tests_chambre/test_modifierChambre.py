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

        id_chambre_test = None

        try:

            # Ouverture d'une session SQLAlchemy
            with Session(engine) as session:

                # Récupération d'un type de chambre valide
                type_chambre = session.execute(select(TypeChambre)).scalars().first()
                self.assertIsNotNone(type_chambre, "Aucun type de chambre dans la base.")

                # Création d'une chambre de test
                chambre = Chambre(
                    id_chambre=uuid4(),
                    numero_chambre=9999,
                    disponible_reservation=True,
                    autre_informations="Test",
                    type_chambre=type_chambre
                )

                session.add(chambre)
                session.commit()

                id_chambre_test = chambre.id_chambre

                # Création du DTO
                chambreDTO = ChambreDTO(chambre)

                # Modifications à tester
                chambreDTO.autre_informations = "Chambre en rénovation"
                chambreDTO.disponible_reservation = False

                # Fonction métier
                modifierChambre(chambreDTO)

                # On vide le cache SQLAlchemy
                session.expire_all()

                # Relecture
                chambre_modifiee = session.execute(
                    select(Chambre).where(Chambre.id_chambre == id_chambre_test)).scalars().one()

                # Vérifications
                self.assertEqual(chambre_modifiee.autre_informations,"Chambre en rénovation")
                self.assertFalse(chambre_modifiee.disponible_reservation)

        finally:

            # Nettoyage garanti même en cas d'échec
            if id_chambre_test is not None:

                # Ouverture d'une session SQLAlchemy
                with Session(engine) as session:

                    chambre_test = session.execute(
                        select(Chambre).where(Chambre.id_chambre == id_chambre_test)).scalars().one_or_none()

                    if chambre_test is not None:
                        session.delete(chambre_test)
                        session.commit()
                        
                        

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