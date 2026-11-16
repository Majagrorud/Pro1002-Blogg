from flask import Flask, render_template, abort, request, redirect, url_for
import db

app = Flask(__name__)


@app.template_filter("utdrag")
def lag_utdrag(tekst):
    if len(tekst) > 150:
        return tekst[:150] + "..."
    return tekst

def sjekk_kommentar(tittel, tekst):
    feil = []
    if tittel == "":
        feil.append("Du må skrive en tittel.")
    elif len(tittel) > 100:
        feil.append("Tittelen kan ikke være lengre enn 100 tegn.")
    if tekst == "":
        feil.append("Du må skrive en kommentar.")
    elif len(tekst) > 1000:
        feil.append("Kommentaren kan ikke være lengre enn 1000 tegn.")
    return feil


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
    kommentarer = db.hent_kommentarer(innlegg_id)
    return render_template(
        "innlegg.html", innlegg=innlegg, tagger=tagger, kommentarer=kommentarer
    )
@app.route("/tag/<tag_navn>")
def vis_tag(tag_navn):
    innlegg = db.hent_innlegg_med_tag(tag_navn)
    tagger = {}
    for et_innlegg in innlegg:
        tagger[et_innlegg["id"]] = db.hent_tagger(et_innlegg["id"])
    return render_template("tag.html", tag_navn=tag_navn, innlegg=innlegg, tagger=tagger)

@app.route("/innlegg/<int:innlegg_id>/kommentar", methods=["POST"])
def ny_kommentar(innlegg_id):
    innlegg = db.hent_innlegg(innlegg_id)
    if innlegg is None:
        abort(404)

    tittel = request.form["tittel"].strip()
    tekst = request.form["tekst"].strip()
    feil = sjekk_kommentar(tittel, tekst)

    if feil:
        tagger = db.hent_tagger(innlegg_id)
        kommentarer = db.hent_kommentarer(innlegg_id)
        return render_template(
            "innlegg.html",
            innlegg=innlegg,
            tagger=tagger,
            kommentarer=kommentarer,
            feil=feil,
            tittel=tittel,
            tekst=tekst,
        ), 400

    db.lagre_kommentar(innlegg_id, tittel, tekst)
    return redirect(url_for("vis_innlegg", innlegg_id=innlegg_id))