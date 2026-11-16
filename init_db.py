import sqlite3

DATABASE = "blogg.db"


def init_db(database=DATABASE):
    con = sqlite3.connect(database)

    with open("schema.sql", encoding="utf-8") as fil:
        con.executescript(fil.read())

    with open("data.sql", encoding="utf-8") as fil:
        con.executescript(fil.read())

    con.commit()
    con.close()


if __name__ == "__main__":
    init_db()
    print("Databasen er laget!")