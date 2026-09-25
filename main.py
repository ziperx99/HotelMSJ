from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

# IMPORTANT :
# On importe les 4 classes pour que SQLAlchemy connaisse
# tous les modèles et toutes les relations.
from modele.chambre import Chambre
from modele.TypeChambre import TypeChambre
from modele.usager import Usager
from modele.reservation import Reservation


engine = create_engine(
    "mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server",
    use_setinputsizes=False
)


app = FastAPI()


@app.get("/chambres/{numero_chambre}")
def read_chambre(numero_chambre: int):

    with Session(engine) as session:

        stmt = select(Chambre).where(
            Chambre.numero_chambre == numero_chambre
        )

        chambre = session.scalars(stmt).first()

        if chambre is None:
            raise HTTPException(
                status_code=404,
                detail="Chambre introuvable"
            )

        return {
            "numero_chambre": chambre.numero_chambre,
            "disponible_reservation": chambre.disponible_reservation,
            "autre_informations": chambre.autre_informations,
            "type_chambre": (
                chambre.type_chambre.nom_type
                if chambre.type_chambre is not None
                else None
            )
        }