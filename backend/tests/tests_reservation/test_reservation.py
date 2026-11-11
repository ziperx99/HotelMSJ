# Modules et librairies
import logging
import unittest
from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from pydantic import ValidationError
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from modele.type_chambre import TypeChambre
from modele.chambre import Chambre
from modele.reservation import Reservation
from modele.usager import Usager
from DTO.reservation_dto import ReservationDTO


# Configuration de base
logging.basicConfig()
# Activation des logs SQLAlchemy
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Configuration du moteur de base de données
engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server',
    use_setinputsizes=False
)


class TestReservation(unittest.TestCase):

    def test_rechercher_reservation(self):
        # Tester la récupération d'une réservation dans la BD
        with Session(engine) as session:
            stmt = select(Reservation).where(
                Reservation.info_reservation == 'Reservation test'
            )
            reservation = session.execute(stmt).scalar_one()

            # Tester tous les champs
            self.assertEqual(
                reservation.date_debut_reservation,
                datetime(2026, 10, 1)
            )
            self.assertEqual(
                reservation.date_fin_reservation,
                datetime(2026, 10, 5)
            )
            self.assertEqual(
                reservation.prix_jour,
                Decimal('199.99')
            )
            self.assertEqual(
                reservation.info_reservation,
                'Reservation test'
            )
            self.assertIsNotNone(
                reservation.id_reservation
            )
            self.assertEqual(
                str(reservation.fk_id_usager).upper(),
                '63E31298-1879-4856-8CB1-F57353271602'
            )
            self.assertEqual(
                str(reservation.fk_id_chambre).upper(),
                '44030EF8-3137-4CE2-8F7D-FA9D8A707F1C'
            )
            # Relation avec Usager
            self.assertEqual(
                reservation.usager.prenom,
                'Melissa'
            )
            self.assertEqual(
                reservation.usager.nom,
                'Test'
            )
            # Relation avec Chambre
            self.assertEqual(
                reservation.chambre.numero_chambre,
                243
            )
            # Chambre -> TypeChambre
            self.assertEqual(
                reservation.chambre.type_chambre.nom_type,
                'queen'
            )

    # Vérifier que la date de fin est après la date de début
    def test_validation_dates_valides(self):
        reservation = ReservationDTO.model_construct(
            id_reservation = uuid4(),
            date_debut_reservation = datetime(2034, 9, 11),
            date_fin_reservation = datetime(2034, 9, 15),
            prix_jour = 150,
            info_reservation = None,
            usager = None,
            chambre = None
        )

        reservation.verifier_date_fin_ulterieure()

        self.assertLess(
            reservation.date_debut_reservation,
            reservation.date_fin_reservation
        )

    # Vérifier qu'une date de fin antérieure est refusée
    def test_validation_date_fin_avant_debut(self):
        reservation = ReservationDTO.model_construct(
            id_reservation = uuid4(),
            date_debut_reservation = datetime(2034, 9, 15),
            date_fin_reservation = datetime(2034, 9, 11),
            prix_jour = 150,
            info_reservation = None,
            usager = None,
            chambre = None
        )

        with self.assertRaises(ValueError):
            reservation.verifier_date_fin_ulterieure()

    # Vérifier que deux dates identiques sont refusées
    def test_validation_dates_identiques(self):
        reservation = ReservationDTO.model_construct(
            id_reservation = uuid4(),
            date_debut_reservation = datetime(2034, 9, 11),
            date_fin_reservation = datetime(2034, 9, 11),
            prix_jour = 150,
            info_reservation = None,
            usager = None,
            chambre = None
        )

        with self.assertRaises(ValueError):
            reservation.verifier_date_fin_ulterieure()

    # Vérifier que Pydantic exécute automatiquement le model_validator
    def test_validation_automatique_dates_invalides(self):
        reservation = self.creer_reservation_pour_validation(prix=150, date_debut=datetime(2034, 9, 15),
                                                             date_fin=datetime(2034, 9, 11))

        with self.assertRaises(ValidationError):
            ReservationDTO(reservation)

    # Méthode utilitaire pour créer une réservation sans utiliser la BD
    def creer_reservation_pour_validation(
        self,
        prix,
        date_debut = datetime(2034, 9, 11),
        date_fin = datetime(2034, 9, 15)
    ):
        usager = Usager(
            id_usager = uuid4(),
            prenom = "Melissa",
            nom = "Test",
            adresse = "123 rue Test",
            mobile = "514-555-9999",
            mot_de_passe = "test123"
        )

        typeChambre = TypeChambre(
            id_type_chambre = uuid4(),
            nom_type = "king",
            prix_plancher = 179.0,
            prix_plafond = 299.0,
            description_chambre = "Chambre avec lit king"
        )

        chambre = Chambre(
            id_chambre = uuid4(),
            numero_chambre = 9500,
            disponible_reservation = True,
            autre_informations = None,
            type_chambre = typeChambre
        )

        return Reservation(
            id_reservation = uuid4(),
            date_debut_reservation = date_debut,
            date_fin_reservation = date_fin,
            prix_jour = prix,
            info_reservation = None,
            usager = usager,
            chambre = chambre
        )


    # Vérifier qu'un prix positif est accepté
    def test_validation_prix_positif(self):
        reservation = self.creer_reservation_pour_validation(prix=150)
        dto = ReservationDTO(reservation)
        self.assertEqual(dto.prix_jour, 150)
    
    # Vérifier qu'un prix de zéro est refusé
    def test_validation_prix_zero(self):
        reservation = self.creer_reservation_pour_validation(prix=0)
        with self.assertRaises(ValidationError):
            ReservationDTO(reservation)
    
    # Vérifier qu'un prix négatif est refusé
    def test_validation_prix_negatif(self):
        reservation = self.creer_reservation_pour_validation(prix=-50)
        with self.assertRaises(ValidationError):
            ReservationDTO(reservation)