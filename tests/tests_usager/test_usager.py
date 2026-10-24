import unittest
import logging
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from DTO.usagerDTO import UsagerDTO
from modele.chambre import Chambre
from modele.TypeChambre import TypeChambre
from modele.usager import Usager
from modele.reservation import Reservation
from decimal import Decimal
from pydantic import ValidationError


logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server',
    use_setinputsizes=False
)


class TestUsager(unittest.TestCase):

    def test_getUsager(self):

        with Session(engine) as session:

            stmt = select(Usager).where(
                Usager.prenom == 'Melissa'
            )

            usager = session.execute(stmt).scalar_one()

            # Tester tous les champs
            self.assertEqual(
                usager.prenom,
                'Melissa'
            )

            self.assertEqual(
                usager.nom,
                'Test'
            )

            self.assertEqual(
                usager.adresse,
                '123 rue Test'
            )

            self.assertEqual(
                usager.mobile.strip(),
                '514-555-1234'
            )

            self.assertEqual(
                usager.mot_de_passe.strip(),
                'test123'
            )

            self.assertEqual(
                str(usager.id_usager).upper(),
                '63E31298-1879-4856-8CB1-F57353271602'
            )

            # Relation avec Reservation
            self.assertEqual(
                len(usager.reservations),
                1
            )

            self.assertEqual(
                usager.reservations[0].info_reservation,
                'Reservation test'
            )

            self.assertEqual(
                usager.reservations[0].prix_jour,
                Decimal('199.99')
            )
     
     # Section qui couvre les tests de validation des champs obligatoires
    
    def test_prenom_vide(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="",
            nom="TestNom",
            adresse="123 rue Test",
            mobile="514-555-1234",
            mot_de_passe="test123"
        )

        with self.assertRaises(ValidationError):
            UsagerDTO(usager)
          
                
    def test_prenom_espaces_seulement(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="   ",
            nom="TestNom",
            adresse="123 rue Test",
            mobile="514-555-1234",
            mot_de_passe="test123"
        )

        with self.assertRaises(ValidationError):
            UsagerDTO(usager)
          
            
    def test_nom_vide(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="TestPrenom",
            nom="",
            adresse="123 rue Test",
            mobile="514-555-1234",
            mot_de_passe="test123"
        )

        with self.assertRaises(ValidationError):
            UsagerDTO(usager)
        
    
    def test_prenom_espaces_seulement(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="   ",
            nom="TestNom",
            adresse="123 rue Test",
            mobile="514-555-1234",
            mot_de_passe="test123"
        )

        with self.assertRaises(ValidationError):
            UsagerDTO(usager)
        
    
    def test_adresse_vide(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="TestPrenom",
            nom="TestNom",
            adresse="",
            mobile="514-555-1234",
            mot_de_passe="test123"
        )

        with self.assertRaises(ValidationError):
            UsagerDTO(usager)
    
    
    def test_adresse_espaces_seulement(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="TestPrenom",
            nom="TestNom",
            adresse="   ",
            mobile="514-555-1234",
            mot_de_passe="test123"
        )

        with self.assertRaises(ValidationError):
            UsagerDTO(usager)
        
    
    def test_mobile_vide(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="TestPrenom",
            nom="TestNom",
            adresse="123 rue Test",
            mobile="",
            mot_de_passe="test123"
        )

        with self.assertRaises(ValidationError):
            UsagerDTO(usager)
    
    
    def test_mobile_espaces_seulement(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="TestPrenom",
            nom="TestNom",
            adresse="123 rue Test",
            mobile="   ",
            mot_de_passe="test123"
        )

        with self.assertRaises(ValidationError):
            UsagerDTO(usager)
    
    
    def test_mobile_valide(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="Jean",
            nom="Tremblay",
            adresse="123 rue Test",
            mobile="514-555-1234",
            mot_de_passe="secret"
        )

        dto = UsagerDTO(usager)

        self.assertEqual(dto.mobile, "514-555-1234")
            
            
    def test_mobile_null(self):
        
        usager = Usager(
            id_usager=uuid4(),
            prenom="Jean",
            nom="Tremblay",
            adresse="123 rue Test",
            mobile=None,
            mot_de_passe="secret"
        )

        with self.assertRaises(ValueError):
            UsagerDTO(usager)


    def test_mobile_trop_court(self):
        
        usager = Usager(
            id_usager=uuid4(),
            prenom="Jean",
            nom="Tremblay",
            adresse="123 rue Test",
            mobile="12345",
            mot_de_passe="secret"
        )

        with self.assertRaises(ValueError) as context:
            UsagerDTO(usager)


    def test_mobile_trop_long(self):
        
        usager = Usager(
            id_usager=uuid4(),
            prenom="Jean",
            nom="Tremblay",
            adresse="123 rue Test",
            mobile="12345678901234567890",
            mot_de_passe="secret"
        )

        with self.assertRaises(ValueError):
            UsagerDTO(usager)
            
         
    def test_mot_de_passe_valide(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="Jean",
            nom="Tremblay",
            adresse="123 rue Test",
            mobile="514-555-1234",
            mot_de_passe="motdepasse123"
        )

        dto = UsagerDTO(usager)

        self.assertIsInstance(dto, UsagerDTO)
         
            
    def test_mot_de_passe_espaces_seulement(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="Jean",
            nom="Tremblay",
            adresse="123 rue Test",
            mobile="514-555-1234",
            mot_de_passe="     "
        )

        with self.assertRaises(ValidationError):
            UsagerDTO(usager)
            
          
    def test_mot_de_passe_trop_court(self):

        usager = Usager(
            id_usager=uuid4(),
            prenom="Jean",
            nom="Tremblay",
            adresse="123 rue Test",
            mobile="514-555-1234",
            mot_de_passe="abc"
        )

        with self.assertRaises(ValidationError):
            UsagerDTO(usager)        