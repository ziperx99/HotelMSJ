# Modules et librairies
import unittest
from datetime import datetime
from uuid import uuid4
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from modele.type_chambre import TypeChambre
from modele.chambre import Chambre
from modele.reservation import Reservation
from modele.usager import Usager
from DTO.chambre_dto import ChambreDTO
from DTO.reservation_dto import ReservationDTO
from DTO.usager_dto import UsagerDTO
from metier.chambre_metier import creerChambre
from metier.reservation_metier import creerReservation, supprimerReservation
from metier.usager_metier import creerUsager

engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+18+for+SQL+Server',
    connect_args={"TrustServerCertificate": "yes"},
    use_setinputsizes=False
)


class TestSupprimerReservation(unittest.TestCase):

    def test_supprimerReservation(self):

        try:
            #Création d'une réservation pour le test
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


            # Vérifier que la réservation est dans la BD
            with Session(engine) as session:

                stmt = select(Reservation).where(
                    Reservation.id_reservation == reservationDTOCree.id_reservation
                )

                reservationBD = session.execute(
                    stmt
                ).scalar_one_or_none()

                self.assertIsNotNone(reservationBD)

            
                # Suppression de la réservation
                supprimerReservation(reservationDTOCree.id_reservation)

            # On vérifie que la réservation n'existe plus
            with Session(engine) as session:
                reservation = session.get(Reservation, reservationDTOCree.id_reservation)
                self.assertIsNone(reservation)
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

    def test_supprimerReservationIdNull(self):
        with self.assertRaises(ValueError):
            supprimerReservation(None)
    
    def test_supprimerReservationInexistante(self):
        # On génère un ID aléatoire
        # Il devrait pas être un ID existant dans la BD
        id_inexistant = uuid4()
        # On tente de supprimer une réservation qui n'existe pas. Doit déclencher un ValueError, si aucun valueerror, le test échoue
        with self.assertRaises(ValueError):
            supprimerReservation(id_inexistant)