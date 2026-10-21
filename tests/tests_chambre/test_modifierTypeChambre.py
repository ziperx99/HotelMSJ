import unittest
from uuid import uuid4
from sqlalchemy.orm import Session
from pydantic import ValidationError
from metier.chambreMetier import modifierTypeChambre, engine
from modele.TypeChambre import TypeChambre
from DTO.chambreDTO import TypeChambreDTO

class TestModifierTypeChambre(unittest.TestCase):
    # Créer un type de chambre temporaire dans la BD
    def setUp(self):
        self.id_type = uuid4()

        with Session(engine) as session:
            typeChambre = TypeChambre(
                id_type_chambre = self.id_type,
                nom_type = "TestModification",
                prix_plancher = 100,
                prix_plafond = 200,
                description_chambre = "Type de chambre temporaire"
            )

            session.add(typeChambre)
            session.commit()
    
    # Supprimer le type temporaire après chaque test
    def tearDown(self):
        with Session(engine) as session:
            typeChambre = session.get(TypeChambre, self.id_type)

            if typeChambre is not None:
                session.delete(typeChambre)
                session.commit()
    
    # Créer un DTO à partir d'un modèle SQLAlchemy
    def creerDTO(self, id_type = None, nom = "TestModifie", prix_plancher = 120, prix_plafond = 250):
        typeChambre = TypeChambre(
            id_type_chambre = id_type if id_type is not None else self.id_type,
            nom_type = nom,
            prix_plancher = prix_plancher,
            prix_plafond = prix_plafond,
            description_chambre = "Description modifiée"
        )

        return TypeChambreDTO(typeChambre)
    
    # Vérifier qu'on peut modifier un type existant
    def test_modifierTypeChambreValide(self):
        dto = self.creerDTO()
        resultat = modifierTypeChambre(dto)

        self.assertIsInstance(resultat, TypeChambreDTO)
        self.assertEqual(resultat.nom_type, "TestModifie")
        self.assertEqual(resultat.prix_plancher, 120)
        self.assertEqual(resultat.prix_plafond, 250)

        # Vérifier que les changements sont enregistrés dans la BD
        with Session(engine) as session:
            typeChambre = session.get(TypeChambre, self.id_type)
            self.assertEqual(typeChambre.nom_type, "TestModifie")
            self.assertEqual(typeChambre.prix_plancher, 120)
            self.assertEqual(typeChambre.prix_plafond, 250)

    # Vérifier qu'un type inexistant est refusé
    def test_modifierTypeChambreInexistant(self):
        dto = self.creerDTO(id_type = uuid4())
        with self.assertRaises(ValueError):
            modifierTypeChambre(dto)
    
    # Vérifier qu'un identifiant manquant est refusé
    def test_modifierTypeChambreSansId(self):
        dto = self.creerDTO()

        # model_copy permet de tester la validation métier sans repasser par le constructeur pydantic
        dto = dto.model_copy(update={"id_type_chambre": None})
        with self.assertRaises(ValueError):
            modifierTypeChambre(dto)
    
    # Vérifier qu'un nom vide est refusé
    def test_modifierTypeChambreNomVide(self):
        dto = self.creerDTO(nom="")
        with self.assertRaises(ValueError):
            modifierTypeChambre(dto)
    
    # Vérifier qu'un prix plafond inférieur au plancher est refusé
    # Peut-être too much vu qu'on l'a déjà dans test_typeChambre.py et test_creerTypeChambre.py ?
    def test_modifierTypeChambrePrixInvalides(self):
        typeChambre = TypeChambre(
            id_type_chambre = self.id_type,
            nom_type = "TestPrix",
            prix_plancher = 300,
            prix_plafond = 100,
            description_chambre = "Prix invalides"
        )

        # Le DTO doit refuser ces prix avant la modification
        with self.assertRaises(ValidationError):
            TypeChambreDTO(typeChambre)

    # Vérifier qu'on peut modifier un type sans prix plafond
    def test_modifierTypeChambreSansPrixPlafond(self):
        dto = self.creerDTO(prix_plafond = None)
        resultat = modifierTypeChambre(dto)
        self.assertIsNone(resultat.prix_plafond)
        self.assertEqual(resultat.prix_plancher, 120)
        
        with Session(engine) as session:
            typeChambre = session.get(TypeChambre, self.id_type)
            self.assertIsNone(typeChambre.prix_plafond)

if __name__ == "__main__":
    unittest.main()