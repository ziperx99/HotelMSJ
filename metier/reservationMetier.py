# Modules et librairies
from uuid import uuid4
from sqlalchemy import create_engine, select
from sqlalchemy.exc import InterfaceError, SQLAlchemyError
from sqlalchemy.orm import Session
from modele.chambre import Chambre
from modele.reservation import Reservation
from modele.usager import Usager
from DTO.rechercherReservationDTO import RechercherReservationDTO
from DTO.reservationDTO import ReservationDTO


# Configuration du moteur de base de données
engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+18+for+SQL+Server',
    connect_args={
        "TrustServerCertificate": "yes"
    },
    use_setinputsizes=False
)

def creerReservation(reservation: ReservationDTO):
    try:
        with Session(engine) as session:
            stmt1 = select(Usager).where(Usager.id_usager == reservation.usager.id_usager)
            usagerSelect = session.execute(stmt1).scalar_one_or_none()

            #Validation de l'existence de l'usager
            if usagerSelect is None:
                raise ValueError("L'usager n'existe pas.")

            stmt2 = select(Chambre).where(Chambre.numero_chambre == reservation.chambre.numero_chambre)
            chambreSelect = session.execute(stmt2).scalar_one_or_none()

            nouvelleReservation = Reservation(
                id_reservation = uuid4(),
                date_debut_reservation = reservation.date_debut_reservation,
                date_fin_reservation = reservation.date_fin_reservation,
                prix_jour = reservation.prix_jour,
                info_reservation = reservation.info_reservation,
                usager = usagerSelect,
                chambre = chambreSelect
            )

            session.add(nouvelleReservation)
            session.commit()

            return ReservationDTO(nouvelleReservation)

    except InterfaceError as e:
            print(f"Erreur de connexion à la base de données. Vérifier l'URL du pilote de connexion.: {e}")    

    except SQLAlchemyError as e:
            print(f"Une erreur est survenue avec la base de données : {e}")    
            raise e
    
    else:
        print("Réservation créée sans problème")


def rechercherReservation(criteres: RechercherReservationDTO):

    try:

        # Vérification des critères reçus
        if criteres is None:
            raise ValueError("Les critères de recherche sont obligatoires.")

        stmt = select(Reservation)

        if(criteres.id_reservation):
            stmt = stmt.where(Reservation.id_reservation == criteres.id_reservation)

        if(criteres.id_usager):
            stmt = stmt.where(Reservation.fk_id_usager == criteres.id_usager)

        if(criteres.id_chambre):
            stmt = stmt.where(Reservation.fk_id_chambre == criteres.id_chambre)

        if(criteres.nom):
            stmt = stmt.join(Usager).where(Usager.nom == criteres.nom)
            stmt = stmt.where(Usager.prenom == criteres.prenom)

        if(criteres.disponible_reservation):
            stmt = stmt.join(Chambre).where(Chambre.disponible_reservation == criteres.disponible_reservation)

        if(criteres.date):
            stmt = stmt.where(Reservation.date_debut_reservation <= criteres.date)
            stmt = stmt.where(Reservation.date_fin_reservation >= criteres.date)

        reservations = []
        with Session(engine) as session:
            for reservation in session.execute(stmt).scalars():
                reservation.usager
                reservation.chambre
                reservations.append(ReservationDTO(reservation))

        return reservations 

    except ValueError as e:
        # Gestion des erreurs de validation
        raise Exception(
            f"Erreur de validation : {str(e)}"
        )

    except InterfaceError as e:
        # Gestion des erreurs de connexion à la base de données
        print(f"Erreur de connexion à la base de données : {e}")
        raise

    except SQLAlchemyError as e:
        # Gestion des erreurs SQLAlchemy
        print(f"Une erreur est survenue avec la base de données : {e}")
        raise


def supprimerReservation(id_reservation):

    # Vérification qu'on a bien un ID
    if id_reservation is None:
        raise ValueError("L'identifiant de la réservation doit exister.")
    
    try:
        with Session(engine) as session:
            # Recherche de la réservation
            stmt = select(Reservation).where(
                Reservation.id_reservation == id_reservation
            )

            # Retourne la réservation trouvée ou None si elle n'existe pas
            reservation = session.execute(stmt).scalar_one_or_none()
            # Vérifier que la réservation existe
            if reservation is None:
                raise ValueError("La réservation n'existe pas.")
            
            # Supprimer la réservation de la session
            session.delete(reservation)
            # Enregistrer la suppression dans la BD
            session.commit()
    
    except InterfaceError as e:
        print(f"Erreur de connexion à la base de données : {e}")
        raise
    except SQLAlchemyError as e:
        print(f"Une erreur est survenue avec la base de données : {e}")
        raise
    
    
def modifierReservation(reservation: ReservationDTO):
        
    try:
        
        # Ouverture d'une session SQLAlchemy
        with Session(engine) as session:
            
            # Recherche de la réservation existante
            stmt = select(Reservation).where(
                Reservation.id_reservation == reservation.id_reservation
            )
            reservation_existante = session.execute(stmt).scalar_one_or_none()

            # Vérifier que la réservation existe
            if reservation_existante is None:
                raise ValueError("La réservation n'existe pas.")

            # Mettre à jour les champs de la réservation existante avec les nouvelles valeurs
            reservation_existante.date_debut_reservation = reservation.date_debut_reservation
            reservation_existante.date_fin_reservation = reservation.date_fin_reservation
            reservation_existante.prix_jour = reservation.prix_jour
            reservation_existante.info_reservation = reservation.info_reservation

            # Enregistrer les modifications dans la BD
            session.commit()

    except InterfaceError as e:
        # Gestion des erreurs de connexion à la base de données
        print(f"Erreur de connexion à la base de données : {e}")
        raise
    
    except SQLAlchemyError as e:
        # Gestion des erreurs SQLAlchemy
        print(f"Une erreur est survenue avec la base de données : {e}")
        raise
    
    except ValueError as e:
        # Gestion des erreurs de valeur
        print(e)
        raise