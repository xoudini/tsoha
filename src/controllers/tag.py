from flask import render_template

from typing import Dict

from src.models.tag import Tag

class TagController:
    
    ### View rendering.

    @staticmethod
    def view_for_tags():
        tags = Tag.find_all()
        return render_template('tags.html', title="Tags", tags=tags)

    @staticmethod
    def view_for_tag(uid: int):
        tag = Tag.find_by_id(uid)
        return render_template('tag.html', title="Tag", tag=tag)

    @staticmethod
    def view_for_new_tag(messages: Dict[str, str] = None):
        return render_template('new_tag.html', title="New tag", messages=messages)

    @staticmethod
    def view_for_edit_tag(uid: int, messages: Dict[str, str] = None):
        tag = Tag.find_by_id(uid)
        return render_template('edit_tag.html', title="Edit tag", tag=tag, messages=messages)


    ### Database updates.

    @staticmethod
    def create(title: str):
        tag = Tag(None, title)
        result = tag.create()
        return result

    @staticmethod
    def update(uid: int, title: str):
        tag = Tag(uid, title)
        result = tag.update()
        return result

    @staticmethod
    def delete(uid: int):
        tag = Tag(uid, None)
        result = tag.delete()
        return result
