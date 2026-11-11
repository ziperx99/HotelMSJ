# Modules et librairies
import logging
import unittest
from datetime import datetime
from uuid import uuid4
from pydantic import ValidationError
from sqlalchemy import create_engine, delete, select
from sqlalchemy.orm import Session
from modele.type_chambre import TypeChambre
from modele.chambre import Chambre
from DTO.chambre_dto import ChambreDTO
from metier.chambre_metier import creer_chambre


# Configuration de base
logging.basicConfig()
# Activation des logs SQLAlchemy
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Configuration du moteur de base de données
engine = create_engine(
    'mssql+pyodbc://localhost\SQLEXPRESS/Hotel?driver=ODBC+Driver+18+for+SQL+Server',
    connect_args={"TrustServerCertificate": "yes"},
    use_setinputsizes=False
)


class TestCreerChambre(unittest.TestCase):
    def test_creer_chambre(self):
        chambreDTO = ChambreDTO(
                    Chambre(
                        id_chambre = uuid4(),
                        numero_chambre = 9000,
                        disponible_reservation = True,
                        autre_informations = None,
                        type_chambre = 
                            TypeChambre(
                                id_type_chambre = uuid4(),
                                nom_type = 'king', 
                                prix_plancher = 179.0,
                                prix_plafond = 299.0,
                                description_chambre = None
                        )
                    )
                )

        chambreDTOCree = creer_chambre(chambreDTO)

        self.assertEqual(chambreDTOCree.numero_chambre,9000)
        self.assertTrue(chambreDTOCree.disponible_reservation)
        self.assertIsNone(chambreDTOCree.autre_informations)
        self.assertEqual(chambreDTOCree.type_chambre.nom_type, 'king')
        self.assertEqual(chambreDTOCree.type_chambre.prix_plancher, 179.0)
        self.assertEqual(chambreDTOCree.type_chambre.prix_plafond, 299.0)

        #Supprimer la chambre nouvellement créée:
        #importer create_engine et delete de SQLAlchemy. Créer une session et exécuter
        #un statement qui vient deleter la chambre nouvellement créé par le test précédent.
        with Session(engine) as session:
            stmt = select(Chambre).where(Chambre.numero_chambre == 9000)
            chambre = session.execute(stmt).scalar_one_or_none()
            self.assertIsNotNone(chambre)
            session.close()

        with Session(engine) as session:       
            stmt2 = delete(Chambre).where(Chambre.numero_chambre == 9000)
            session.execute(stmt2)
            session.commit()
            session.close()


    def test_creer_chambre_sans_numero(self):
        
        with self.assertRaises(ValidationError):

            ChambreDTO(
                Chambre(
                    id_chambre = uuid4(),
                    numero_chambre = None,
                    disponible_reservation = True,
                    autre_informations = None,
                    type_chambre = 
                        TypeChambre(
                            id_type_chambre = uuid4(),
                            nom_type = 'king', 
                            prix_plancher = 179.0,
                            prix_plafond = 299.0,
                            description_chambre = None
                    )
                )
            )

    def test_creer_chambre_sans_disponibilite(self):
            
        with self.assertRaises(ValidationError):

            ChambreDTO(
                Chambre(
                    id_chambre = uuid4(),
                    numero_chambre = 9400,
                    disponible_reservation = None,
                    autre_informations = None,
                    type_chambre = 
                        TypeChambre(
                            id_type_chambre = uuid4(),
                            nom_type = 'king', 
                            prix_plancher = 179.0,
                            prix_plafond = 299.0,
                            description_chambre = None
                    )
                )
            )

    def test_creer_chambre_sans_id(self):
            
        with self.assertRaises(ValidationError):

            ChambreDTO(
                Chambre(
                    id_chambre = None,
                    numero_chambre = 9400,
                    disponible_reservation = True,
                    autre_informations = None,
                    type_chambre = 
                        TypeChambre(
                            id_type_chambre = uuid4(),
                            nom_type = 'king', 
                            prix_plancher = 179.0,
                            prix_plafond = 299.0,
                            description_chambre = None
                    )
                )
            )

    def test_creer_chambre_info_mauvais_type(self):
            
        with self.assertRaises(ValidationError):

            ChambreDTO(
                Chambre(
                    id_chambre = uuid4(),
                    numero_chambre = 9400,
                    disponible_reservation = True,
                    autre_informations = datetime.now(),
                    type_chambre = 
                        TypeChambre(
                            id_type_chambre = uuid4(),
                            nom_type = 'king', 
                            prix_plancher = 179.0,
                            prix_plafond = 299.0,
                            description_chambre = None
                    )
                )
            )