from flask import render_template

class BaseController:

    @staticmethod
    def index():
        return render_template('index.html', title="Home")
