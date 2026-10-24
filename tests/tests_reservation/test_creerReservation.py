# Modules et librairies
import unittest
from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, ValidationError
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from modele.TypeChambre import TypeChambre
from modele.chambre import Chambre
from modele.reservation import Reservation
from modele.usager import Usager
from DTO.chambreDTO import ChambreDTO
from DTO.reservationDTO import ReservationDTO
from DTO.usagerDTO import UsagerDTO
from metier.chambreMetier import creerChambre
from metier.reservationMetier import creerReservation
from metier.usagerMetier import creerUsager


# Configuration du moteur de base de données
engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+18+for+SQL+Server',
    connect_args={"TrustServerCertificate": "yes"},
    use_setinputsizes=False
)


class test_creerReservation(unittest.TestCase):

    def test_creerReservation(self):

        try:

            usager = Usager(
                id_usager = uuid4(),
                prenom = "TestDebugReservation",
                nom = "TestNom",
                adresse = "123 rue Test",
                mobile = "514-555-9999",
                mot_de_passe = "test123"
            )

            typeChambre = TypeChambre(
                id_type_chambre = "99EF51BF-5E86-47E6-A1A3-601B936D91F0",
                nom_type = 'king',
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

            usagerCree = creerUsager(UsagerDTO(usager))
            chambreCree = creerChambre(ChambreDTO(chambre))

            with Session(engine) as session:
                usagerDB = session.get(Usager, usagerCree.id_usager)
                chambreDB = session.get(Chambre, chambreCree.idChambre)

                reservation = Reservation(
                    id_reservation = uuid4(),
                    date_debut_reservation = datetime(2034, 9, 11),
                    date_fin_reservation = datetime(2034, 10, 30),
                    prix_jour = 350,
                    info_reservation = "Test création de réservation",
                    usager = usagerDB,
                    chambre = chambreDB
                )

                reservationDTO = ReservationDTO(reservation)
                reservationDTOCree = creerReservation(reservationDTO)

            # Tests
            self.assertIsNotNone(
                reservationDTO.id_reservation
            )

            self.assertIsNotNone(
                reservationDTO.date_debut_reservation
            )

            self.assertIsNotNone(
                reservationDTO.date_fin_reservation
            )

            self.assertEqual(
                reservationDTO.prix_jour, 350
            )

            self.assertEqual(
                reservationDTO.info_reservation, "Test création de réservation"
            )

            self.assertEqual(
                reservationDTO.usager, usagerCree
            )

            self.assertEqual(
                reservationDTO.chambre, chambreCree
            )


            # Vérifier que la réservation est dans la BD
            with Session(engine) as session:

                stmt = select(Reservation).where(
                    Reservation.id_reservation == reservationDTOCree.id_reservation
                )

                reservationBD = session.execute(
                    stmt
                ).scalar_one_or_none()

                self.assertIsNotNone(reservationBD)

        finally:


            # Nettoyage de la BD
            with Session(engine) as session:
                try:
                    reservation = session.get(Reservation, reservationDTOCree.id_reservation)
                    if reservation is not None:
                        session.delete(reservation)
                        session.commit()

                finally:
                    usagerDB = session.get(Usager, usagerCree.id_usager)
                    if usagerDB is not None:
                        session.delete(usagerDB)
                        session.commit()

                    chambreDB = session.get(Chambre, chambreCree.idChambre)
                    if chambreDB is not None:
                        session.delete(chambreDB)
                        session.commit()

    def test_creerReservationDateDebutVide(self):

        with self.assertRaises(ValidationError):

            usager = Usager(
                id_usager = uuid4(),
                prenom = "TestDebugReservation",
                nom = "TestNom",
                adresse = "123 rue Test",
                mobile = "514-555-9999",
                mot_de_passe = "test123"
            )
    
            typeChambre = TypeChambre(
                id_type_chambre = "99EF51BF-5E86-47E6-A1A3-601B936D91F0",
                nom_type = 'king',
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

            ReservationDTO(
                Reservation(
                    id_reservation = uuid4(),
                    date_debut_reservation = None,
                    date_fin_reservation = datetime.now(),
                    prix_jour = 350,
                    info_reservation = "Test création de réservation",
                    usager = usager,
                    chambre = chambre)
            )

    def test_creerReservationDateFinVide(self):
    
        with self.assertRaises(ValidationError):

            usager = Usager(
                id_usager = uuid4(),
                prenom = "TestDebugReservation",
                nom = "TestNom",
                adresse = "123 rue Test",
                mobile = "514-555-9999",
                mot_de_passe = "test123"
            )
    
            typeChambre = TypeChambre(
                id_type_chambre = "99EF51BF-5E86-47E6-A1A3-601B936D91F0",
                nom_type = 'king',
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

            ReservationDTO(
                Reservation(
                    id_reservation = uuid4(),
                    date_debut_reservation = datetime.now(),
                    date_fin_reservation = None,
                    prix_jour = 350,
                    info_reservation = "Test création de réservation",
                    usager = usager,
                    chambre = chambre)
            )


    def test_creerReservationPrixJourVide(self):
    
        with self.assertRaises(ValidationError):

            usager = Usager(
                id_usager = uuid4(),
                prenom = "TestDebugReservation",
                nom = "TestNom",
                adresse = "123 rue Test",
                mobile = "514-555-9999",
                mot_de_passe = "test123"
            )
    
            typeChambre = TypeChambre(
                id_type_chambre = "99EF51BF-5E86-47E6-A1A3-601B936D91F0",
                nom_type = 'king',
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

            ReservationDTO(
                Reservation(
                    id_reservation = uuid4(),
                    date_debut_reservation = datetime(2034, 9, 11),
                    date_fin_reservation = datetime(2034, 10, 30),
                    prix_jour = None,
                    info_reservation = "Test création de réservation",
                    usager = usager,
                    chambre = chambre)
            )

    def test_creerReservationInfoReservationMauvaisType(self):

        with self.assertRaises(ValidationError):

            usager = Usager(
                id_usager = uuid4(),
                prenom = "TestDebugReservation",
                nom = "TestNom",
                adresse = "123 rue Test",
                mobile = "514-555-9999",
                mot_de_passe = "test123"
            )
    
            typeChambre = TypeChambre(
                id_type_chambre = "99EF51BF-5E86-47E6-A1A3-601B936D91F0",
                nom_type = 'king',
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

            ReservationDTO(
                Reservation(
                    id_reservation = uuid4(),
                    date_debut_reservation = datetime(2034, 9, 11),
                    date_fin_reservation = datetime(2034, 10, 30),
                    prix_jour = 350,
                    info_reservation = datetime.now(),
                    usager = usager,
                    chambre = chambre)
            )


    def test_creerReservationUsagerVide(self):
    
        with self.assertRaises(ValueError):
    
            typeChambre = TypeChambre(
                id_type_chambre = "99EF51BF-5E86-47E6-A1A3-601B936D91F0",
                nom_type = 'king',
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

            ReservationDTO(
                Reservation(
                    id_reservation = uuid4(),
                    date_debut_reservation = datetime(2034, 9, 11),
                    date_fin_reservation = datetime(2034, 10, 30),
                    prix_jour = 350,
                    info_reservation = datetime.now(),
                    usager = None,
                    chambre = chambre)
            )

    def test_creerReservationDateDebutUlterieure(self):

        with self.assertRaises(ValueError):

            usager = Usager(
                id_usager = uuid4(),
                prenom = "TestDebugReservation",
                nom = "TestNom",
                adresse = "123 rue Test",
                mobile = "514-555-9999",
                mot_de_passe = "test123"
            )
                
            typeChambre = TypeChambre(
                id_type_chambre = "99EF51BF-5E86-47E6-A1A3-601B936D91F0",
                nom_type = 'king',
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

            ReservationDTO(
                Reservation(
                    id_reservation = uuid4(),
                    date_debut_reservation = datetime(2034, 10, 30),
                    date_fin_reservation = datetime(2034, 9, 11),
                    prix_jour = 350,
                    info_reservation = datetime.now(),
                    usager = usager,
                    chambre = chambre)
            )