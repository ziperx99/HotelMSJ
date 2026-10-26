# Modules et librairies
import unittest
from uuid import uuid4
from sqlalchemy.orm import Session
from modele.type_chambre import TypeChambre
from DTO.chambre_dto import TypeChambreDTO
from metier.chambre_metier import engine, rechercher_type_chambre


class TestRechercherTypeChambre(unittest.TestCase):

    # Vérifier qu'on peut rechercher un type de chambre existant
    def test_rechercher_type_chambre_existant(self):
        id_type = uuid4()

        # Créer un type temporaire pour le test
        with Session(engine) as session:
            typeChambre = TypeChambre(
                id_type_chambre = id_type,
                nom_type = "TestRecherche",
                prix_plancher = 100,
                prix_plafond = 200,
                description_chambre = "Type de chambre pour test"
            )

            session.add(typeChambre)
            session.commit()
        
        try:
            # Rechercher le type créé
            resultat = rechercher_type_chambre(id_type)
            self.assertIsInstance(resultat, TypeChambreDTO)
            self.assertEqual(resultat.id_type_chambre, id_type)
            self.assertEqual(resultat.nom_type, "TestRecherche")

        finally:
            # Supprimer les données temporaires
            with Session(engine) as session:
                typeChambre = session.get(TypeChambre, id_type)

                if typeChambre is not None:
                    session.delete(typeChambre)
                    session.commit()
    
    # Vérifier qu'un identifiant manquant est refusé
    def test_rechercher_type_chambre_sans_id(self):
        with self.assertRaises(ValueError):
            rechercher_type_chambre(None)

    def test_rechercher_type_chambre_invalide(self):
        with self.assertRaises(ValueError):
            rechercher_type_chambre("identifiant_invalide")