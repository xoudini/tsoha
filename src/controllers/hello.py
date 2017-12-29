from flask import render_template
from src.controllers.base import BaseController

class HelloWorldController(BaseController):

    @staticmethod
    def index():
        return render_template('index.html', title="Home")

    @staticmethod
    def test():
        return render_template('profile.html', title="Test")

    @staticmethod
    def threads():
        return render_template('threads.html', title="Threads")
    
    @staticmethod
    def thread():
        return render_template('thread.html', title="Thread")

    @staticmethod
    def signin():
        return render_template('signin.html', title="Sign in")
    
    @staticmethod
    def profile():
        return render_template('profile.html', title="Edit")
    
    @staticmethod
    def editprofile():
        return render_template('profile.html', title="Edit", edit=True)
    
