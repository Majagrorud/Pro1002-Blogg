import os
import unittest

import db
from init_db import init_db

TEST_DATABASE = "test_blogg.db"


class TestDatabase(unittest.TestCase):

    def setUp(self):
        db.DATABASE = TEST_DATABASE
        init_db(TEST_DATABASE)

    def tearDown(self):
        os.remove(TEST_DATABASE)

    def test_henter_alle_innlegg(self):
        innlegg = db.hent_alle_innlegg()
        self.assertEqual(len(innlegg), 10)

    def test_nyeste_innlegg_kommer_forst(self):
        innlegg = db.hent_alle_innlegg()
        self.assertEqual(innlegg[0]["tittel"], "Topp 10 hundevennlige restauranter i Oslo")

    def test_henter_ett_innlegg(self):
        innlegg = db.hent_innlegg(3)
        self.assertEqual(innlegg["tittel"], "Hundekafe på Løkka")

    def test_innlegg_som_ikke_finnes_gir_none(self):
        self.assertIsNone(db.hent_innlegg(999))

    def test_henter_tagger_sortert(self):
        navn = []
        for tag in db.hent_tagger(2):
            navn.append(tag["navn"])
        self.assertEqual(navn, ["arrangement", "mat", "pizza"])

    def test_henter_innlegg_med_tag(self):
        innlegg = db.hent_innlegg_med_tag("pizza")
        self.assertEqual(len(innlegg), 1)
        self.assertEqual(innlegg[0]["id"], 2)

    def test_lagrer_kommentar(self):
        db.lagre_kommentar(5, "Test", "Dette er en test.")
        kommentarer = db.hent_kommentarer(5)
        self.assertEqual(len(kommentarer), 1)
        self.assertEqual(kommentarer[0]["tittel"], "Test")

    def test_lagrer_innlegg_med_tagger(self):
        nytt_id = db.lagre_innlegg("Nytt innlegg", "Litt tekst")
        db.lagre_tagger(nytt_id, ["hund", "ny"])
        self.assertEqual(db.hent_innlegg(nytt_id)["tittel"], "Nytt innlegg")
        self.assertEqual(len(db.hent_alle_innlegg()), 11)
        self.assertEqual(len(db.hent_innlegg_med_tag("ny")), 1)

    def test_oppdaterer_innlegg(self):
        db.oppdater_innlegg(1, "Ny tittel", "Ny tekst")
        self.assertEqual(db.hent_innlegg(1)["tittel"], "Ny tittel")
        