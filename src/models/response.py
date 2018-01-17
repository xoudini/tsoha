from src.shared import db

# Required models
from src.models.account import Account

from typing import List
import datetime

class Response:
    
    def __init__(self, uid: int, author: Account, content: str, created: datetime):
        self.uid = uid
        self.author = author
        self.content = content
        self.created = "{0:%Y/%m/%d %H:%M}".format(created)
    

    ### Helper methods.

    @staticmethod
    def validate(content: str):
        result = []

        if not (10 <= len(content) <= 1000):
            result.append("Content must be between 10 and 1000 characters.")

        return result


    ### CRUD actions.

    @staticmethod
    def find_by_thread_id(thread_id: int) -> List['Response']:
        rows = db.execute_query(
            """
            SELECT 
                Response.*,
                Account.username, Account.display_name
            FROM Response
            INNER JOIN Account ON Account.id = Response.author_id
            AND Response.thread_id = %(thread_id)s
            ORDER BY created ASC;
            """,
            {'thread_id': thread_id}
        )

        result = []

        for row in rows:
            account = Account(row['author_id'], row['username'], row['display_name'])
            response = Response(row['id'], account, row['content'], row['created'])
            result.append(response)
        
        return result
    
    @staticmethod
    def create(author_id: int, thread_id: int, content: str, created: datetime = None):
        # Remove whitespace.
        content = content.strip()

        errors = Response.validate(content)
        
        if errors:
            return {'errors': errors, 'content': content}

        if created is None:
            created = db.get_timestamp()

        db.execute_update(
            """
            INSERT INTO Response (author_id, thread_id, content, created)
            VALUES (%(author_id)s, %(thread_id)s, %(content)s, %(created)s);
            """,
            {'author_id': author_id, 'thread_id': thread_id, 'content': content, 'created': created}
        )

        # Success.
        return {}
