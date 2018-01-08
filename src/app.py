from flask import Flask, request, redirect, url_for

# Set up shared instances, once.
import src.shared as shared
shared.setup()

# Controllers.
from src.controllers.hello import HelloWorldController # TODO: remove
from src.controllers.tag import TagController

# Application instance.
app = Flask(__name__)


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
        title = request.form['title']
        result = TagController.update(uid, title)
        if result is None:
            return redirect(url_for('tags'))
        else:
            return TagController.view_for_edit_tag(uid, result)

@app.route("/tags/<int:uid>/delete", methods=['POST']) # HACK: DELETE method unavailable from jinja.
def delete_tag(uid: int):
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
        title = request.form['title']
        result = TagController.create(title)
        if result is None:
            return redirect(url_for('tags'))
        else:
            return TagController.view_for_new_tag(result)


### Account endpoints ###

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
