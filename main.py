from flask import Flask, render_template, request, redirect, url_for, make_response

from models import User, db

import random

app = Flask(__name__)
db.create_all()


@app.route("/", methods=["GET"])
def index():
    email_adress = request.cookies.get("email")

    if email_adress:
        user = db.query(User).filter_by(email=email_adress).first()
    else:
        user = None

    return render_template("index2.html", user=user)


@app.route("/game", methods=["GET"])
def game():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")

    geheime_zahl = random.randint(1, 50)

    user = db.query(User).filter_by(email=email).first()

    if not user:
        user = User(name=name, email=email, geheime_zahl=geheime_zahl)

        db.add(user)
        db.commit()

    response = make_response(redirect(url_for("game")))
    response.set_cookie("email", email)

    return response
    # response = make_response(redirect(url_for("")))


@app.route("/result", methods=["POST"])
def result():
    try:
        rate = int(request.form.get("rate"))
    except ValueError:
        nachricht = "Bitte eine Zahl eingeben!"
        return render_template("result.html", nachricht=nachricht)

    email_adress = request.cookies.get("email")

    user = db.query(User).filter_by(email=email_adress).first()

    if rate == user.geheime_zahl:  # Wenn geheime Zahl erraten wird!
        nachricht = "Korrekt! Die geheime Zahl ist {0}".format(str(user.geheime_zahl))  # Nachricht Ausgabe
        response = make_response(render_template("result2.html", nachricht=nachricht))  # Nachricht in result2.html
        neues_geheimnis = random.randint(1, 50)
        user.geheime_zahl = neues_geheimnis
        db.add(user)
        db.commit()
        return response

    elif rate < user.geheime_zahl:  # Wenn Ratezahl kleiner als geheime Zahl
        nachricht = "Falsch! . . .   Versuche eine höhere Zahl"  # Nachricht Ausgabe
        return render_template("result.html", nachricht=nachricht)  # Nachricht in result.html
    elif rate > user.geheime_zahl:  # Wenn Ratezahl größer als geheime Zahl
        nachricht = "Falsch! . . .   Versuche eine niedrigere Zahl"  # Nachricht Ausgabe
        return render_template("result.html", nachricht=nachricht)  # Nachricht in result.html


if __name__ == '__main__':
    app.run(debug=True)
