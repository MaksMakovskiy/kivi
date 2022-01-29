# 01010111 00101110 01010101 00101110 01000011 00101110

from os import name, urandom
from flask import Flask, jsonify, request, render_template, redirect, url_for, session
import flask
from flask.helpers import flash
from api.user.users import user, Userlogin
from api.database.database import DataCrude
from flask_login import login_user, logout_user, login_required, LoginManager
app = Flask(__name__)
base = DataCrude()
login_manager = LoginManager(app)

app.config['SECRET_KEY'] = '\\n\\xf6\\x8dn\\xe7C\\xc6b\\x80\\xb8\\xb5\\xc5x\\x9e!4\\xe58\\xbb\\xf0j\\xfa\\xcfW'


#    #     #   #    #    ####     #
#    #     #   #    #   #         #
#    #  #  #   #    #   #         #
#     ## ## .   #### .   #### .   #


@login_manager.user_loader
def load_user(name):
    return Userlogin(name)


@app.route("/")
def start():
    return redirect(url_for("autpage"))


@app.route("/sing", methods=["GET"])
def autred():
    logout_user()
    session["name"] = None
    return redirect(url_for("autpage"))


@app.route("/auth", methods=["GET"])
def autpage():
    base.DoDIctUsers()
    base.RecordAllName()
    if request.values.get("name") != None:
        name = request.values.get("name")
        password = request.values.get("psw")
        if name in base.usersname:
            if password == base.users[name]["password"]:
                print(name)
                userlog = Userlogin(name)
                login_user(userlog)
                session["name"] = name
                return redirect(url_for("mainpage", username=name))
            else:
                flash('Name or password invalid!')
                return render_template("auth.html")
        else:
            flash('Name or password invalid!')
            return render_template("auth.html")
    else:
        return render_template("auth.html")


@app.route("/postmoney", methods=["GET"])
def postmoney():
    name = request.values.get("name")
    postman = request.values.get("postman")
    value = request.values.get("value")
    valuename = request.values.get("valuename")
    if name:
        if user.UserCheak(name) == True:
            if user.UserCheak(postman) == True:
                if base.PostMoney(name, postman, valuename, value,) == True:
                    return jsonify({"info": f"Succes"})
                else:
                    return jsonify({"Error": f"insufficient funds"})
            else:
                return jsonify({"Error": f"People not found"})
        else:
            return jsonify({"Error": f"People not found"})
    else:
        return render_template("postmoney.html")


@app.route("/reg", methods=["GET", "POST"])
def regpage():
    base.DoDIctUsers()
    print(base.users)
    if request.method == "GET":
        if request.values.get("name") != None:
            name = request.values.get("name")
            password = request.values.get("psw")
            password_true = request.values.get("psw-repeat")

            cheak = user.UserRegister(name, password, password_true)

            if cheak == "Passwords not same":
                flash("Your passwords not same")
                return render_template("register.html")
            elif cheak == "User with your name alredy registed":
                flash(f"User with name: '{name}' alredy registed")
                return render_template("register.html")
            else:
                session["name"] = name
                userlog = Userlogin(name)
                login_user(userlog)
                return redirect(url_for("mainpage", username=name))
        else:
            return render_template("register.html")


@ app.route("/user/<username>", methods=["GET"])
@login_required
def mainpage(username):
    if session["name"] == username:
        print(session["name"], type(session["name"]))
        base.DoDIctUsers()
        if username in base.usersname:
            return render_template('main.html', name=username, USD=base.users[username]["money"]["USD"], UAH=base.users[username]["money"]["UAH"], RUB=base.users[username]["money"]["RUB"])
        else:
            return jsonify({"info": f"No user with name {username}"})
    else:
        return render_template("dontdothis.html")


if __name__ == "__main__":
    app.run(debug=True, host="192.168.0.103")
