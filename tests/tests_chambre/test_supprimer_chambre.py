# Modules et librairies
import unittest
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import Session
from modele.type_chambre import TypeChambre
from modele.chambre import Chambre
from metier.chambre_metier import engine, supprimerChambre


class TestSupprimerChambre(unittest.TestCase):

    def test_supprimerChambre(self):
        # On crée une chambre temporaire uniquement pour ce test
        # On utilise un type de chambre déjà présent dans la BD
        with Session(engine) as session:
            type_chambre = session.execute(select(TypeChambre)).scalars().first()
            self.assertIsNotNone(type_chambre)
            id_chambre = uuid4()

            chambre = Chambre(
                id_chambre = id_chambre,
                numero_chambre = 9001,
                disponible_reservation = True,
                autre_informations = "Test suppression",
                type_chambre = type_chambre
            )

            session.add(chambre)
            session.commit()
        
        try:
            # On appelle la méthode métier pour supprimer
            supprimerChambre(id_chambre)

            # On vérifie que la chambre n'existe plus
            with Session(engine) as session:
                chambre = session.get(Chambre, id_chambre)
                self.assertIsNone(chambre)
        finally:
            # Nettoyage de la BD si le test échoue
            with Session(engine) as session:
                chambre = session.get(Chambre, id_chambre)
                if chambre is not None:
                    session.delete(chambre)
                    session.commit()

    def test_supprimerChambreIdNull(self):
        # Une chambre ne peut pas être supprimée sans ID
        # On s'attend à une ValueError
        with self.assertRaises(ValueError):
            supprimerChambre(None)
    
    def test_supprimerChambreInexistante(self):
        # On génère un ID aléatoire
        # Il devrait pas être un ID existant dans la BD
        id_inexistant = uuid4()
        # On tente de supprimer une chambre qui n'existe pas. Doit déclencher un ValueError, si aucun valueerror, le test échoue
        with self.assertRaises(ValueError):
            supprimerChambre(id_inexistant)

    def test_supprimerChambreAvecReservation(self):
        # On cherche une chambre qui a une réservation
        # On ne crée pas et on modifie pas dans la BD
        with Session(engine) as session:
            chambres = session.execute(select(Chambre)).scalars().all()
            id_chambre = None
            
            # On regarde les chambres pour en avoir une avec réservation
            for chambre in chambres:
                if len(chambre.reservations) > 0:
                    id_chambre = chambre.id_chambre
                    break
        
        # Si aucune chambre avec réservation existe, on ignore le test
        if id_chambre is None:
            self.skipTest("Aucune chambre avec réservation dans la BD.")
        
        # On tente de supprimer la chambre et lever un ValueError
        with self.assertRaises(ValueError):
            supprimerChambre(id_chambre)
        # On vérifie que la chambre est toujours dans la BD
        with Session(engine) as session:
            chambre = session.get(Chambre, id_chambre)
            self.assertIsNotNone(chambre)