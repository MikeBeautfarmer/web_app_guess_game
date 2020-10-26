import hashlib
import random
import uuid
from flask import Flask, render_template, request, redirect, url_for, make_response
from models import User, db


app = Flask(__name__)
db.create_all()


@app.route("/", methods=["GET"])
def index():
    session_token = request.cookies.get("session_token")

    if session_token:
        user = db.query(User).filter_by(session_token=session_token).first()
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
    password = request.form.get("user-password")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    geheime_zahl = random.randint(1, 50)

    user = db.query(User).filter_by(email=email).first()

    if not user:
        user = User(name=name, email=email, geheime_zahl=geheime_zahl, password=hashed_password)

        db.add(user)
        db.commit()

    if hashed_password != user.password:
        return "Falsches Passwort! Bitte klicke zurück und versuche es nochmals."

    session_token = str(uuid.uuid4())
    user.session_token = session_token
    db.add(user)
    db.commit()

    response = make_response(redirect(url_for("game")))
    response.set_cookie("session_token", session_token, httponly=True, samesite="Strict")
    return response
    # response = make_response(redirect(url_for("")))


@app.route("/result", methods=["POST"])
def result():
    try:
        rate = int(request.form.get("rate"))
    except ValueError:
        nachricht = "Bitte eine Zahl eingeben!"
        return render_template("result.html", nachricht=nachricht)

    session_token = request.cookies.get("session_token")

    user = db.query(User).filter_by(session_token=session_token).first()

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
