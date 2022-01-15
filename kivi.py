from os import name
from flask import Flask, jsonify, request, render_template
import flask
from flask.helpers import flash
from api.user.users import user
from api.database.database import DataCrude
from flask_login import login_user, logout_user, login_required, LoginManager
app = Flask(__name__)
base = DataCrude()
login_manager = LoginManager()

#
#
#
#
#
#
#


@app.route("/")
def Trsa():
    flask.url_for("regpage")
    return jsonify({None: None})


@app.route("/auth", methods=["GET", "POST"])
def autpage():
    if request.method == "GET":
        if request.values.get("name") != None:
            name = request.values.get("name")
            password = request.values.get("psw")
        else:
            return render_template("auth.html")


@app.route("/postmoney", methods=["GET", "POST"])
def postmoney():
    info = request.get_json(force=True)
    if user.UserCheak(info.get("name")) == True:
        if user.UserCheak(info.get("postman")) == True:
            if base.PostMoney(info.get("name"), info.get("postman"),
                              info.get("valuename"), info.get("value"),) == True:
                return jsonify({"info": f"Succes"})
            else:
                return jsonify({"Error": f"insufficient funds"})
        else:
            return jsonify({"Error": f"People not found"})
    else:
        return jsonify({"Error": f"People not found"})


@app.route("/reg", methods=["GET", "POST"])
def regpage():
    if request.method == "GET":
        if request.values.get("name") != None:
            name = request.values.get("name")
            password = request.values.get("psw")
            password_true = request.values.get("psw-repeat")

            cheak = user.UserRegister(name, password, password_true)

            if cheak == "Passwords not same":
                return jsonify({"info": "Your passwords not same"})
            elif cheak == "User with your name alredy registed":
                return jsonify({"info": f"User with name: '{name}' alredy registed"})
            else:
                return jsonify({"info": "You are registed"})

        else:
            return render_template("register.html")


@ app.route("/user/<username>", methods=["GET"])
def mainpage(username):
    return render_template('main.html', name=username, USD="42", UAH="62", RUB="0")


if __name__ == "__main__":
    app.run(debug=True)
