from sqlite3.dbapi2 import Error
from flask import request, jsonify
from ..database.database import DataCrude
from flask_login import UserMixin


base = DataCrude()


class UserCrude(UserMixin):
    def __init__(self) -> None:
        ...

    def UserCheak(self, name: str):
        base.RecordAllName()
        if name in base.usersname:
            return True
        else:
            return None

    def UserLogin(self, data: dict) -> str | None:
        self.name = data.get("name")
        self.password = str(data.get("password"))
        base.DoDIctUsers()
        if self.name in base.usersname:
            if base.users[self.name]["password"] == self.password:
                return True
            else:
                return False
        else:
            return False

    def UserRegister(self, name, psw, pswr):
        self.name = name
        self.password = psw
        self.password_true = pswr
        if self.password != self.password_true:
            return "Passwords not same"
        else:
            if self.UserCheak(self.name) == None:
                base.PrintUserToBase(self.name, self.password)
            else:
                return "User with your name alredy registed"


user = UserCrude()
