import os
import unittest

import db
from app import app, lag_utdrag
from init_db import init_db

TEST_DATABASE = "test_blogg.db"


class TestApp(unittest.TestCase):

    def setUp(self):
        db.DATABASE = TEST_DATABASE
        init_db(TEST_DATABASE)
        app.config["TESTING"] = True
        self.klient = app.test_client()

    def tearDown(self):
        os.remove(TEST_DATABASE)

    def test_forside_viser_innlegg(self):
        svar = self.klient.get("/")
        self.assertEqual(svar.status_code, 200)
        self.assertIn("Topp 10 hundevennlige restauranter i Oslo", svar.text)

    def test_innleggside_viser_kommentarer(self):
        svar = self.klient.get("/innlegg/1")
        self.assertEqual(svar.status_code, 200)
        self.assertIn("Hundecafe på Løkka", svar.text)

    def test_innlegg_som_ikke_finnes_gir_404(self):
        svar = self.klient.get("/innlegg/999")
        self.assertEqual(svar.status_code, 404)

    def test_taggside_viser_riktige_innlegg(self):
        svar = self.klient.get("/tag/pizza")
        self.assertEqual(svar.status_code, 200)
        self.assertIn("Åpningsfest på Pizza Primitivo", svar.text)
        self.assertNotIn("Hundekafe på Løkka", svar.text)

    def test_ny_kommentar_blir_lagret(self):
        svar = self.klient.post(
            "/innlegg/5/kommentar",
            data={"tittel": "Hei", "tekst": "For en fin brunsj!"},
            follow_redirects=True,
        )
        self.assertEqual(svar.status_code, 200)
        self.assertIn("For en fin brunsj!", svar.text)

    def test_tom_kommentar_blir_ikke_lagret(self):
        svar = self.klient.post("/innlegg/5/kommentar", data={"tittel": "", "tekst": ""})
        self.assertEqual(svar.status_code, 400)
        self.assertIn("Du må skrive en tittel.", svar.text)
        self.assertEqual(len(db.hent_kommentarer(5)), 0)

    def test_script_i_kommentar_blir_escapet(self):
        svar = self.klient.post(
            "/innlegg/5/kommentar",
            data={"tittel": "Test", "tekst": "<script>alert('Hacked!')</script>"},
            follow_redirects=True,
        )
        self.assertNotIn("<script>alert", svar.text)
        self.assertIn("&lt;script&gt;", svar.text)

    def test_nytt_innlegg_med_tagger(self):
        svar = self.klient.post(
            "/innlegg/ny",
            data={"tittel": "Testinnlegg", "tekst": "Litt tekst", "tagger": "hund, Ny"},
            follow_redirects=True,
        )
        self.assertEqual(svar.status_code, 200)
        self.assertIn("Testinnlegg", svar.text)
        self.assertEqual(len(db.hent_innlegg_med_tag("ny")), 1)

    def test_tomt_innlegg_blir_ikke_lagret(self):
        svar = self.klient.post("/innlegg/ny", data={"tittel": "", "tekst": "", "tagger": ""})
        self.assertEqual(svar.status_code, 400)
        self.assertEqual(len(db.hent_alle_innlegg()), 10)

    def test_redigeringsskjema_er_utfylt(self):
        svar = self.klient.get("/innlegg/2/rediger")
        self.assertEqual(svar.status_code, 200)
        self.assertIn('value="arrangement, mat, pizza"', svar.text)

    def test_rediger_innlegg(self):
        svar = self.klient.post(
            "/innlegg/1/rediger",
            data={"tittel": "Endret tittel", "tekst": "Ny tekst", "tagger": "hund"},
            follow_redirects=True,
        )
        self.assertIn("Endret tittel", svar.text)
        self.assertEqual(len(db.hent_tagger(1)), 1)

    def test_utdrag_av_kort_tekst_er_uendret(self):
        self.assertEqual(lag_utdrag("Kort tekst"), "Kort tekst")

    def test_utdrag_av_lang_tekst_blir_kuttet(self):
        utdrag = lag_utdrag("a" * 200)
        self.assertEqual(len(utdrag), 153)
        self.assertTrue(utdrag.endswith("..."))

    def test_404_side_har_egen_tekst(self):
        svar = self.klient.get("/finnes/ikke")
        self.assertEqual(svar.status_code, 404)
        self.assertIn("Fant ikke siden", svar.text)

    def test_bekreftelse_vises_etter_kommentar(self):
        svar = self.klient.post(
            "/innlegg/5/kommentar",
            data={"tittel": "Hei", "tekst": "Fin tekst"},
            follow_redirects=True,
        )
        self.assertIn("Kommentaren er lagret.", svar.text)

    def test_bekreftelsesside_sletter_ikke(self):
        svar = self.klient.get("/innlegg/1/slett")
        self.assertEqual(svar.status_code, 200)
        self.assertIn("Slett innlegg?", svar.text)
        self.assertIsNotNone(db.hent_innlegg(1))

    def test_slett_innlegg(self):
        svar = self.klient.post("/innlegg/1/slett", follow_redirects=True)
        self.assertIn("Innlegget er slettet.", svar.text)
        self.assertIsNone(db.hent_innlegg(1))
        self.assertEqual(len(db.hent_kommentarer(1)), 0)

    def test_slett_kommentar(self):
        svar = self.klient.post("/kommentar/1/slett", follow_redirects=True)
        self.assertIn("Kommentaren er slettet.", svar.text)
        self.assertEqual(len(db.hent_kommentarer(1)), 1)

    def test_innlegg_har_knapp_for_aa_slette_kommentar(self):
        svar = self.klient.get("/innlegg/1")
        self.assertIn("Slett kommentar", svar.text)