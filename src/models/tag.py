from src.models.base import BaseModel
from src.shared import db

from typing import List

class Tag(BaseModel):

    def __init__(self, uid: int, title: str, count: int):
        self.uid = uid
        self.title = title
        self.count = count
    
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
    def create(title: str):
        db.execute_update(
            """
            INSERT INTO Tag (title) VALUES (%(title)s);
            """,
            {'title': title}
        )


    def __repr__(self):
        return "Tag - id: " + str(self.uid) + ", title: " + self.title
