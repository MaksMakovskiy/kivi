# 01010111 00101110 01010101 00101110 01000011 00101110

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


#    #     #   #    #    ####     #
#    #     #   #    #   #         #
#    #  #  #   #    #   #         #
#     ## ## .   #### .   #### .   #


@app.route("/")
def Trsa():
    flask.url_for("regpage")
    return jsonify({None: None})


@app.route("/auth", methods=["GET"])
def autpage():
    if request.values.get("name") != None:
        name = request.values.get("name")
        password = request.values.get("psw")
        return None
    else:
        return render_template("auth.html")


@app.route("/postmoney", methods=["GET"])
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
    base.DoDIctUsers()
    if username in base.usersname:
        print(base.usersname)
        return render_template('main.html', name=username, USD=base.users[username]["money"]["USD"], UAH=base.users[username]["money"]["UAH"], RUB=base.users[username]["money"]["RUB"])
    else:
        return jsonify({"info": f"No user with name {username}"})


if __name__ == "__main__":
    app.run(debug=True, host="192.168.0.103")
