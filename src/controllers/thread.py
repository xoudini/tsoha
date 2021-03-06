from flask import render_template

from typing import Dict, List

from src.models.thread import Thread
from src.models.tag import Tag

class ThreadController:

    ### View rendering.
    
    @staticmethod
    def view_for_threads():
        threads = Thread.find_all()
        return render_template('threads.html', title="Threads", threads=threads)

    @staticmethod
    def view_for_thread(uid: int, messages: Dict[str, str] = None):
        thread = Thread.find_by_id(uid)
        return render_template('thread.html', title="Thread", thread=thread, messages=messages)

    @staticmethod
    def view_for_new_thread(messages: Dict[str, str] = None):
        tags = Tag.find_all()
        return render_template('new_thread.html', title="New thread", tags=tags, messages=messages)

    @staticmethod
    def view_for_edit_thread(uid: int, messages: Dict[str, str] = None):
        thread = Thread.find_by_id(uid)
        tags = Tag.find_all()
        return render_template('edit_thread.html', title="Edit thread", thread=thread, tags=tags, messages=messages)


    ### Database updates.

    @staticmethod
    def create(user_id: int, title: str, content: str, tag_ids: List[int]):
        result = Thread.create(user_id, title, content, tag_ids)
        return result

    @staticmethod
    def update(uid: int, title: str, tag_ids: List[int]):
        result = Thread.update(uid, title, tag_ids)
        return result

    @staticmethod
    def delete(uid: int):
        Thread.delete(uid)


    ### Helper methods.

    @staticmethod
    def thread_exists(uid: int):
        return Thread.find_by_id(uid) is not None

    @staticmethod
    def author_for_thread(uid: int):
        return Thread.author_for_thread(uid)
