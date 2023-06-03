from flask import Flask
from flask import request, make_response, render_template, jsonify

from src.file import GenerateMaze

app = Flask(__name__)

WIDTH = 10
HEIGHT = 16


@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')


@app.route('/api/wall', methods=['GET'])
def get_encoding():
	maze = GenerateMaze(WIDTH, HEIGHT)
	maze.generate_walls_encodings()
	
	encodings = maze.walls_encoding
	print(encodings)
	encodings = [''.join([str(w) for w in walls]) for walls in encodings]
	
	return jsonify(encodings)
	

@app.route('/api/maze', methods=['GET'])
def get_maze():
	maze = GenerateMaze(WIDTH, HEIGHT)
	maze.generate_maze()
	
	list_maze = maze.maze_grid.tolist()
	# print(list_maze)
	
	return jsonify(list_maze)


if __name__ == '__main__':
	app.run()
