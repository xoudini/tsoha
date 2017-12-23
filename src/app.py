from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
	return "<p style=\"font-size: 15pt; font-family: Menlo, monospace;\">Up and running.<p>"


if __name__ == "__main__":
	app.run(host='0.0.0.0')
