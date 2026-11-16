import sqlite3
from datetime import date

DATABASE = "blogg.db"


def hent_tilkobling():
    """Åpner databasen og slår på fremmednøkler."""
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def hent_alle_innlegg():
    """Henter alle innlegg, nyeste først."""
    con = hent_tilkobling()
    innlegg = con.execute("SELECT * FROM innlegg ORDER BY dato DESC").fetchall()
    con.close()
    return innlegg


def hent_tagger(innlegg_id):
    """Henter taggene til ett innlegg, sortert etter navn."""
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
    """Henter ett innlegg. Returnerer None hvis det ikke finnes."""
    con = hent_tilkobling()
    innlegg = con.execute(
        "SELECT * FROM innlegg WHERE id = ?", (innlegg_id,)
    ).fetchone()
    con.close()
    return innlegg


def hent_kommentarer(innlegg_id):
    """Henter kommentarene til ett innlegg, eldste først."""
    con = hent_tilkobling()
    kommentarer = con.execute(
        "SELECT * FROM kommentarer WHERE innlegg_id = ? ORDER BY dato",
        (innlegg_id,),
    ).fetchall()
    con.close()
    return kommentarer


def hent_innlegg_med_tag(tag_navn):
    """Henter alle innlegg med en bestemt tag, nyeste først."""
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


def lagre_kommentar(innlegg_id, tittel, tekst):
    """Lagrer en ny kommentar med dagens dato."""
    dato = date.today().isoformat()
    con = hent_tilkobling()
    con.execute(
        "INSERT INTO kommentarer (innlegg_id, tittel, dato, tekst) VALUES (?, ?, ?, ?)",
        (innlegg_id, tittel, dato, tekst),
    )
    con.commit()
    con.close()


def lagre_innlegg(tittel, tekst):
    """Lagrer et nytt innlegg med dagens dato. Returnerer id til innlegget."""
    dato = date.today().isoformat()
    con = hent_tilkobling()
    cur = con.execute(
        "INSERT INTO innlegg (tittel, dato, tekst) VALUES (?, ?, ?)",
        (tittel, dato, tekst),
    )
    con.commit()
    nytt_id = cur.lastrowid
    con.close()
    return nytt_id


def lagre_tagger(innlegg_id, tagger):
    """Lagrer taggene og kobler dem til innlegget."""
    con = hent_tilkobling()
    for navn in tagger:
        con.execute("INSERT OR IGNORE INTO tagger (navn) VALUES (?)", (navn,))
        tag = con.execute("SELECT id FROM tagger WHERE navn = ?", (navn,)).fetchone()
        con.execute(
            "INSERT OR IGNORE INTO innlegg_tagger (innlegg_id, tag_id) VALUES (?, ?)",
            (innlegg_id, tag["id"]),
        )
    con.commit()
    con.close()


def oppdater_innlegg(innlegg_id, tittel, tekst):
    """Endrer tittel og tekst på et innlegg."""
    con = hent_tilkobling()
    con.execute(
        "UPDATE innlegg SET tittel = ?, tekst = ? WHERE id = ?",
        (tittel, tekst, innlegg_id),
    )
    con.commit()
    con.close()


def fjern_tagger(innlegg_id):
    """Fjerner alle taggene fra et innlegg."""
    con = hent_tilkobling()
    con.execute("DELETE FROM innlegg_tagger WHERE innlegg_id = ?", (innlegg_id,))
    con.commit()
    con.close()

def slett_innlegg(innlegg_id):
    """Sletter et innlegg med kommentarer og taggkoblinger."""
    con = hent_tilkobling()
    con.execute("DELETE FROM kommentarer WHERE innlegg_id = ?", (innlegg_id,))
    con.execute("DELETE FROM innlegg_tagger WHERE innlegg_id = ?", (innlegg_id,))
    con.execute("DELETE FROM innlegg WHERE id = ?", (innlegg_id,))
    con.commit()
    con.close()