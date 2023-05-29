from flask import Flask
from flask import request, make_response, render_template, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')


if __name__ == '__main__':
	app.run()
