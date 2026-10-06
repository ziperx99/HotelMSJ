from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, InterfaceError
from sqlalchemy import create_engine, select
from DTO.chambreDTO import ChambreDTO, TypeChambreDTO
from modele.chambre import Chambre
from modele.TypeChambre import TypeChambre
from uuid import uuid4

engine = create_engine(
    'mssql+pyodbc://localhost\SQLEXPRESS/Hotel?driver=ODBC+Driver+18+for+SQL+Server',
    connect_args=
        {
            "TrustServerCertificate": "yes"
        },
    use_setinputsizes=False)

def creerChambre(chambre: ChambreDTO):
    try:
        with Session(engine) as session:
            stmt = select(TypeChambre).where(TypeChambre.nom_type == chambre.type_chambre.nom_type)
            result = session.execute(stmt)

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

    except InterfaceError as e:
            print(f"Erreur de connexion à la base de données. Vérifier l'URL du pilote de connexion.: {e}")    

    except SQLAlchemyError as e:
            print(f"Une erreur est survenue avec la base de données : {e}")    
            raise e
    
    else:
        print("Chambre créée sans problème")


    

def creerTypeChambre(typeChambre: TypeChambreDTO):

    try:
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

    except InterfaceError as e:
            print(f"Erreur de connexion à la base de données. Vérifier l'URL du pilote de connexion.: {e}")

    except SQLAlchemyError as e:
            print(f"Une erreur est survenue avec la base de données : {e}")    
            raise e

    else:
            print("TypeChambre créée sans problème")

    

def getChambreParNumero(no_chambre: int):
    #TODO : Ajouter des validations au besoin. EX: no_chambre ne doit pas être null.
    #TODO : Ajouter gestion des erreurs. On va voir un exemple au prochain cours.
    with Session(engine) as session:
        stmt = select(Chambre).where(Chambre.numero_chambre == no_chambre)
        result = session.execute(stmt)

        for chambre in result.scalars():
            return ChambreDTO (chambre)


def modifierChambre(chambre: ChambreDTO):
    #TODO: Ajouter gestion des erreurs. On va voir un exemple au prochain cours.
    with Session(engine) as session:
        stmt = select(Chambre).where(Chambre.id_chambre == chambre.idChambre)
        chambreAModifier = session.execute(stmt).scalars().one()
        
        # Vérifier que la chambre existe
        if chambreAModifier is None:
            raise ValueError("La chambre n'existe pas")
        
        # Setter les autres champs
        chambreAModifier.numero_chambre = chambre.numero_chambre
        chambreAModifier.disponible_reservation = chambre.disponible_reservation
        if chambre.autre_informations is None:
            chambreAModifier.autre_informations = chambre.autre_informations
        if chambre.idChambre is not None:
            chambreAModifier.id_chambre = chambre.idChambre
        if chambre.type_chambre is None:
            chambreAModifier.type_chambre = chambre.type_chambre

        session.commit()