import sqlite3

DATABASE = "blogg.db"


def hent_tilkobling():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def hent_alle_innlegg():
    con = hent_tilkobling()
    innlegg = con.execute("SELECT * FROM innlegg ORDER BY dato DESC").fetchall()
    con.close()
    return innlegg


def hent_tagger(innlegg_id):
    con = hent_tilkobling()
    tagger = con.execute(
        "SELECT tagger.navn FROM tagger "
        "JOIN innlegg_tagger ON tagger.id = innlegg_tagger.tag_id "
        "WHERE innlegg_tagger.innlegg_id = ? "
        "ORDER BY tagger.navn",
        (innlegg_id,),
    ).fetchall()
    con.close()
    return tagger


def hent_innlegg(innlegg_id):
    con = hent_tilkobling()
    innlegg = con.execute(
        "SELECT * FROM innlegg WHERE id = ?", (innlegg_id,)
    ).fetchone()
    con.close()
    return innlegg


def hent_kommentarer(innlegg_id):
    con = hent_tilkobling()
    kommentarer = con.execute(
        "SELECT * FROM kommentarer WHERE innlegg_id = ? ORDER BY dato",
        (innlegg_id,),
    ).fetchall()
    con.close()
    return kommentarer


def hent_innlegg_med_tag(tag_navn):
    con = hent_tilkobling()
    innlegg = con.execute(
        "SELECT innlegg.* FROM innlegg "
        "JOIN innlegg_tagger ON innlegg.id = innlegg_tagger.innlegg_id "
        "JOIN tagger ON tagger.id = innlegg_tagger.tag_id "
        "WHERE tagger.navn = ? "
        "ORDER BY innlegg.dato DESC",
        (tag_navn,),
    ).fetchall()
    con.close()
    return innlegg