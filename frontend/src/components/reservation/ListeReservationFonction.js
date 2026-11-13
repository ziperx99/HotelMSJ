import Reservation from "./ReservationFonction";

const ListeReservation = ({ reservations }) => {
    const ListeReservation = reservations.map(
        (reservation) => (
            <Reservation key = {reservation.id} reservation={reservation} />
        )
    );

    return (
        <>
            {ListeReservation}
        </>
    );
};

export default ListeReservation;