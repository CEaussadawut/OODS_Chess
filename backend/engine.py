#!/usr/bin/env python3
from abc import ABC, abstractmethod

class Chessboard:
	def __init__(self, fen = None):
		self.fen = fen


	# def board_validator(self):
	# 	board_split = self.board.split()
	# 	king_count = 0
	# 	for row in board_split:
	# 		if len(row) != self.size:
	# 			raise ValueError("Board is not square")
	# 		for char in row:
	# 			if char not in ['P','B','R','Q','K','.']:
	# 				raise ValueError("Invalid character in board")
	# 			if char == 'K':
	# 				king_count += 1
	# 	if king_count != 1:
	# 		raise ValueError("There must be exactly one king on the board")
	# 	return True

	# def initialize_pieces(self):
	# 	pieces = []
	# 	for y, row in enumerate(self.board_split):
	# 		for x, char in enumerate(row):
	# 			if char == 'P':
	# 				pieces.append(pawn([x + 1, y + 1], self))  # Pass self
	# 			elif char == 'K':
	# 				pieces.append(king([x + 1, y + 1], self))  # Pass self
	# 				self.king_pos = [x + 1, y + 1]
	# 			elif char == 'B':
	# 				pieces.append(bishop([x + 1, y + 1], self))
	# 			elif char == 'R':
	# 				pieces.append(rook([x + 1, y + 1], self))
	# 			elif char == 'Q':
	# 				pieces.append(queen([x + 1, y], self))
	# 	return pieces
	
	# def opponent_moves(self, pieces):
	# 	moves = []
	# 	for piece in pieces:
	# 		if not isinstance(piece, king):
	# 			moves.extend(piece.move_ables)
	# 	return moves

	# def check_for_checkmate(self):
	# 	opponent_moves = self.opponent_moves(self.pieces)
	# 	if self.king_pos in opponent_moves:
	# 		return True
	# 	return False

class piece(ABC):
	def __init__(self, pos, chessboard):
		self.pos = pos
		self.chessboard = chessboard
		self.moves = self.move()
		self.move_ables = self.move_able()

	@abstractmethod
	def move(self):
		pass

	def move_able(self):
		self.move_ables = []
		for move in self.moves:
			if self.pos[0] + move[0] <= self.chessboard.size and \
				self.pos[0] + move[0] > 0 and \
				self.pos[1] + move[1] > 0 and \
				self.pos[1] + move[1] <= self.chessboard.size:
				self.move_ables.append([self.pos[0] + move[0], self.pos[1] + move[1]])
		return self.move_ables


class pawn(piece):
	def __init__(self, pos, chessboard):
		super().__init__(pos, chessboard)
		self.moves = self.move()
		self.move_ables = self.move_able()
	
	def move(self):
		return [[-1,-1],[1,1]]

class king(piece):
	def __init__(self, pos, chessboard):
		super().__init__(pos, chessboard)
		self.moves = self.move()

	def move(self):
		return [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]

class bishop(piece):
	def __init__(self, pos, chessboard):
		super().__init__(pos, chessboard)
		self.moves = self.move()

	def move(self):
		return [[-1,-1],[-1,1],[1,-1],[1,1]]

class rook(piece):
	def __init__(self, pos, chessboard):
		super().__init__(pos, chessboard)
		self.moves = self.move()

	def move(self):
		moves_list = []
		for i in range(1, self.chessboard.size):
			moves_list.append([i, 0])
			moves_list.append([-i, 0])
			moves_list.append([0, i])
			moves_list.append([0, -i])
		return moves_list

class queen(piece):
	def __init__(self, pos, chessboard):
		super().__init__(pos, chessboard)

	def move(self):
		moves_list = []
		# Horizontal and vertical moves (like a rook)
		for i in range(1, self.chessboard.size):
			moves_list.append([i, 0])   # Right
			moves_list.append([-i, 0])  # Left
			moves_list.append([0, i])   # Up
			moves_list.append([0, -i])  # Down

		# Diagonal moves (like a bishop)
		for i in range(1, self.chessboard.size):
			moves_list.append([i, i])    # Top-right
			moves_list.append([-i, -i])  # Bottom-left
			moves_list.append([i, -i])   # Bottom-right
			moves_list.append([-i, i])   # Top-left

		return moves_list
	

def checkmate(board):
	chess_board = Chessboard(board)
	if chess_board.board_validator():
		chess_board.initialize_pieces()
		print(chess_board.king_pos)
		print(chess_board.opponent_movess)
		if chess_board.check_for_checkmate():
			print("Success")
			return "Success"
		print("Fail")
		return "Fail"
	return "Board Invalid"
