# Modules et librairies
import unittest
from datetime import datetime
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from modele.TypeChambre import TypeChambre
from modele.chambre import Chambre
from modele.reservation import Reservation
from modele.usager import Usager
from DTO.chambreDTO import ChambreDTO
from DTO.rechercherReservationDTO import RechercherReservationDTO
from DTO.reservationDTO import ReservationDTO
from DTO.usagerDTO import UsagerDTO
from metier.chambreMetier import creerChambre
from metier.reservationMetier import (
    creerReservation,
    modifierReservation,
    rechercherReservation,
)
from metier.usagerMetier import creerUsager


# Configuration du moteur de base de données
engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+18+for+SQL+Server',
    connect_args={"TrustServerCertificate": "yes"},
    use_setinputsizes=False
)


class TestModifierTousLesChampsReservation(unittest.TestCase):

    def test_modifierTousLesChampsReservation(self):

        # Variables utilisées pour le nettoyage des données de test
        reservationDTOCree = None
        usagerCree = None
        chambreCree = None

        try:

            # Création d'un usager de test
            usager = Usager(
                id_usager=uuid4(),
                prenom="TestDebugReservation",
                nom="TestNom",
                adresse="123 rue Test",
                mobile="514-555-9999",
                mot_de_passe="test123"
            )

            # Création d'un type de chambre valide
            typeChambre = TypeChambre(
                id_type_chambre="99EF51BF-5E86-47E6-A1A3-601B936D91F0",
                nom_type="king",
                prix_plancher=179.0,
                prix_plafond=299.0,
                description_chambre="Chambre avec lit king"
            )

            # Création d'une chambre de test
            chambre = Chambre(
                id_chambre=uuid4(),
                numero_chambre=9999,
                disponible_reservation=True,
                autre_informations=None,
                type_chambre=typeChambre
            )

            # Création de l'usager et de la chambre dans la base de données
            usagerCree = creerUsager(UsagerDTO(usager))
            chambreCree = creerChambre(ChambreDTO(chambre))

            # Ouverture d'une session SQLAlchemy
            with Session(engine) as session:

                # Récupération des entités persistées
                usagerDB = session.get(Usager, usagerCree.id_usager)
                chambreDB = session.get(Chambre, chambreCree.idChambre)

                # Création d'une réservation de test
                reservation = Reservation(
                    id_reservation=uuid4(),
                    date_debut_reservation=datetime(2030, 10, 30),
                    date_fin_reservation=datetime(2030, 11, 5),
                    prix_jour=299.0,
                    info_reservation="Test création de réservation",
                    usager=usagerDB,
                    chambre=chambreDB
                )

                # Création de la réservation dans la base de données
                reservationDTOCree = creerReservation(ReservationDTO(reservation))

            # Modification de tous les champs de la réservation
            reservationModifiee = reservationDTOCree

            reservationModifiee.date_debut_reservation = datetime(2031, 1, 10)
            reservationModifiee.date_fin_reservation = datetime(2031, 1, 20)
            reservationModifiee.prix_jour = 199.0
            reservationModifiee.info_reservation = "Réservation modifiée"

            # Fonction métier
            modifierReservation(reservationModifiee)

            # Recherche de la réservation modifiée
            criteres = RechercherReservationDTO(id_reservation=reservationDTOCree.id_reservation)
            reservations = rechercherReservation(criteres)

            # Vérification des résultats de recherche
            self.assertIsNotNone(reservations)
            self.assertEqual(len(reservations), 1)

            # Récupération de la réservation trouvée
            reservationTrouvee = reservations[0]

            # Vérification de la date de début
            self.assertEqual(reservationTrouvee.date_debut_reservation, datetime(2031, 1, 10))

            # Vérification de la date de fin
            self.assertEqual(reservationTrouvee.date_fin_reservation, datetime(2031, 1, 20))

            # Vérification du prix par jour
            self.assertEqual(reservationTrouvee.prix_jour, 199.0)

            # Vérification des informations de réservation
            self.assertEqual(reservationTrouvee.info_reservation, "Réservation modifiée")

        finally:

            # Ouverture d'une session SQLAlchemy
            with Session(engine) as session:

                try:

                    # Récupération de la réservation créée pour le test
                    reservation = session.get(Reservation, reservationDTOCree.id_reservation)

                    # Suppression de la réservation de test
                    if reservationDTOCree is not None:
                        session.delete(reservation)
                        session.commit()

                finally:

                    # Récupération de l'usager de test
                    usagerDB = session.get(Usager, usagerCree.id_usager)

                    # Suppression de l'usager de test
                    if usagerDB is not None:
                        session.delete(usagerDB)
                        session.commit()

                    # Récupération de la chambre de test
                    chambreDB = session.get(Chambre, chambreCree.idChambre)

                    # Suppression de la chambre de test
                    if chambreDB is not None:
                        session.delete(chambreDB)
                        session.commit()