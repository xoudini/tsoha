from src.models.base import BaseModel
from src.shared import db

# Required models
from src.models.account import Account
from src.models.tag import Tag
from src.models.response import Response

from typing import List
import datetime

class Thread(BaseModel):

    def __init__(self, uid: int, author: Account, tags: List[Tag], title: str, created: datetime, last_active: datetime = None, response_count: int = None, responses: List[Response] = None):
        self.uid = uid
        self.author = author
        self.tags = tags
        self.title = title
        self.created = "{0:%Y/%m/%d %H:%M}".format(created)
        self.last_active = "{0:%Y/%m/%d %H:%M}".format(last_active) if last_active else None
        self.response_count = response_count
        self.responses = responses
    
    @staticmethod
    def all() -> List['Thread']:
        rows = db.execute_query(
            """
            SELECT 
                Thread.*, 
                Account.username, Account.display_name, 
                COUNT(Response.id) as response_count,
                MAX(Response.created) as last_active
            FROM Thread
            INNER JOIN Account ON Account.id = Thread.author_id
            LEFT JOIN Response ON Response.thread_id = Thread.id
            GROUP BY Thread.id, Account.username, Account.display_name
            ORDER BY last_active DESC;
            """
        )

        result = []

        for row in rows:
            account = Account(row['author_id'], row['username'], row['display_name'])
            tags = Tag.find_by_thread_id(row['id'])
            thread = Thread(row['id'], account, tags, row['title'], row['created'], row['last_active'], row['response_count'])
            result.append(thread)
            # tag = Tag(row['id'], row['title'], row['count'])
            # result.append(tag)
        
        return result
    
    @staticmethod
    def find_by_id(uid: int) -> 'Thread':
        rows = db.execute_query(
            """
            SELECT
                Thread.*,
                Account.username, Account.display_name
            FROM Thread
            INNER JOIN Account ON Account.id = Thread.author_id
            AND Thread.id = %(id)s;
            """,
            {'id': uid}
        )

        try:
            row = rows.pop(0)
            account = Account(row['author_id'], row['username'], row['display_name'])
            tags = Tag.find_by_thread_id(row['id'])
            responses = Response.find_by_thread_id(row['id'])
            thread = Thread(row['id'], account, tags, row['title'], row['created'], responses=responses)
            return thread

        except:
            return None

    @staticmethod
    def create(author_id: int, title: str, content: str, tag_ids: List[int]):
        result = db.execute_update(
            """
            INSERT INTO Thread (author_id, title, created)
            VALUES (%(author_id)s, %(title)s, NOW() AT TIME ZONE 'UTC')
            RETURNING id, created;
            """,
            {'author_id': author_id, 'title': title}
        )

        print("Result of insert:", result)

        if not ('id' in result and 'created' in result):
            return {'error': "Something went wrong."}

        thread_id = result['id']
        created = result['created']

        Response.create(author_id, thread_id, content, created)

        for tag_id in tag_ids:
            db.execute_update(
                """
                INSERT INTO ThreadTag (tag_id, thread_id)
                VALUES (%(tag_id)s, %(thread_id)s);
                """,
                {'tag_id': tag_id, 'thread_id': thread_id}
            )
        
        return {'thread_id': thread_id}
    