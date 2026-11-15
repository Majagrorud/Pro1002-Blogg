from flask import Flask, render_template, abort
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
    tagger = {}
    for et_innlegg in innlegg:
        tagger[et_innlegg["id"]] = db.hent_tagger(et_innlegg["id"])
    return render_template("index.html", innlegg=innlegg, tagger=tagger)

@app.route("/innlegg/<int:innlegg_id>")
def vis_innlegg(innlegg_id):
    innlegg = db.hent_innlegg(innlegg_id)
    if innlegg is None:
        abort(404)
    tagger = db.hent_tagger(innlegg_id)
    return render_template("innlegg.html", innlegg=innlegg, tagger=tagger)