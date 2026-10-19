import unittest
from modele.TypeChambre import TypeChambre
from metier.chambreMetier import creerTypeChambre
from DTO.chambreDTO import TypeChambreDTO
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, delete, select
from uuid import uuid4, UUID
from pydantic import ValidationError

import logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

engine = create_engine(
    'mssql+pyodbc://localhost\SQLEXPRESS/Hotel?driver=ODBC+Driver+18+for+SQL+Server',
    connect_args=
        {
            "TrustServerCertificate": "yes"
        },
    use_setinputsizes=False)

class test_creerTypeChambre(unittest.TestCase):
    def test_creerTypeChambre(self):
        TypeChambreDTO = TypeChambre(
                            id_type_chambre = None,
                            nom_type = 'Test', 
                            prix_plancher = 229.0,
                            prix_plafond = None,
                            description_chambre = "Test unitaire"
                        )
                    
        typeChambreDTOCree = creerTypeChambre(TypeChambreDTO)

        self.assertIsNotNone(typeChambreDTOCree.id_type_chambre)
        self.assertIsInstance(typeChambreDTOCree.id_type_chambre, UUID)
        self.assertEqual(typeChambreDTOCree.nom_type, 'Test')
        self.assertEqual(typeChambreDTOCree.prix_plancher, 229.0)
        self.assertIsNone(typeChambreDTOCree.prix_plafond)
        self.assertEqual(typeChambreDTOCree.description_chambre, 'Test unitaire')

        #Supprimer la chambre nouvellement créée:
        #importer create_engine et delete de SQLAlchemy. Créer une session et exécuter
        # un statement qui vient deleter la chambre nouvellement créé par le test précédent.
        with Session(engine) as session:
            stmt = select(TypeChambre).where(TypeChambre.description_chambre == 'Test unitaire')
            typeChambre = session.execute(stmt).scalar_one_or_none()
            self.assertIsNotNone(typeChambre)
            session.close()

        with Session(engine) as session:       
            stmt2 = delete(TypeChambre).where(TypeChambre.description_chambre == 'Test unitaire')
            session.execute(stmt2)
            session.commit()
            session.close()

    def test_creerTypeChambreSansId(self):
            
        with self.assertRaises(ValidationError):
            TypeChambreDTO(
                TypeChambre(
                    id_type_chambre = None,
                    nom_type = 'Test', 
                    prix_plancher = 229.0,
                    prix_plafond = None,
                    description_chambre = "Test unitaire"
                )
            )

    def test_creerTypeChambreSansNom(self):
            
        with self.assertRaises(ValidationError):
            TypeChambreDTO(
                TypeChambre(
                    id_type_chambre = uuid4(),
                    nom_type = None, 
                    prix_plancher = 229.0,
                    prix_plafond = None,
                    description_chambre = "Test unitaire"
                )
            )

    def test_creerTypeChambreSansPrixPlancher(self):
            
        with self.assertRaises(ValidationError):
            TypeChambreDTO(
                TypeChambre(
                    id_type_chambre = uuid4(),
                    nom_type = 'Test', 
                    prix_plancher = None,
                    prix_plafond = 300,
                    description_chambre = "Test unitaire"
                )
            )

    def test_creerTypeChambrePrixPlancherSuperieurPrixPlafond(self):
            
        with self.assertRaises(ValueError):
            TypeChambreDTO(
                TypeChambre(
                    id_type_chambre = uuid4(),
                    nom_type = 'Test', 
                    prix_plancher = 300,
                    prix_plafond = 200,
                    description_chambre = "Test unitaire"
                )
            )