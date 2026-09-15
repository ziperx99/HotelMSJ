from typing import Any, Optional
from pydantic import BaseModel
from modele.chambre import TypeChambre, Chambre
from uuid import UUID

# Data Transfer Object : pydantic BaseModel pour intégration facile avec FastAPI
# Facilite aussi grandement la sérialization et la validation des données contenues dans les DTOs
class TypeChambreDTO(BaseModel):
    id_type_chambre : Optional[UUID] = None
    nom_type : str
    prix_plafond : Optional[float] = None
    prix_plancher : float
    description_chambre : Optional[str] = None

    def __init__(self, typeChambre: TypeChambre = None):
        super().__init__(id_type_chambre = typeChambre.id_type_chambre,
                         nom_type = typeChambre.nom_type,
                         prix_plafond = typeChambre.prix_plafond,
                         prix_plancher = typeChambre.prix_plancher,
                         description_chambre = typeChambre.description_chambre)
        
class ChambreDTO(BaseModel):
    idChambre : Optional[UUID]
    numero_chambre : int
    disponible_reservation : bool
    autre_informations: Optional[str] = None
    type_chambre: TypeChambreDTO

    def __init__(self, chambre: Chambre = None):
        super().__init__(idChambre = chambre.id_chambre,
                         numero_chambre = chambre.numero_chambre,
                         disponible_reservation = chambre.disponible_reservation,
                         autre_informations = chambre.autre_informations,
                         type_chambre = TypeChambreDTO(chambre.type_chambre))