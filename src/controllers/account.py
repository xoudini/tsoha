from flask import render_template
from src.controllers.base import BaseController

from typing import Dict

from src.models.account import Account

class AccountController(BaseController):
    
    @staticmethod
    def view_for_signin(messages: Dict[str, str] = None):
        return render_template('signin.html', title="Sign in", messages=messages)

    @staticmethod
    def signin(username: str, password: str):
        result = Account.authenticate(username, password)
        return result

    @staticmethod
    def view_for_profile(uid: int, messages: Dict[str, str] = None):
        account = Account.find_by_id(uid)
        return render_template('profile.html', title="Profile", messages=messages, account=account)
