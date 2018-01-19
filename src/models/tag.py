from src.shared import db

from typing import List
from string import ascii_letters, digits

class Tag:

    def __init__(self, uid: int, title: str, count: int = None, threads: List = None):
        self.uid = uid
        self.title = title
        self.count = count
        self.threads = threads
    
    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.uid == other.uid
        return False
    
    
    ### Helper methods.
    
    def validate(self) -> List[str]:
        result = []

        # Remove whitespace.
        self.title = self.title.strip()
        
        if not (1 <= len(self.title) <= 16):
            result.append("Title must be between 1 and 16 characters.")

        if any(character not in ascii_letters + digits for character in self.title):
            result.append("Title must contain only alphanumeric characters.")

        return result


    ### CRUD actions.
    
    @staticmethod
    def find_all() -> List['Tag']:
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

            # Deferred in order to prevent circular imports.
            from src.models.thread import Thread

            threads = Thread.find_by_tag_id(row['id'])
            tag = Tag(row['id'], row['title'], row['count'], threads)
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
        errors = self.validate()

        if errors:
            return {'errors': errors, 'title': self.title}

        if Tag.find_by_title(self.title) is not None:
            return {'errors': ["A tag with that title already exists."], 'title': self.title}

        db.execute_update(
            """
            INSERT INTO Tag (title) VALUES (%(title)s);
            """,
            {'title': self.title}
        )

        # Success.
        return {}
    
    def update(self):
        errors = self.validate()

        if errors:
            return {'errors': errors, 'title': self.title}

        tag_with_same_title = Tag.find_by_title(self.title)

        if tag_with_same_title is not None:
            if tag_with_same_title.uid == self.uid:
                return {'warnings': ["The title is unchanged."], 'title': self.title}
            else:
                return {'errors': ["A tag with that title already exists."], 'title': self.title}

        if Tag.find_by_id(self.uid) is None:
            return {'errors': ["Tag doesn't exist."], 'title': self.title}

        db.execute_update(
            """
            UPDATE Tag SET title = %(title)s 
            WHERE id = %(id)s;
            """,
            {'id': self.uid, 'title': self.title}
        )

        # Success.
        return {}
    
    def delete(self):
        if Tag.find_by_id(self.uid) is None:
            return {'errors': ["Tag doesn't exist."]}

        db.execute_update(
            """
            DELETE FROM Tag 
            WHERE id = %(id)s;
            """,
            {'id': self.uid}
        )

        # Success.
        return {}
