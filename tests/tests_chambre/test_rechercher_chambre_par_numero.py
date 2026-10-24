# Modules et librairies
import logging
import unittest
from uuid import uuid4
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from modele.type_chambre import TypeChambre
from modele.chambre import Chambre


# Configuration de base
logging.basicConfig()
# Activation des logs SQLAlchemy
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Configuration du moteur de base de données
engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server',
      use_setinputsizes=False
)


class TestChambre(unittest.TestCase):

    def test_getChambreParNumero(self):

        id_chambre_test = None

        try:

        # Ouverture d'une session SQLAlchemy
            with Session(engine) as session:

                # Récupérer un type de chambre valide
                type_chambre = session.execute(select(TypeChambre)).scalars().first()

                if type_chambre is None:
                    self.fail("Aucun type de chambre disponible pour le test.")

                # Création d'une chambre de test
                chambre_test = Chambre(
                    id_chambre=uuid4(),
                    numero_chambre=9999,
                    disponible_reservation=True,
                    autre_informations=None,
                    type_chambre=type_chambre
                )

                session.add(chambre_test)
                session.commit()

                id_chambre_test = chambre_test.id_chambre

                # Recherche de la chambre par numéro
                stmt = select(Chambre).where(Chambre.numero_chambre == 9999)

                chambre = session.execute(stmt).scalar_one()

                # Vérification des champs simples
                self.assertEqual(chambre.numero_chambre, 9999)
                self.assertIsNone(chambre.autre_informations)
                self.assertTrue(chambre.disponible_reservation)

                # Vérification de l'identifiant
                self.assertEqual(chambre.id_chambre, id_chambre_test)

                # Vérification de la clé étrangère
                self.assertIsNotNone(chambre.fk_type_chambre)

                # Vérification de la relation TypeChambre
                self.assertEqual(chambre.type_chambre.id_type_chambre, type_chambre.id_type_chambre)
                self.assertEqual(chambre.type_chambre.nom_type, type_chambre.nom_type)

        finally:

            # Nettoyage garanti même si le test échoue
            if id_chambre_test is not None:

                # Ouverture d'une session SQLAlchemy
                with Session(engine) as session:

                    chambre = session.execute(select(Chambre).where(Chambre.id_chambre == id_chambre_test)).scalars().one_or_none()

                    if chambre is not None:
                        session.delete(chambre)
                        session.commit()