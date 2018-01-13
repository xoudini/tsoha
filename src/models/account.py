from src.models.base import BaseModel
from src.shared import db, pw

from typing import List
from string import ascii_letters

class Account(BaseModel):
    
    def __init__(self, uid: int, username: str, display_name: str = None, admin: bool = False, threads: List = None):
        self.uid = uid
        self.username = username
        self.display_name = display_name
        self.admin = admin
        self.threads = threads

    @staticmethod
    def authenticate(username: str, password: str):
        errors = []

        if not password:
            errors.append("Password can't be empty.")

        if not (1 <= len(username) <= 16):
            errors.append("Username must be between 1 and 16 characters.")

        if any(character not in ascii_letters for character in username):
            errors.append("Username must contain only alphabetic characters.")
        
        if errors:
            return {'errors': errors, 'username': username}

        rows = db.execute_query(
            """
            SELECT * FROM Account WHERE username = %(username)s;
            """,
            {'username': username.lower()}
        )

        try:
            row = rows.pop(0)
            stored_hash = row['password']
            if pw.matches(password, stored_hash):
                account = Account(row['id'], row['username'], row['display_name'], row['admin'])
                return {'user': account}
        
        except:
            pass
        
        return {'errors': ["Incorrect username or password."], 'username': username}

    @staticmethod
    def find_by_id(uid: int) -> 'Account':
        rows = db.execute_query(
            """
            SELECT id, username, display_name, admin FROM Account WHERE id = %(id)s;
            """,
            {'id': uid}
        )

        try:
            row = rows.pop(0)

            # Deferred in order to prevent circular imports.
            from src.models.thread import Thread

            threads = Thread.find_by_author_id(row['id'])
            account = Account(row['id'], row['username'], row['display_name'], row['admin'], threads)
            return account

        except:
            return None
    
    def update(self):
        errors = []

        if Account.find_by_id(self.uid) is None:
            errors.append("Account doesn't exist.")

        # Remove whitespace.
        self.display_name = self.display_name.strip()

        if not (len(self.display_name) <= 50):
            errors.append("Display name must be shorter than 50 characters.")

        if errors:
            return {'errors': errors, 'display_name': self.display_name}

        db.execute_update(
            """
            UPDATE Account SET display_name = %(display_name)s 
            WHERE id = %(id)s;
            """,
            {'id': self.uid, 'display_name': None if not self.display_name else self.display_name}
        )
