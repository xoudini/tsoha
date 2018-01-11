from src.models.base import BaseModel
from src.shared import db

from typing import List

class Tag(BaseModel):

    def __init__(self, uid: int, title: str, count: int = None):
        self.uid = uid
        self.title = title
        self.count = count
    
    def valid(self) -> bool:
        return self.title
    
    @staticmethod
    def all() -> List['Tag']:
        rows = db.execute_query(
            """
            SELECT Tag.*, COUNT(ThreadTag.tag_id) as count FROM Tag
            LEFT JOIN ThreadTag ON ThreadTag.tag_id = Tag.id
            GROUP BY Tag.id
            ORDER BY count DESC, title;
            """
        )

        result = []

        for row in rows:
            tag = Tag(row['id'], row['title'], row['count'])
            result.append(tag)
        
        return result

    @staticmethod
    def find_by_id(uid: int) -> 'Tag':
        rows = db.execute_query(
            """
            SELECT *, (
                SELECT COUNT(*) FROM ThreadTag
                WHERE ThreadTag.tag_id = %(id)s
            ) AS count FROM Tag
            WHERE id = %(id)s;
            """,
            {'id': uid}
        )

        try:
            row = rows.pop(0)
            tag = Tag(row['id'], row['title'], row['count'])
            return tag

        except:
            return None
    
    @staticmethod
    def find_by_thread_id(thread_id: int) -> List['Tag']:
        rows = db.execute_query(
            """
            SELECT Tag.* FROM Tag
            INNER JOIN ThreadTag ON ThreadTag.thread_id = %(thread_id)s
            AND ThreadTag.tag_id = Tag.id
            ORDER BY title;
            """,
            {'thread_id': thread_id}
        )

        result = []

        for row in rows:
            tag = Tag(row['id'], row['title'])
            result.append(tag)
        
        return result
    
    @staticmethod
    def find_by_title(title: str) -> 'Tag':
        rows = db.execute_query(
            """
            SELECT *, (
                SELECT COUNT(*) FROM ThreadTag
                WHERE ThreadTag.tag_id = Tag.id
            ) AS count FROM Tag
            WHERE title = %(title)s;
            """,
            {'title': title}
        )

        try:
            row = rows.pop(0)
            tag = Tag(row['id'], row['title'], row['count'])
            return tag

        except:
            return None
    
    def create(self):
        if not self.valid():
            return {'error': "Invalid tag.", 'title': self.title}

        if Tag.find_by_title(self.title) is not None:
            return {'error': "Tag with that title already exists.", 'title': self.title}

        db.execute_update(
            """
            INSERT INTO Tag (title) VALUES (%(title)s);
            """,
            {'title': self.title}
        )
    
    def update(self):
        if not self.valid():
            return {'error': "Invalid tag.", 'title': self.title}

        if Tag.find_by_title(self.title) is not None:
            return {'error': "Tag with that title already exists.", 'title': self.title}

        if Tag.find_by_id(self.uid) is None:
            return {'error': "Tag doesn't exist.", 'title': self.title}

        db.execute_update(
            """
            UPDATE Tag SET title = %(title)s 
            WHERE id = %(id)s;
            """,
            {'id': self.uid, 'title': self.title}
        )
    
    def delete(self):
        if Tag.find_by_id(self.uid) is None:
            return {'error': "Tag doesn't exist."}

        db.execute_update(
            """
            DELETE FROM Tag 
            WHERE id = %(id)s;
            """,
            {'id': self.uid}
        )



    def __repr__(self):
        return "Tag - id: " + str(self.uid) + ", title: " + self.title
