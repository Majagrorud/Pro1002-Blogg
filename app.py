from flask import Flask, render_template
import db

app = Flask(__name__)


@app.route("/")
def forside():
    innlegg = db.hent_alle_innlegg()
    return render_template("index.html", innlegg=innlegg)