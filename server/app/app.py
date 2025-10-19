from flask import Flask, render_template, request
import engine
import os

app = Flask(__name__, 
			template_folder='../templates',
			static_folder='../static')

board = []

@app.route('/')
def chess_game():
	return render_template('index.html')

@app.route('/api/create_board', methods=['POST'])
def create_board():
	board_id = int(request.form.get('id'))
	while len(board) <= board_id:
		board.append(None)
	board[board_id] = engine.Chessboard('start')
	print(board_id)
	return {'fen': board[board_id].fen}

@app.route('/api/start_position', methods=['GET'])
def start_position():
	fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

	return {'fen': fen}

@app.route('/api/clear', methods=['GET'])
def clear():
	fen = '8/8/8/8/8/8/8/8'
	return {'fen': fen}

@app.route('/api/make_move', methods=['POST'])
def make_move():
	board_id = int(request.form.get('id'))
	fen = request.form.get('fen')
	print('fen:', fen)
	print('id:', board_id)
	board[board_id].pushHistory(fen)
	print(board[board_id].history)
	return {'fen': 'make move'}


@app.route('/api/valid_check', methods=['POST'])
def valid_check():
	fen = request.form.get('fen')
	print('fen:', fen)
	board2 = engine.Chessboard(fen)
	return {'fen': 'make move'}

if __name__ == '__main__':
	app.run(debug=True, threaded=True)