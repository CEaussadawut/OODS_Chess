#!/usr/bin/env python3
from abc import ABC, abstractmethod

types = {
	1: 'fen',
	2: 'matrix',
	3: 'dictionary',
	4: 'hash'
}

class Chessboard:
	def __init__(self, fen = None):
		if fen == 'start':
			fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
		self.fen = fen
		self.matrix = None
		self.dict = None
		
	def fenToMatrix(self, fen):
		pass
	
	def fenToDict(self, fen):
		pass

	def fenToHash(self, fen):
		pass

	def matrixToFen(self, matrix):
		pass

	def dictToFen(self, matrix):
		pass

	def hashToFen(self, dict):
		pass

	def validFen(self, fen):
		try:
			parts = fen.split()
			print(parts)
		except Exception:
			return False

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
