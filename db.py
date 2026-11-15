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