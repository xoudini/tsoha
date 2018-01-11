from flask import render_template
from src.controllers.base import BaseController

from src.models.thread import Thread
from src.models.tag import Tag

class ThreadController(BaseController):
    
    @staticmethod
    def index():
        threads = Thread.all()
        return render_template('threads.html', title="Threads", threads=threads)

    @staticmethod
    def view_for_thread(uid: int):
        thread = Thread.find_by_id(uid)
        return render_template('thread.html', title="Thread", thread=thread)
