# Modules et librairies
import unittest
from uuid import uuid4
from sqlalchemy.orm import Session
from modele.usager import Usager
from metier.usagerMetier import engine, getUsagerParNom


class Test_rechercherUsagerParNom(unittest.TestCase):
    
    def test_rechercherUsagerParNom(self):
        # Créer un usager temporaire pour notre recherche
        id_usager = uuid4()
        nom_test = "TestRechercheNom"

        with Session(engine) as session:
            usager = Usager(
                id_usager = id_usager,
                prenom = "TestPrenom",
                nom = nom_test,
                adresse = "123 rue Test",
                mobile = "514-555-1234",
                mot_de_passe = "test123"
            )

            session.add(usager)
            session.commit()

        try:
            # Recherche l'usager par son nom
            resultats = getUsagerParNom(nom_test)
            # Vérifie qu'une liste est retournée
            self.assertIsInstance(resultats, list)
            # Vérifie que l'usager est dedans
            ids = []
            for resultat in resultats:
                ids.append(resultat.id_usager)
            self.assertIn(id_usager, ids)
        
        finally:
            # Nettoyage BD
            with Session(engine) as session:
                usager = session.get(Usager, id_usager)

                if usager is not None:
                    session.delete(usager)
                    session.commit()


    def test_rechercherUsagerParNomNull(self):
        # Aucun nom fourni
        with self.assertRaises(ValueError):
            getUsagerParNom(None)
    
    def test_rechercherUsagerParNomVide(self):
        # Un nom composé d'espaces est invalide
        with self.assertRaises(ValueError):
            getUsagerParNom("    ")
    
    def test_rechercherUsagerParNomInexistant(self):
        # Recherche un nom inexistant dans la BD
        with self.assertRaises(ValueError):
            getUsagerParNom("NomInexistant_" + str(uuid4()))