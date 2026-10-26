# Modules et librairies
import unittest
from datetime import datetime
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from modele.type_chambre import TypeChambre
from modele.chambre import Chambre
from modele.reservation import Reservation
from modele.usager import Usager
from DTO.chambre_dto import ChambreDTO
from DTO.rechercher_reservation_dto import RechercherReservationDTO
from DTO.reservation_dto import ReservationDTO
from DTO.usager_dto import UsagerDTO
from metier.chambre_metier import creer_chambre
from metier.reservation_metier import creer_reservation, rechercher_reservation
from metier.usager_metier import creer_usager


# Configuration du moteur de base de données
engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+18+for+SQL+Server',
    connect_args={"TrustServerCertificate": "yes"},
    use_setinputsizes=False
)


class TestRechercherReservation(unittest.TestCase):

    def test_rechercher_reservation_par_id_reservation(self):

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

            usagerCree = creer_usager(UsagerDTO(usager))
            chambreCree = creer_chambre(ChambreDTO(chambre))

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
                reservationDTOCree = creer_reservation(reservationDTO)


            criteres = RechercherReservationDTO(
                id_reservation=reservationDTOCree.id_reservation
            )

            reservations = rechercher_reservation(criteres)

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


    def test_rechercher_reservation_par_id_chambre(self):

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

            usagerCree = creer_usager(UsagerDTO(usager))
            chambreCree = creer_chambre(ChambreDTO(chambre))

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
                reservationDTOCree = creer_reservation(reservationDTO)


            criteres = RechercherReservationDTO(
                id_chambre=reservationDTOCree.chambre.idChambre
            )

            reservations = rechercher_reservation(criteres)

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

    def test_rechercher_reservation_par_id_usager(self):

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

            usagerCree = creer_usager(UsagerDTO(usager))
            chambreCree = creer_chambre(ChambreDTO(chambre))

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
                reservationDTOCree = creer_reservation(reservationDTO)


            criteres = RechercherReservationDTO(
                id_usager=reservationDTOCree.usager.id_usager
            )

            reservations = rechercher_reservation(criteres)

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


    def test_rechercher_reservation_par_nom_et_prenom(self):

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

            usagerCree = creer_usager(UsagerDTO(usager))
            chambreCree = creer_chambre(ChambreDTO(chambre))

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
                reservationDTOCree = creer_reservation(reservationDTO)

            criteres = RechercherReservationDTO(
                                        nom = reservationDTOCree.usager.nom,
                                        prenom = reservationDTOCree.usager.prenom
                                    )

            reservations = rechercher_reservation(criteres)

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

    def test_rechercher_reservation_par_disponibilite(self):

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

            usagerCree = creer_usager(UsagerDTO(usager))
            chambreCree = creer_chambre(ChambreDTO(chambre))

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
                reservationDTOCree = creer_reservation(reservationDTO)

            criteres = RechercherReservationDTO(
                                        disponible_reservation=True
                                    )

            reservations = rechercher_reservation(criteres)

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


    def test_rechercher_reservation_par_date(self):

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

            usagerCree = creer_usager(UsagerDTO(usager))
            chambreCree = creer_chambre(ChambreDTO(chambre))

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
                reservationDTOCree = creer_reservation(reservationDTO)

            criteres = RechercherReservationDTO(
                                        date=datetime(2034, 10, 10)
                                    )

            reservations = rechercher_reservation(criteres)

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


    def test_rechercher_reservation_par_nom_et_prenom_sans_prenom(self):

        with self.assertRaises(ValueError):

            criteres = RechercherReservationDTO(
                            nom = "Test",
                            prenom = None
                        )

            rechercher_reservation(criteres)

    def test_rechercher_reservation_par_nom_et_prenom_sans_nom(self):
    
        with self.assertRaises(ValueError):

            criteres = RechercherReservationDTO(
                            nom = None,
                            prenom = "Test"
                        )

            rechercher_reservation(criteres)

    # Vérifier que le DTO accepte un nom et un prénom fournis ensemble
    def test_validation_nom_et_prenom_valides(self):
        criteres = RechercherReservationDTO(
            nom="Chapdelaine",
            prenom="Melissa"
        )
        self.assertEqual(criteres.nom, "Chapdelaine")
        self.assertEqual(criteres.prenom, "Melissa")

    # Vérifier que le DTO accepte une recherche sans nom ni prénom puisque les deux champs sont facultatifs
    def test_nom_et_prenom_absents(self):
        criteres = RechercherReservationDTO()
        self.assertIsNone(criteres.nom)
        self.assertIsNone(criteres.prenom)