import unittest
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import select
from modele.chambre import Chambre
from modele.TypeChambre import TypeChambre
from metier.chambreMetier import supprimerTypeChambre, engine

class TestSupprimerTypeChambre(unittest.TestCase):

    def test_supprimerTypeChambre(self):
        # Créer un type de chambre temporaire
        id_type = uuid4()

        with Session(engine) as session:
            type_chambre = TypeChambre(
                id_type_chambre = id_type,
                nom_type = "TestSuppression",
                prix_plancher = 100,
                prix_plafond = 200,
                description_chambre = "Type temporaire"
            )

            session.add(type_chambre)
            session.commit()

        try:
            # Supprimer le type de chambre
            supprimerTypeChambre(id_type)
            # Vérifier que y'existe plus
            with Session(engine) as session:
                resultat = session.execute(
                    select(TypeChambre).where(
                        TypeChambre.id_type_chambre == id_type
                    )
                ).scalar_one_or_none()
                self.assertIsNone(resultat)
        finally:
            # Nettoyage si le test échoue
            with Session(engine) as session:
                type_restant = session.get(TypeChambre, id_type)

                if type_restant is not None:
                    session.delete(type_restant)
                    session.commit()
    
    def test_supprimerTypeChambreIdNull(self):
        # Aucun ID fourni
        with self.assertRaises(ValueError):
            supprimerTypeChambre(None)
    
    def test_supprimerTypeChambreInexistant(self):
        # ID aléatoire inexistant
        id_inexistant = uuid4()
        with self.assertRaises(ValueError):
            supprimerTypeChambre(id_inexistant)
    
    def test_supprimerTypeChambreUtilise(self):
        # Créer un type de chambre et une chambre associée
        id_type = uuid4()
        id_chambre = uuid4()

        with Session(engine) as session:
            type_chambre = TypeChambre(
                id_type_chambre = id_type,
                nom_type = "TestTypeUtilise",
                prix_plancher = 150,
                prix_plafond = 250,
                description_chambre = "Type utilisé"
            )

            chambre = Chambre(
                id_chambre = id_chambre,
                numero_chambre = 9901,
                disponible_reservation = True,
                autre_informations = "Test",
                type_chambre = type_chambre
            )

            session.add(chambre)
            session.commit()
        
        try:
            # La suppression doit être refusée
            with self.assertRaises(ValueError):
                supprimerTypeChambre(id_type)
            # Vérifier que le type existe toujours
            with Session(engine) as session:
                resultat = session.get(TypeChambre, id_type)
                self.assertIsNotNone(resultat)
        finally:
            # Supprimer la chambre avant son type
            with Session(engine) as session:
                chambre = session.get(Chambre, id_chambre)

                if chambre is not None:
                    session.delete(chambre)
                    session.flush()
                type_chambre = session.get(TypeChambre, id_type)

                if type_chambre is not None:
                    session.delete(type_chambre)

                session.commit()