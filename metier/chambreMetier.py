from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from DTO.chambreDTO import ChambreDTO, TypeChambreDTO
from modele.chambre import Chambre
from modele.TypeChambre import TypeChambre
from uuid import UUID, uuid4

engine = create_engine(
    'mssql+pyodbc://localhost\SQLEXPRESS/Hotel?driver=ODBC+Driver+18+for+SQL+Server',
    connect_args=
        {
            "TrustServerCertificate": "yes"
        },
    use_setinputsizes=False)

def creerChambre(chambre: ChambreDTO):
    # DONE: TODO : Générer un UUID et l'assigner à la chambre, si vous n'utilisez pas un auto-increment.
    # DONE: TODO : Ajouter des validations au besoin. EX: Lorsque l'on crééé une chambre, s'il n'y a pas de numéro de chambre
    # ou si le numéro de chambre existe déjà, on Raise un ValueError
    # TODO : Ajouter gestion des erreurs. On va voir un exemple au prochain cours.
    with Session(engine) as session:
        stmt = select(TypeChambre).where(TypeChambre.nom_type == chambre.type_chambre.nom_type)
        result = session.execute(stmt)

        # Validations d'erreur
        # Validation de l'existence du numéro de chambre
        if chambre.numero_chambre is None:
            raise ValueError("Le numéro de chambre doit exister")

        # Validation de duplicat de numéro de chambre
        with Session(engine) as session2:
            stmt2 = select(Chambre).where(Chambre.numero_chambre == chambre.numero_chambre)
            if session2.execute(stmt2).scalar_one_or_none() is not None:
                raise ValueError("Le numéro de chambre existe déjà.")
            session2.close()

        for typeChambre in result.scalars():
            
            nouvelleChambre = Chambre(
                id_chambre = uuid4(),
                numero_chambre = chambre.numero_chambre,
                disponible_reservation = chambre.disponible_reservation,
                autre_informations = chambre.autre_informations,
                type_chambre = typeChambre
            )

        session.add(nouvelleChambre)
        session.commit()

        return chambre

def creerTypeChambre(typeChambre: TypeChambreDTO):
    #TODO : Générer un UUID et l'assigner à la chambre, si vous n'utilisez pas un auto-increment.
    #TODO: Ajouter des validations au besoin.
    #TODO: Ajouter gestion des erreurs. On va voir un exemple au prochain cours.
    with Session(engine) as session:
        nouveauTypeChambre = TypeChambre(
            id_type_chambre = uuid4(),
            nom_type = typeChambre.nom_type,
            prix_plafond = typeChambre.prix_plafond,
            prix_plancher = typeChambre.prix_plancher,
            description_chambre = typeChambre.description_chambre,
        )

        session.add(nouveauTypeChambre)
        session.commit()

        return typeChambre

def getChambreParNumero(no_chambre: int):
    #TODO : Ajouter des validations au besoin. EX: no_chambre ne doit pas être null.
    #TODO : Ajouter gestion des erreurs. On va voir un exemple au prochain cours.
    with Session(engine) as session:
        stmt = select(Chambre).where(Chambre.numero_chambre == no_chambre)
        result = session.execute(stmt)

        for chambre in result.scalars():
            return ChambreDTO (chambre)

def modifierChambre(chambre: ChambreDTO):
    #TODO: Valider que la chambre existe bien dans la BD et autres validations.
    #TODO: Ajouter gestion des erreurs. On va voir un exemple au prochain cours.
    with Session(engine) as session:
        stmt = select(Chambre).where(Chambre.id_chambre == chambre.idChambre)
        chambreAModifier = session.execute(stmt).scalars().one()

        chambreAModifier.disponible_reservation = chambre.disponible_reservation
        chambreAModifier.autre_informations = chambre.autre_informations
        chambreAModifier.numero_chambre = chambre.numero_chambre
        #TODO: Setter les autres champs

        session.commit()
