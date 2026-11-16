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


def les_tagger(tekst):
    tagger = []
    for bit in tekst.split(","):
        navn = bit.strip().lower()
        if navn != "" and navn not in tagger:
            tagger.append(navn)
    return tagger

def sjekk_innlegg(tittel, tekst):
    feil = []
    if tittel == "":
        feil.append("Du må skrive en tittel.")
    elif len(tittel) > 150:
        feil.append("Tittelen kan ikke være lengre enn 150 tegn.")
    if tekst == "":
        feil.append("Du må skrive en tekst.")
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


@app.route("/innlegg/ny", methods=["GET", "POST"])
def nytt_innlegg():
    if request.method == "POST":
        tittel = request.form["tittel"].strip()
        tekst = request.form["tekst"].strip()
        tagger_tekst = request.form["tagger"]
        feil = sjekk_innlegg(tittel, tekst)

        if feil:
            return render_template(
                "skjema.html",
                overskrift="Nytt innlegg",
                feil=feil,
                tittel=tittel,
                tekst=tekst,
                tagger_tekst=tagger_tekst,
            ), 400

        innlegg_id = db.lagre_innlegg(tittel, tekst)
        db.lagre_tagger(innlegg_id, les_tagger(tagger_tekst))
        return redirect(url_for("vis_innlegg", innlegg_id=innlegg_id))

    return render_template("skjema.html", overskrift="Nytt innlegg")

@app.route("/innlegg/<int:innlegg_id>/rediger", methods=["GET", "POST"])
def rediger_innlegg(innlegg_id):
    innlegg = db.hent_innlegg(innlegg_id)
    if innlegg is None:
        abort(404)

    if request.method == "POST":
        tittel = request.form["tittel"].strip()
        tekst = request.form["tekst"].strip()
        tagger_tekst = request.form["tagger"]
        feil = sjekk_innlegg(tittel, tekst)

        if feil:
            return render_template(
                "skjema.html",
                overskrift="Rediger innlegg",
                feil=feil,
                tittel=tittel,
                tekst=tekst,
                tagger_tekst=tagger_tekst,
            ), 400

        db.oppdater_innlegg(innlegg_id, tittel, tekst)
        db.fjern_tagger(innlegg_id)
        db.lagre_tagger(innlegg_id, les_tagger(tagger_tekst))
        return redirect(url_for("vis_innlegg", innlegg_id=innlegg_id))

    navn = []
    for tag in db.hent_tagger(innlegg_id):
        navn.append(tag["navn"])
    tagger_tekst = ", ".join(navn)

    return render_template(
        "skjema.html",
        overskrift="Rediger innlegg",
        tittel=innlegg["tittel"],
        tekst=innlegg["tekst"],
        tagger_tekst=tagger_tekst,
    )

@app.errorhandler(404)
def side_finnes_ikke(feil):
    return render_template("404.html"), 404