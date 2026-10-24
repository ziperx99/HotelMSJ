# Modules et librairies
from uuid import UUID, uuid4
from sqlalchemy import create_engine, select
from sqlalchemy.exc import InterfaceError, SQLAlchemyError
from sqlalchemy.orm import Session
from modele.chambre import Chambre
from modele.type_chambre import TypeChambre
from DTO.chambre_dto import ChambreDTO, TypeChambreDTO


# Configuration du moteur de base de données
engine = create_engine(
    'mssql+pyodbc://localhost\SQLEXPRESS/Hotel?driver=ODBC+Driver+18+for+SQL+Server',
    connect_args=
        {
            "TrustServerCertificate": "yes"
        },
    use_setinputsizes=False)


def creer_chambre(chambre: ChambreDTO):
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
            session.refresh(nouvelleChambre)

            return ChambreDTO (nouvelleChambre)

    except InterfaceError as e:
            print(f"Erreur de connexion à la base de données. Vérifier l'URL du pilote de connexion.: {e}")    

    except SQLAlchemyError as e:
            print(f"Une erreur est survenue avec la base de données : {e}")    
            raise e
    
    else:
        print("Chambre créée sans problème")


    

def creer_type_chambre(typeChambre: TypeChambreDTO):

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
            session.refresh(nouveauTypeChambre)
            
            return TypeChambreDTO (nouveauTypeChambre)

    except InterfaceError as e:
            print(f"Erreur de connexion à la base de données. Vérifier l'URL du pilote de connexion.: {e}")

    except SQLAlchemyError as e:
            print(f"Une erreur est survenue avec la base de données : {e}")    
            raise e

    else:
            print("TypeChambre créée sans problème")

    

def get_chambre_par_numero(no_chambre: int):
    # Certaines validations se retrouvent dans la classe DTO.
    try:
        with Session(engine) as session:
            stmt = select(Chambre).where(Chambre.numero_chambre == no_chambre)
            result = session.execute(stmt)

            for chambre in result.scalars():
                return ChambreDTO (chambre)

    except InterfaceError as e:
        print(f"Erreur de connexion à la base de données : {e}")
        raise

    except SQLAlchemyError as e:
        print(f"Une erreur est survenue avec la base de données : {e}")
        raise

    except ValueError as e:
        print(e)
        raise

    # Aucun Finally nécessaire


def modifier_chambre(chambre: ChambreDTO):

    try:

        with Session(engine) as session:

            stmt = select(Chambre).where(Chambre.id_chambre == chambre.idChambre)

            # one_or_none() retourne la chambre si elle existe, sinon retourne None.
            chambreAModifier = session.execute(stmt).scalars().one_or_none()

            # Vérifier que la chambre existe déjà dans la base de données avant de la modifier
            if chambreAModifier is None:
                raise ValueError("La chambre n'existe pas")

            # Met à jour le numéro de la chambre
            chambreAModifier.numero_chambre = chambre.numero_chambre

            # Met à jour la disponibilité de la chambre pour les réservations
            chambreAModifier.disponible_reservation = chambre.disponible_reservation

            # Vérifie si de nouvelles informations ont été fournies avant de les modifier.
            # Si autre_informations=None, on conserve la valeur déjà présente dans la base de données.
            if chambre.autre_informations is not None:
                chambreAModifier.autre_informations = chambre.autre_informations

            # Recherche le type de chambre dans la base de données à partir de l'id fourni dans le DTO.
            typeChambre = session.execute(
                select(TypeChambre).where(TypeChambre.id_type_chambre == chambre.type_chambre.id_type_chambre)
            ).scalars().one()
            chambreAModifier.type_chambre = typeChambre

            session.commit()

    except InterfaceError as e:
        print(f"Erreur de connexion à la base de données : {e}")
        raise

    except SQLAlchemyError as e:
        print(f"Une erreur est survenue avec la base de données : {e}")
        raise

    except ValueError as e:
        print(e)
        raise

    # Aucun Finally nécessaire


def supprimer_chambre(id_chambre):
    # Vérifier qu'un identifiant a été fourni
    # Sans ça, on peut pas savoir quelle chambre supprimer
    if id_chambre is None:
        raise ValueError("L'identifiant de la chambre doit exister.")
    
    try:
        with Session(engine) as session:
            # Rechercher la chambre dans la BD à partir de son UUID
            stmt = select(Chambre).where(
                Chambre.id_chambre == id_chambre
            )

            # Retourne la chambre trouvée ou None si elle n'existe pas
            chambre = session.execute(stmt).scalar_one_or_none()
            # Vérifier que la chambre existe
            if chambre is None:
                raise ValueError("La chambre n'existe pas.")
            
            # Vérifier si des réservations sont associés à cette chambre
            # On refuse la suppression pour ne pas perdre les réservations existantes
            if len(chambre.reservations) > 0:
                raise ValueError(
                    "Impossible de supprimer une chambre qui possède des réservations."
                )
            
            # Supprimer la chambre de la session
            session.delete(chambre)
            # Enregistrer la suppression dans la BD
            session.commit()
    
    except InterfaceError as e:
        print(f"Erreur de connexion à la base de données : {e}")
        raise
    except SQLAlchemyError as e:
        print(f"Une erreur est survenue avec la base de données : {e}")
        raise

def supprimer_type_chambre(id_type_chambre):
    # Vérifier qu'un identifiant a été fourni
    # Sans ça, on peut pas savoir quel type supprimer
    if id_type_chambre is None:
        raise ValueError("L'identifiant du type de chambre doit exister.")
    
    try:
        with Session(engine) as session:
            # Rechercher le type de chambre dans la base de données
            stmt = select(TypeChambre).where(
                TypeChambre.id_type_chambre == id_type_chambre
            )

            # Retourne le type de chambre trouvé ou None si y'en a pas
            typeChambre = session.execute(stmt).scalar_one_or_none()
            # Empêcher la suppression d'un type inexistant
            if typeChambre is None:
                raise ValueError("Le type de chambre n'existe pas.")
            
            # Vérifier si des chambres utilisent encore ce type
            stmtChambres = select(Chambre).where(
                Chambre.fk_type_chambre == id_type_chambre
            )
            chambreExistante = session.execute(
                stmtChambres
            ).scalars().first()

            # Une chambre utilise ce type donc on refuse la suppression
            if chambreExistante is not None:
                raise ValueError(
                    "Impossible de supprimer un type de chambre utilisé."
                )
            
            # Supprimer le type de chambre trouvé
            session.delete(typeChambre)
            # Enregistrer la suppression dans la BD
            session.commit()

    except InterfaceError as e:
        print(f"Erreur de connexion à la base de données : {e}")
        raise
    except SQLAlchemyError as e:
        print(f"Une erreur est survenue avec la base de données : {e}")
        raise

def rechercher_type_chambre(id_type_chambre):
    # Vérifier qu'un identifiant a été fourni
    if id_type_chambre is None:
        raise ValueError("L'identifiant du type de chambre doit exister.")
    # Vérifier le format de l'identifiant
    try:
        id_type_chambre = UUID(str(id_type_chambre))
    except (ValueError, TypeError, AttributeError):
        raise ValueError("L'identifiant du type de chambre doit être un UUID valide.")
    
    try:
        with Session(engine) as session:
            # Rechercher le type de chambre dans la BD
            stmt = select(TypeChambre).where(
                TypeChambre.id_type_chambre == id_type_chambre
            )

            typeChambre = session.execute(stmt).scalar_one_or_none()

            # Vérifier que le type de chambre existe
            if typeChambre is None:
                raise ValueError("Le type de chambre n'existe pas.")
            
            # Retourner le résultat sous forme de DTO
            return TypeChambreDTO(typeChambre)

    except InterfaceError as e:
        print(f"Erreur de connexion à la base de données : {e}")
        raise
    except SQLAlchemyError as e:
        print(f"Une erreur est survenue avec la base de données : {e}")
        raise

def modifier_type_chambre(typeChambre: TypeChambreDTO):
    # Vérifier qu'un identifiant a été fourni
    if typeChambre.id_type_chambre is None:
        raise ValueError("L'identifiant du type de chambre doit exister.")
    
    # Vérifier que le nom est valide
    if typeChambre.nom_type is None or typeChambre.nom_type.strip() == "":
        raise ValueError("Le nom du type de chambre doit exister.")
    
    try:
        with Session(engine) as session:
            # Rechercher le type de chambre dans la BD
            stmt = select(TypeChambre).where(
                TypeChambre.id_type_chambre == typeChambre.id_type_chambre
            )

            typeChambreAModifier = session.execute(
                stmt).scalar_one_or_none()
            
            # Vérifier que le type existe
            if typeChambreAModifier is None:
                raise ValueError("Le type de chambre n'existe pas.")
            
            # Modifier les informations
            typeChambreAModifier.nom_type = typeChambre.nom_type
            typeChambreAModifier.prix_plancher = typeChambre.prix_plancher
            typeChambreAModifier.prix_plafond = typeChambre.prix_plafond
            typeChambreAModifier.description_chambre = typeChambre.description_chambre

            # Enregistrer les modifications
            session.commit()
            session.refresh(typeChambreAModifier)
            return TypeChambreDTO(typeChambreAModifier)
    
    except InterfaceError as e:
        print(f"Erreur de connexion à la base de données : {e}")
        raise
    
    except SQLAlchemyError as e:
        print(f"Une erreur est survenue avec la base de données : {e}")
        raise