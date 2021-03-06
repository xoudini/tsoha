from flask import Flask, request, redirect, abort, url_for, session

# Set up shared instances, once.
import src.shared as shared
shared.setup()

# Controllers.
from src.controllers.account import AccountController
from src.controllers.tag import TagController
from src.controllers.thread import ThreadController
from src.controllers.response import ResponseController

# Application instance.
app = Flask(__name__)
app.secret_key = shared.secret_key


### Convenience methods for session. ###

def signed_in():
    return session['signed_in'] if 'signed_in' in session else False

def get_user_id() -> int:
    if 'user_id' in session:
        return session['user_id']

def get_username() -> str:
    if 'username' in session:
        return session['username']

def admin_session() -> bool:
    return session['admin'] if 'admin' in session else False

def set_signed_in(user_id: int, username: str, display_name: str = None, admin: bool = False):
    session['signed_in'] = True
    session['fresh_signin'] = True
    session['user_id'] = user_id
    session['username'] = username
    session['display_name'] = display_name
    session['admin'] = admin


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
    return ThreadController.view_for_threads()

@app.route("/threads/<int:uid>", methods=['GET', 'POST'])
def thread(uid: int):
    if request.method == 'GET':
        return ThreadController.view_for_thread(uid)
    else:
        if not signed_in():
            abort(401)
        
        # Abort if no content was provided.
        if 'content' not in request.form:
            abort(405)
        
        # Abort if thread doesn't exist.
        if not ThreadController.thread_exists(uid):
            abort(404)
        
        content = request.form['content']

        result = ResponseController.create(get_user_id(), uid, content)

        if 'errors' not in result:
            return redirect(url_for('thread', uid=uid))
        else:
            return ThreadController.view_for_thread(uid, messages=result)

@app.route("/threads/<int:uid>/edit", methods=['GET', 'POST']) # HACK: PUT method unavailable from jinja.
def update_thread(uid: int):
    if request.method == 'GET':
        return ThreadController.view_for_edit_thread(uid)
    else:
        if not signed_in():
            abort(401)
        
        author_id = ThreadController.author_for_thread(uid)

        # Abort if author_id wasn't found.
        if author_id is None:
            abort(404)
        
        # Abort if privileges aren't sufficient.
        if not (admin_session() or author_id == get_user_id()):
            abort(403)

        title = request.form['title']
        tag_ids = request.form.getlist('tags')
        
        result = ThreadController.update(uid, title, tag_ids)

        if 'errors' not in result:
            return redirect(url_for('thread', uid=uid))
        else:
            return ThreadController.view_for_edit_thread(uid, result)

@app.route("/threads/<int:uid>/delete", methods=['POST']) # HACK: DELETE method unavailable from jinja.
def delete_thread(uid: int):
    # Abort if not signed in.
    if not signed_in():
        abort(401)
    
    author_id = ThreadController.author_for_thread(uid)

    # Abort if author_id wasn't found.
    if author_id is None:
        abort(404)
    
    # Abort if privileges aren't sufficient.
    if not (admin_session() or author_id == get_user_id()):
        abort(403)
    
    ThreadController.delete(uid)

    return redirect(url_for('threads'))

@app.route("/threads/new", methods=['GET', 'POST'])
def new_thread():
    if request.method == 'GET':
        return ThreadController.view_for_new_thread()
    else:
        # Abort if not signed in.
        if not signed_in():
            abort(401)

        title = request.form['title']
        content = request.form['content']
        tag_ids = request.form.getlist('tags')

        result = ThreadController.create(get_user_id(), title, content, tag_ids)
        
        if 'errors' not in result:
            return redirect(url_for('thread', uid=result['thread_id']))
        else:
            return ThreadController.view_for_new_thread(result)


### Tag endpoints ###

@app.route("/tags")
def tags():
    return TagController.view_for_tags()

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

        if not any(key in result for key in ('errors', 'warnings')):
            return redirect(url_for('tags'))
        else:
            return TagController.view_for_edit_tag(uid, result)

@app.route("/tags/<int:uid>/delete", methods=['POST']) # HACK: DELETE method unavailable from jinja.
def delete_tag(uid: int):
    # Admin only.
    if not admin_session():
        abort(403)

    result = TagController.delete(uid)

    if 'errors' not in result:
        return redirect(url_for('tags'))
    else:
        # NOTE: Only reason for a delete failing is the non-existence of the tag.
        abort(404)

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

        if 'errors' not in result:
            return redirect(url_for('tags'))
        else:
            return TagController.view_for_new_tag(result)


### Account endpoints ###

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    # Redirect if already signed in.
    if signed_in():
        return redirect(url_for('profile'))

    if request.method == 'GET':
        return AccountController.view_for_signup()
    else:
        username = request.form['username']
        password = request.form['password']
        repeated_password = request.form['repeated_password']
        result = AccountController.signup(username, password, repeated_password)

        if 'user' in result:
            # TODO: Make account serializable.
            account = result['user']
            set_signed_in(account.uid, account.username)
            return redirect(url_for('profile'))
        else:
            return AccountController.view_for_signup(result)

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
            set_signed_in(account.uid, account.username, account.display_name, account.admin)
            return redirect(url_for('profile'))
        else:
            return AccountController.view_for_signin(result)

@app.route("/signout", methods=['POST'])
def signout():
    # Abort if not signed in.
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
        name = session['display_name'] if 'display_name' in session and session['display_name'] else get_username()
        session.pop('fresh_signin')
        return AccountController.view_for_profile(get_user_id(), {'welcome': "Welcome, " + name + "!"})
    
    return AccountController.view_for_profile(get_user_id())

@app.route("/profile/edit", methods=['GET', 'POST'])
def udpate_profile():
    if not signed_in():
        return redirect(url_for('signin'))

    if request.method == "GET":
        return AccountController.view_for_edit_profile(get_user_id())
    else:
        display_name = request.form['display_name']
        result = AccountController.update(get_user_id(), display_name)

        if 'errors' not in result:
            return redirect(url_for('profile'))
        else:
            return AccountController.view_for_edit_profile(get_user_id(), result)

@app.route("/users/<int:uid>")
def user(uid: int):
    if signed_in() and uid == get_user_id():
        return redirect(url_for('profile'))

    return AccountController.view_for_profile(uid)



### Entry point.

if __name__ == "__main__":
	app.run(host='0.0.0.0')
