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