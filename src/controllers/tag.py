from flask import render_template
from src.controllers.base import BaseController

from src.models.tag import Tag

class TagController(BaseController):
    
    @staticmethod
    def index():
        tags = Tag.all()
        return render_template('tags.html', title="Tags", tags=tags)

    @staticmethod
    def view_for_tag(uid: int):
        tag = Tag.find_by_id(uid)
        return render_template('tag.html', title="Tag", tag=tag)

    @staticmethod
    def view_for_new_tag():
        return render_template('newtag.html', title="New tag")

    @staticmethod
    def create_tag(title: str):
        Tag.create(title)
