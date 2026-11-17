import Reservation from "./Reservation";

const ListeReservation = ({ reservations }) => {
    const listeReservation = reservations.map(
        (reservation) => (
            <Reservation key={reservation.id} reservation={reservation} />
        )
    );

    return (
        <>
            {listeReservation}
        </>
    );
};

export default ListeReservation;