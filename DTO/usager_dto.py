# Modules et librairies
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from modele.usager import Usager


class UsagerDTO(BaseModel):
    id_usager: UUID = Field(custom_error='id_usager doit être un UUID comportant 36 caractères')
    prenom: str = Field(max_length=50, custom_error='prenom a une limite de 50 caractères')
    nom: str = Field(max_length=50, custom_error='nom a une limite de 50 caractères')
    adresse: str = Field(max_length=100, custom_error='adresse a une limite de 100 caractères')
    mobile: str = Field(max_length=15, custom_error='mobile a une limite de 15 caractères')
    mot_de_passe: str = Field(max_length=60, custom_error='mot_de_passe a une limite de 60 caractères')

    @field_validator("prenom", "nom", "adresse", "mobile", "mot_de_passe", mode="before")
    @classmethod
    def valider_champs_obligatoires(cls, valeur):
        if valeur is None or str(valeur).strip() == "":
            raise ValueError("Ce champ ne peut pas être vide.")
        return valeur

    @field_validator("mobile")
    @classmethod
    def valider_mobile(cls, valeur):
        chiffres = valeur.replace("-", "").replace(" ", "")
        if len(chiffres) != 10:
            raise ValueError("Le numéro de téléphone doit contenir 10 chiffres.")
        return valeur

    def __init__(self, usager: Usager = None, **kwargs):

        if usager is not None:
            super().__init__(
                id_usager=usager.id_usager,
                prenom=usager.prenom,
                nom=usager.nom,
                adresse=usager.adresse,
                mobile=usager.mobile,
                mot_de_passe=usager.mot_de_passe
            )

        else:
            super().__init__(**kwargs)