from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from DTO.chambreDTO import ChambreDTO
from DTO.usagerDTO import UsagerDTO
from DTO.reservationDTO import ReservationDTO
from modele.usager import Usager
from modele.chambre import Chambre
from modele.reservation import Reservation
from uuid import uuid4

engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+18+for+SQL+Server',
    connect_args={
        "TrustServerCertificate": "yes"
    },
    use_setinputsizes=False
)

def creerReservation(reservation: ReservationDTO):

    with Session(engine) as session:
        stmt1 = select(Usager).where(Usager.id_usager == reservation.usager.id_usager)
        usagerSelect = session.execute(stmt1).scalar_one_or_none()

        #Validation de l'existence du numéro de chambre
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

    