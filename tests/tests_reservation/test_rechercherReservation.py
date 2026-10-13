import unittest

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from modele.chambre import Chambre
from modele.usager import Usager
from modele.TypeChambre import TypeChambre
from modele.reservation import Reservation
from DTO.chambreDTO import ChambreDTO
from DTO.usagerDTO import UsagerDTO
from DTO.reservationDTO import ReservationDTO
from DTO.rechercherReservationDTO import RechercherReservationDTO
from metier.reservationMetier import creerReservation, rechercherReservation
from metier.usagerMetier import creerUsager
from metier.chambreMetier import creerChambre
from uuid import uuid4
from datetime import datetime

engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+18+for+SQL+Server',
    connect_args={
        "TrustServerCertificate": "yes"
    },
    use_setinputsizes=False
)

class TestRechercherReservation(unittest.TestCase):

    def test_rechercherReservationParIdReservation(self):

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


            criteres = RechercherReservationDTO(
                id_reservation=reservationDTOCree.id_reservation
            )

            reservations = rechercherReservation(criteres)

            # Tests
            self.assertIsNotNone(reservations)

            for reservation in reservations:
                self.assertEqual(reservation.id_reservation, reservationDTOCree.id_reservation)

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


    def test_rechercherReservationParIdChambre(self):

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


            criteres = RechercherReservationDTO(
                id_chambre=reservationDTOCree.chambre.idChambre
            )

            reservations = rechercherReservation(criteres)

            # Tests
            self.assertIsNotNone(reservations)

            for reservation in reservations:
                self.assertEqual(reservation.chambre.idChambre, reservationDTOCree.chambre.idChambre)

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

    def test_rechercherReservationParIdUsager(self):

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


            criteres = RechercherReservationDTO(
                id_usager=reservationDTOCree.usager.id_usager
            )

            reservations = rechercherReservation(criteres)

            # Tests
            self.assertIsNotNone(reservations)

            for reservation in reservations:
                self.assertEqual(reservation.usager.id_usager, reservationDTOCree.usager.id_usager)

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


    def test_rechercherReservationParNomEtPrenom(self):

        try:
            usager = Usager(
                id_usager = uuid4(),
                prenom = "PrenomTest",
                nom = "NomTest",
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

            criteres = RechercherReservationDTO(
                                        nom = reservationDTOCree.usager.nom,
                                        prenom = reservationDTOCree.usager.prenom
                                    )

            reservations = rechercherReservation(criteres)

            # Tests
            self.assertIsNotNone(reservations)

            for reservation in reservations:
                self.assertEqual(reservation.usager.nom, reservationDTOCree.usager.nom)
                self.assertEqual(reservation.usager.prenom, reservationDTOCree.usager.prenom)

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

    def test_rechercherReservationParDisponibilite(self):

        try:
            usager = Usager(
                id_usager = uuid4(),
                prenom = "PrenomTest",
                nom = "NomTest",
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

            criteres = RechercherReservationDTO(
                                        disponible_reservation=True
                                    )

            reservations = rechercherReservation(criteres)

            # Tests
            self.assertIsNotNone(reservations)

            for reservation in reservations:
                self.assertEqual(reservation.chambre.disponible_reservation, reservationDTOCree.chambre.disponible_reservation)

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


    def test_rechercherReservationParDate(self):

        try:
            usager = Usager(
                id_usager = uuid4(),
                prenom = "PrenomTest",
                nom = "NomTest",
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

            criteres = RechercherReservationDTO(
                                        date=datetime(2034, 10, 10)
                                    )

            reservations = rechercherReservation(criteres)

            # Tests
            self.assertIsNotNone(reservations)

            for reservation in reservations:
                self.assertEqual(reservation.date_debut_reservation, reservationDTOCree.date_debut_reservation)
                self.assertEqual(reservation.date_fin_reservation, reservationDTOCree.date_fin_reservation)
                self.assertGreaterEqual(criteres.date, reservation.date_debut_reservation)
                self.assertGreaterEqual(reservation.date_fin_reservation, criteres.date)

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


    def test_rechercherReservationParNomEtPrenomSansPrenom(self):

        with self.assertRaises(ValueError):

            criteres = RechercherReservationDTO(
                            nom = "Test",
                            prenom = None
                        )
            
            rechercherReservation(criteres)

    def test_rechercherReservationParNomEtPrenomSansNom(self):
    
        with self.assertRaises(ValueError):

            criteres = RechercherReservationDTO(
                            nom = None,
                            prenom = "Test"
                        )
            
            rechercherReservation(criteres)