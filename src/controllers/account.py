from flask import render_template

from typing import Dict

from src.models.account import Account

class AccountController:
    
    @staticmethod
    def view_for_signin(messages: Dict[str, str] = None):
        return render_template('signin.html', title="Sign in", messages=messages)

    @staticmethod
    def signin(username: str, password: str):
        result = Account.authenticate(username, password)
        return result

    @staticmethod
    def view_for_signup(messages: Dict[str, str] = None):
        return render_template('signup.html', title="Sign up", messages=messages)

    @staticmethod
    def signup(username: str, password: str, repeated_password: str):
        result = Account.create(username, password, repeated_password)
        return result

    @staticmethod
    def view_for_profile(uid: int, messages: Dict[str, str] = None):
        account = Account.find_by_id(uid)
        return render_template('profile.html', title="Profile", messages=messages, account=account)
    
    @staticmethod
    def view_for_edit_profile(uid: int, messages: Dict[str, str] = None):
        account = Account.find_by_id(uid)
        return render_template('edit_profile.html', title="Profile", messages=messages, account=account)

    @staticmethod
    def update(uid: int, display_name: str):
        account = Account(uid, None, display_name)
        result = account.update()
        return result
