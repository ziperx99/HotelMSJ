from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from DTO.usagerDTO import UsagerDTO
from modele.usager import Usager
from uuid import uuid4

engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+18+for+SQL+Server',
    connect_args={
        "TrustServerCertificate": "yes"
    },
    use_setinputsizes=False
)


def creerUsager(usager: UsagerDTO):

    # Validations
    if usager.prenom is None or usager.prenom.strip() == "":
        raise ValueError("Le prénom doit exister.")

    if usager.nom is None or usager.nom.strip() == "":
        raise ValueError("Le nom doit exister.")

    if usager.adresse is None or usager.adresse.strip() == "":
        raise ValueError("L'adresse doit exister.")

    if usager.mobile is None or usager.mobile.strip() == "":
        raise ValueError("Le numéro de téléphone doit exister.")

    if usager.mot_de_passe is None or usager.mot_de_passe.strip() == "":
        raise ValueError("Le mot de passe doit exister.")

    with Session(engine) as session:
        nouvelUsager = Usager(
            id_usager=uuid4(),
            prenom=usager.prenom,
            nom=usager.nom,
            adresse=usager.adresse,
            mobile=usager.mobile,
            mot_de_passe=usager.mot_de_passe
        )

        session.add(nouvelUsager)
        session.commit()

        return UsagerDTO(nouvelUsager)


def getUsagerParId(id_usager):

    if id_usager is None:
        raise ValueError(
            "L'identifiant de l'usager doit exister."
        )

    with Session(engine) as session:
        stmt = select(Usager).where(
            Usager.id_usager == id_usager
        )

        usager = session.execute(
            stmt
        ).scalar_one_or_none()

        if usager is None:
            raise ValueError(
                "L'usager n'existe pas."
            )

        return UsagerDTO(usager)

def getUsagerParNom(nom: str):
    # Vérifie qu'un nom a été donné. On refuse None, un chaîne vide ou juste des espaces
    if nom is None or nom.strip() == "":
        raise ValueError("Le nom de l'usager doit exister.")
    
    try:
        with Session(engine) as session:
            # Rechercher les usagers avec ce nom
            stmt = select(Usager).where(Usager.nom == nom.strip())

            # scalars().all() retourne une liste d'usagers
            usagers = session.execute(stmt).scalars().all()

            # Si aucun usager avec ce nom
            if len(usagers) == 0:
                raise ValueError("Aucun usager trouvé avec ce nom.")
            
            # Convertir les objets SQLAlchemy en DTO
            resultats = []
            for usager in usagers:
                resultats.append(UsagerDTO(usager))
            return resultats
    except SQLAlchemyError as e:
        print(f"Une erreur est survenue avec la base de données : {e}")
        raise


def modifierUsager(usager: UsagerDTO):

    if usager.id_usager is None:
        raise ValueError(
            "L'identifiant de l'usager doit exister."
        )

    if usager.prenom is None or usager.prenom.strip() == "":
        raise ValueError("Le prénom doit exister.")

    if usager.nom is None or usager.nom.strip() == "":
        raise ValueError("Le nom doit exister.")

    if usager.adresse is None or usager.adresse.strip() == "":
        raise ValueError("L'adresse doit exister.")

    if usager.mobile is None or usager.mobile.strip() == "":
        raise ValueError(
            "Le numéro de téléphone doit exister."
        )

    if usager.mot_de_passe is None or usager.mot_de_passe.strip() == "":
        raise ValueError(
            "Le mot de passe doit exister."
        )

    with Session(engine) as session:
        stmt = select(Usager).where(
            Usager.id_usager == usager.id_usager
        )

        usagerAModifier = session.execute(
            stmt
        ).scalar_one_or_none()

        if usagerAModifier is None:
            raise ValueError(
                "L'usager n'existe pas."
            )

        usagerAModifier.prenom = usager.prenom
        usagerAModifier.nom = usager.nom
        usagerAModifier.adresse = usager.adresse
        usagerAModifier.mobile = usager.mobile
        usagerAModifier.mot_de_passe = usager.mot_de_passe

        session.commit()

        return UsagerDTO(usagerAModifier)