from flask import Flask, render_template
import db

app = Flask(__name__)


@app.template_filter("utdrag")
def lag_utdrag(tekst):
    if len(tekst) > 150:
        return tekst[:150] + "..."
    return tekst


@app.route("/")
def forside():
    innlegg = db.hent_alle_innlegg()
    return render_template("index.html", innlegg=innlegg)