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
        self.response_count = response_count - 1 if response_count else None # Thread starter shouldn't count as a response.
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
    def find_by_author_id(author_id: int) -> List['Thread']:
        rows = db.execute_query(
            """
            SELECT
                Thread.id, Thread.title, Thread.created,
                COUNT(Response.id) as response_count,
                MAX(Response.created) as last_active
            FROM Thread
            INNER JOIN Account ON Account.id = Thread.author_id
            AND Thread.author_id = %(author_id)s
            LEFT JOIN Response ON Response.thread_id = Thread.id
            GROUP BY Thread.id
            ORDER BY created DESC
            LIMIT 5;
            """,
            {'author_id': author_id}
        )

        result = []

        for row in rows:
            tags = Tag.find_by_thread_id(row['id'])
            thread = Thread(row['id'], None, tags, row['title'], row['created'], row['last_active'], row['response_count'])
            result.append(thread)
        
        return result
    
    @staticmethod
    def author_for_thread(uid: int) -> int:
        rows = db.execute_query(
            """
            SELECT author_id FROM Thread
            WHERE id = %(id)s;
            """,
            {'id': uid}
        )

        try:
            row = rows.pop(0)
            return row['author_id']
        except:
            return None

    @staticmethod
    def create(author_id: int, title: str, content: str, tag_ids: List[int]):
        try:
            tag_ids = list(int(tag_id) for tag_id in tag_ids)
        except:
            return {'error': "Invalid formatting on tags.", 'title': title, 'content': content, 'tag_ids': tag_ids}

        if not title:
            return {'error': "Title can't be empty.", 'content': content, 'tag_ids': tag_ids}

        if not content:
            return {'error': "Content can't be empty.", 'title': title, 'tag_ids': tag_ids}

        result = db.execute_update(
            """
            INSERT INTO Thread (author_id, title, created)
            VALUES (%(author_id)s, %(title)s, NOW() AT TIME ZONE 'UTC')
            RETURNING id, created;
            """,
            {'author_id': author_id, 'title': title}
        )

        if not ('id' in result and 'created' in result):
            return {'error': "Something went wrong.", 'title': title, 'content': content, 'tag_ids': tag_ids}

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

    @staticmethod
    def update(uid: int, title: str, tag_ids: List[int]):
        try:
            tag_ids = list(int(tag_id) for tag_id in tag_ids)
        except:
            return {'error': "Invalid formatting on tags.", 'title': title, 'tag_ids': tag_ids}

        if not title:
            return {'error': "Title can't be empty.", 'tag_ids': tag_ids}

        db.execute_update(
            """
            UPDATE Thread SET title = %(title)s
            WHERE id = %(id)s;
            """,
            {'id': uid, 'title': title}
        )

        existing_tags = Tag.find_by_thread_id(uid)
        existing_tag_ids = list(t.uid for t in existing_tags) if existing_tags else []

        for tag_id in tag_ids:
            if tag_id not in existing_tag_ids:
                db.execute_update(
                    """
                    INSERT INTO ThreadTag (tag_id, thread_id)
                    VALUES (%(tag_id)s, %(thread_id)s);
                    """,
                    {'tag_id': tag_id, 'thread_id': uid}
                )
            
        for existing_tag_id in existing_tag_ids:
            if existing_tag_id not in tag_ids:
                db.execute_update(
                    """
                    DELETE FROM ThreadTag
                    WHERE tag_id = %(tag_id)s
                    AND thread_id = %(thread_id)s;
                    """,
                    {'tag_id': existing_tag_id, 'thread_id': uid}
                )

    @staticmethod
    def delete(uid: int):
        db.execute_update(
            """
            DELETE FROM Thread
            WHERE id = %(id)s;
            """,
            {'id': uid}
        )
    