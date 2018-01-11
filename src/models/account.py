from src.models.base import BaseModel
from src.shared import db, pw

from string import ascii_letters

class Account(BaseModel):
    
    def __init__(self, uid: int, username: str, display_name: str = None, admin: bool = False):
        self.uid = uid
        self.username = username
        self.display_name = display_name
        self.admin = admin

    @staticmethod
    def authenticate(username: str, password: str):
        if not (username and password):
            return {'error': "Neither field can be empty.", 'username': username}

        if not (1 <= len(username) <= 16):
            return {'error': "Username must be between 1 and 16 characters.", 'username': username}

        if any(character not in ascii_letters for character in username):
            return {'error': "Username can only contain alphabetic characters.", 'username': username}

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
        
        return {'error': "Incorrect username or password.", 'username': username}

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
            account = Account(row['id'], row['username'], row['display_name'], row['admin'])
            return account

        except:
            return None
    
    def update(self):
        if Account.find_by_id(self.uid) is None:
            return {'error': "Account doesn't exist.", 'display_name': self.display_name}

        if not (len(self.display_name) <= 50):
            return {'error': "Display name must be shorter than 50 characters.", 'display_name': self.display_name}

        db.execute_update(
            """
            UPDATE Account SET display_name = %(display_name)s 
            WHERE id = %(id)s;
            """,
            {'id': self.uid, 'display_name': None if not self.display_name else self.display_name}
        )
