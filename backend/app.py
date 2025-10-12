from flask import Flask, render_template, request
import engine
import os

app = Flask(__name__, 
			template_folder='../templates',
			static_folder='../static')

@app.route('/')
def chess_game():
	return render_template('index.html')

@app.route('/make_move', methods=['POST'])
def make_move():
	fen = request.form.get('fen')
	print('fen:', fen)
	board1 = engine.Chessboard(fen)
	print(board1.fen)
	return {'fen': 'make move'}

if __name__ == '__main__':
	app.run(debug=True, threaded=True)