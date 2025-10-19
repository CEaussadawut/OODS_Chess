from flask import Flask, render_template, request
import engine
import os

app = Flask(__name__, 
			template_folder='../templates',
			static_folder='../static')

@app.route('/')
def chess_game():
	return render_template('index.html')

@app.route('/api/create_board', methods=['POST'])
def create_board():
	fen = request.form.get('fen')
	board = engine.Chessboard(fen)
	return {'fen': board.fen}

@app.route('/api/start_position', methods=['GET'])
def start_position():
	fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
	# board = engine.Chessboard(fen)
	return {'fen': fen}

@app.route('/api/clear', methods=['POST'])
def clear():
	fen = request.form.get('fen')
	print('fen:', fen)
	board1 = engine.Chessboard(fen)
	return {'fen': 'make move'}

@app.route('/api/make_move', methods=['POST'])
def make_move():
	fen = request.form.get('fen')
	print('fen:', fen)
	board1 = engine.Chessboard(fen)
	return {'fen': 'make move'}


@app.route('/api/valid_check', methods=['POST'])
def valid_check():
	fen = request.form.get('fen')
	print('fen:', fen)
	board2 = engine.Chessboard(fen)
	return {'fen': 'make move'}

if __name__ == '__main__':
	app.run(debug=True, threaded=True)