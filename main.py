from flask import Flask, render_template, request, make_response
import random

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    geheime_zahl = request.cookies.get("geheime_zahl")

    response = make_response(render_template("index.html"))
    if not geheime_zahl:
        neues_geheimnis = random.randint(1, 50)
        response.set_cookie("geheime_zahl", str(neues_geheimnis))

    return response


@app.route("/result", methods=["POST"])
def result():
    try:
        rate = int(request.form.get("rate"))
    except ValueError:
        nachricht = "Bitte eine Zahl eingeben!"
        return render_template("result.html", nachricht=nachricht)

    #  rate = int(request.form.get("rate"))
    geheime_zahl = int(request.cookies.get("geheime_zahl"))  # !!!!!!!!!!!!!!!!   FRAGEN   !!!!!!!!!!!!!!!!!!!!!!!!!!

    if rate == geheime_zahl:  # Wenn geheime Zahl erraten wird!
        nachricht = "Korrekt! Die geheime Zahl ist {0}".format(str(geheime_zahl))  # Nachricht Ausgabe
        response = make_response(render_template("result2.html", nachricht=nachricht))  # Nachricht in result.html
        response.set_cookie("geheime_zahl", str(random.randint(1, 50)))  # Neue geheime Zahl wird erstellt
        return response
    elif rate < geheime_zahl:  # Wenn Ratezahl kleiner als geheime Zahl
        nachricht = "Falsch! . . .   Versuche eine höhere Zahl"  # Nachricht Ausgabe
        return render_template("result.html", nachricht=nachricht)  # Nachricht in result.html
    elif rate > geheime_zahl:  # Wenn Ratezahl größer als geheime Zahl
        nachricht = "Falsch! . . .   Versuche eine niedrigere Zahl"  # Nachricht Ausgabe
        return render_template("result.html", nachricht=nachricht)  # Nachricht in result.html


if __name__ == '__main__':
    app.run(debug=True)
