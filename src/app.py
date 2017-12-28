from flask import Flask

from src.controllers.base import BaseController
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
    return BaseController.index()

if __name__ == "__main__":
	app.run(host='0.0.0.0')
