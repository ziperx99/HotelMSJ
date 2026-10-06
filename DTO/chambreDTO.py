from typing import Any, Optional
from pydantic import BaseModel, Field, model_validator, field_validator
from modele.chambre import Chambre
from modele.TypeChambre import TypeChambre
from uuid import UUID

# Data Transfer Object : pydantic BaseModel pour intégration facile avec FastAPI
# Facilite aussi grandement la sérialization et la validation des données contenues dans les DTOs
class TypeChambreDTO(BaseModel):
    id_type_chambre : UUID = Field(custom_error='id_type_chambre doit être un UUID comportant 36 caractères') #Le champ étant UUID valide déjà la taille
    nom_type : str = Field(max_length=50, custom_error='nom_type a une limite de 50 caractères')
    prix_plafond : Optional[float] = Field(default=None, ge=0, custom_error='prix_plafond doit être une valeur positive')
    prix_plancher : float = Field(ge=0, custom_error='prix_plancher doit être une valeur positive') #ge = Greater or Equal
    description_chambre : Optional[str] = Field(max_length=200, custom_error="description_chambre a une limite de 200 caractères")

    @model_validator(mode="after")
    def validerPrix(self):
        # Le model_validator est exécuté après la validation invidividuelle des champs
        # Permet de comparer les prix entre eux
        # Le prix plafond peut être None, donc on le vérifie d'abord et si il existe, il doit être supérieur à plancher
        if self.prix_plafond is not None and self.prix_plafond <= self.prix_plancher:
            raise ValueError("Le prix plafond doit être supérieur au prix plancher.")
        # Si les prix sont valides, pydantic continuer la création du DTO
        return self
    def __init__(self, typeChambre: TypeChambre = None): 
        super().__init__(id_type_chambre = typeChambre.id_type_chambre,
                         nom_type = typeChambre.nom_type,
                         prix_plafond = typeChambre.prix_plafond,
                         prix_plancher = typeChambre.prix_plancher,
                         description_chambre = typeChambre.description_chambre)

        
class ChambreDTO(BaseModel):
    idChambre : UUID = Field(custom_error='id_type_chambre doit être un UUID comportant 36 caractères')
    numero_chambre : int = Field(ge=0, le=2147483647, custom_error='numero_chambre doit être une valeur positive avec une taille maximale de 4 bytes')
    disponible_reservation : bool = Field(custom_error='disponible_reservation doit être un bool')
    autre_informations: Optional[str] = Field(default=None, max_length=2147483647, custom_error='autre_informations doit posséder une taille plus petite que 2GB')
    type_chambre: TypeChambreDTO

    @field_validator("numero_chambre", mode="before")
    @classmethod
    def validerNumeroChambre(cls, valeur):
        # Ce field_validator s'applique uniquement au champ numero_chambre
        # Le mode "before" permet de vérifier la valeur avant que pydantic essaie de le convertir
        # Une chambre doit obligatoirement avoir un numéro
        # Si aucune valeur fournie, on empêche la création
        if valeur is None:
            raise ValueError("Le numéro de chambre ne peut pas être nul.")
        # Si le numéro n'est pas nul, on retourne la valeur que pydantic puisse continuer ses autres validations
        return valeur
    def __init__(self, chambre: Chambre = None):
        super().__init__(idChambre = chambre.id_chambre,
                         numero_chambre = chambre.numero_chambre,
                         disponible_reservation = chambre.disponible_reservation,
                         autre_informations = chambre.autre_informations,
                         type_chambre = TypeChambreDTO(chambre.type_chambre))