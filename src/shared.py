import src.utilities.database as database
import src.utilities.password as password

def setup():
    global db
    db = database.DatabaseManager(database="tsoha")

    global pw
    pw = password.PasswordUtility()
