from flask import Flask

from src.controllers.hello import HelloWorldController
from src.utilities.database import DatabaseManager

# Required instances.
app = Flask(__name__)
dbm = DatabaseManager(database="tsoha")

# Testing database connection.
@app.route("/connection")
def connection():
    return dbm.test_connection()

@app.route("/")
def index():
    return HelloWorldController.index()

@app.route("/threads")
def threads():
    return HelloWorldController.threads()

@app.route("/threads/1")
def thread():
    return HelloWorldController.thread()

@app.route("/signin")
def signin():
    return HelloWorldController.signin()

@app.route("/profile")
def profile():
    return HelloWorldController.profile()

@app.route("/profile/edit")
def editprofile():
    return HelloWorldController.editprofile()

if __name__ == "__main__":
	app.run(host='0.0.0.0')
