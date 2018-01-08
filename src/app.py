from flask import Flask, request, redirect, abort, url_for, session

# Set up shared instances, once.
import src.shared as shared
shared.setup()

# Controllers.
from src.controllers.hello import HelloWorldController # TODO: remove
from src.controllers.account import AccountController
from src.controllers.tag import TagController

# Application instance.
app = Flask(__name__)
app.secret_key = shared.secret_key


# Convenience methods for session.
def signed_in():
    return session['signed_in'] if 'signed_in' in session else False

def get_user_id() -> int:
    if 'user_id' in session:
        return session['user_id']

def get_username() -> str:
    if 'username' in session:
        return session['username']

def get_display_name() -> str:
    if 'display_name' in session:
        return session['display_name']

def admin_session() -> bool:
    return session['admin'] if 'admin' in session else False


### Testing database connection ###

@app.route("/connection")
def connection():
    return shared.db.test_connection()

### Thread endpoints ###

@app.route("/")
def index():
    # Default to threads.
    return redirect(url_for('threads'))

@app.route("/threads")
def threads():
    return HelloWorldController.threads()

@app.route("/threads/1")
def thread():
    return HelloWorldController.thread()


### Tag endpoints ###

@app.route("/tags")
def tags():
    return TagController.index()

@app.route("/tags/<int:uid>")
def tag(uid: int):
    return TagController.view_for_tag(uid)

@app.route("/tags/<int:uid>/edit", methods=['GET', 'POST']) # HACK: PUT method unavailable from jinja.
def update_tag(uid: int):
    if request.method == 'GET':
        return TagController.view_for_edit_tag(uid)
    else:
        # Admin only.
        if not admin_session():
            abort(403)

        title = request.form['title']
        result = TagController.update(uid, title)
        if result is None:
            return redirect(url_for('tags'))
        else:
            return TagController.view_for_edit_tag(uid, result)

@app.route("/tags/<int:uid>/delete", methods=['POST']) # HACK: DELETE method unavailable from jinja.
def delete_tag(uid: int):
    # Admin only.
    if not admin_session():
        abort(403)

    result = TagController.delete(uid)
    if result is None:
        return redirect(url_for('tags'))
    else:
        return TagController.view_for_edit_tag(uid, result)

@app.route("/tags/new", methods=['GET', 'POST'])
def new_tag():
    if request.method == 'GET':
        return TagController.view_for_new_tag()
    else:
        # Admin only.
        if not admin_session():
            abort(403)

        title = request.form['title']
        result = TagController.create(title)
        if result is None:
            return redirect(url_for('tags'))
        else:
            return TagController.view_for_new_tag(result)


### Account endpoints ###

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    # Redirect if already signed in.
    if signed_in():
        return redirect(url_for('profile'))

    if request.method == 'GET':
        return AccountController.view_for_signin()
    else:
        username, password = request.form['username'], request.form['password']
        result = AccountController.signin(username, password)

        if 'user' in result:
            # TODO: Make account serializable.
            account = result['user']
            session['signed_in'] = True
            session['user_id'] = account.uid
            session['username'] = account.username
            session['display_name'] = account.display_name
            session['admin'] = account.admin
            session['fresh_signin'] = True
            return redirect(url_for('profile'))
        else:
            return AccountController.view_for_signin(result)

@app.route("/signout", methods=['POST'])
def signout():
    if not signed_in():
        abort(401)

    session.pop('signed_in', None)
    session.pop('user_id', None)
    session.pop('display_name', None)
    session.pop('admin', None)
    return redirect(url_for('signin'))

@app.route("/profile")
def profile():
    if not signed_in():
        return redirect(url_for('signin'))

    if 'fresh_signin' in session:
        name = get_display_name() if get_display_name() else get_username()
        session.pop('fresh_signin')
        return AccountController.view_for_profile(get_user_id(), {'welcome': "Welcome back " + name + "!"})
    
    return AccountController.view_for_profile(get_user_id())

@app.route("/profile/edit")
def editprofile():
    return HelloWorldController.editprofile()



if __name__ == "__main__":
	app.run(host='0.0.0.0')
