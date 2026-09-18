import unittest
from modele.chambre import Chambre
from modele.TypeChambre import TypeChambre
from metier.chambreMetier import creerChambre
from DTO.chambreDTO import ChambreDTO, TypeChambreDTO
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, delete, select
from uuid import uuid4, UUID

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

class test_creerChambre(unittest.TestCase):
    def test_creerChambre(self):
        chambreDTO = ChambreDTO(
                    Chambre(
                        id_chambre = uuid4(),
                        numero_chambre = 9000,
                        disponible_reservation = True,
                        autre_informations = None,
                        type_chambre = 
                            TypeChambre(
                                id_type_chambre = None,
                                nom_type = 'king', 
                                prix_plancher = 229.0,
                                prix_plafond = None,
                                description_chambre = None
                        )
                    )
                )

        chambreDTOCree = creerChambre(chambreDTO)

        self.assertEqual(chambreDTOCree.numero_chambre,9000)
        self.assertTrue(chambreDTOCree.disponible_reservation)
        #TODO: Ajouter des assertions pour tous les champs afin de s'assurer que le DTO a été
        #construit adéquatement et est complet.
        self.assertIsNone(chambreDTOCree.autre_informations)
        self.assertEqual(chambreDTOCree.type_chambre.nom_type, 'king')
        self.assertEqual(chambreDTOCree.type_chambre.prix_plancher, 229.0)
        self.assertIsNone(chambreDTOCree.type_chambre.prix_plafond)

        #TODO: Supprimer la chambre nouvellement créée:
        #importer create_engine et delete de SQLAlchemy. Créer une session et exécuter
        # un statement qui vient deleter la chambre nouvellement créé par le test précédent.
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

