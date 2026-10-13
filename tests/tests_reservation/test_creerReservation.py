import unittest

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, delete
from modele.chambre import Chambre
from modele.usager import Usager
from modele.TypeChambre import TypeChambre
from modele.reservation import Reservation
from DTO.chambreDTO import ChambreDTO
from DTO.usagerDTO import UsagerDTO
from DTO.reservationDTO import ReservationDTO
from metier.reservationMetier import creerReservation
from metier.usagerMetier import creerUsager
from metier.chambreMetier import creerChambre
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError


engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+18+for+SQL+Server',
    connect_args={
        "TrustServerCertificate": "yes"
    },
    use_setinputsizes=False
)


class test_creerReservation(unittest.TestCase):

    def test_creerReservation(self):

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
                date_debut_reservation = datetime.now(),
                date_fin_reservation = datetime.now(),
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
            

        # Nettoyer la BD
        with Session(engine) as session:

            stmt = delete(Reservation).where(
                Reservation.id_reservation == reservationDTOCree.id_reservation
            )

            session.execute(stmt)
            session.commit()

            stmt2 = delete(Usager).where(
                Usager.prenom == "TestDebugReservation"
            )

            session.execute(stmt2)
            session.commit()

            stmt3 = delete(Chambre).where(
                Chambre.numero_chambre == "9500"
            )

            session.execute(stmt3)
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
                    date_debut_reservation = datetime.now(),
                    date_fin_reservation = datetime.now(),
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
                    date_debut_reservation = datetime.now(),
                    date_fin_reservation = datetime.now(),
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
                        date_debut_reservation = datetime.now(),
                        date_fin_reservation = datetime.now(),
                        prix_jour = 350,
                        info_reservation = datetime.now(),
                        usager = None,
                        chambre = chambre)
                )


if __name__ == "__main__":
    unittest.main()