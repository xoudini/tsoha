from src.models.base import BaseModel
from src.shared import db, pw

class Account(BaseModel):
    
    def __init__(self, uid: int, username: str, display_name: str = None, admin: bool = False):
        self.uid = uid
        self.username = username
        # self.password_hash = password_hash
        self.display_name = display_name
        self.admin = admin

    @staticmethod
    def authenticate(username: str, password: str):
        if not (username and password):
            return {'error': "Neither field can be empty.", 'username': username}

        rows = db.execute_query(
            """
            SELECT * FROM Account WHERE username = %(username)s;
            """,
            {'username': username}
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
