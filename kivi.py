from flask import Flask, jsonify, request
from api.user.users import user
from api.database.database import DataCrude
from flask_login import login_user, logout_user, login_required, LoginManager
app = Flask(__name__)
base = DataCrude()
login_manager = LoginManager()
login_manager.init_app(app)
#
#
#
#
#
#
#


@app.route("/auth", methods=["GET", "POST"])
def autpage():
    info = request.get_json(force=True)
    if user.UserLogin(info) == True:
        # login_user(user)
        return jsonify({"info": "logined"})
    else:
        return jsonify({"info": "anlogin"})


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


@app.route("/reg", methods=["POST"])
def regpage():
    info = request.get_json(force=True)
    cheak = user.UserRegister(info)
    if cheak == "Passwords not same":
        return jsonify({"info": "Your passwords not same"})
    elif cheak == "User with your name alredy registed":
        return jsonify({"info": f"User with name: '{info.get('login')}' alredy registed"})
    else:
        return jsonify({"info": "You are registed"})


@app.route("/user/<username>", methods=["GET"])
def mainpage(username):
    if user.UserLogin(username) == True:
        b = "1212"
        return jsonify({"info": f"{b}"})
    else:
        return jsonify({"info": "c"})


if __name__ == "__main__":
    app.run(debug=True)
