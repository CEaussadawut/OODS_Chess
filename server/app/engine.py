#!/usr/bin/env python3
from abc import ABC, abstractmethod


START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
EMPTY_FEN = "8/8/8/8/8/8/8/8"

class Chessboard:
	"""Represent a chessboard and keep track of position history."""

	def __init__(self, fen=None):
		if fen == "start" or fen is None:
			fen = START_FEN
		self.fen = None
		self.matrix = None
		self.history = []
		self.current_index = -1
		if fen:
			self.reset(fen)

	def reset(self, fen=START_FEN):	
		self.history = []
		self.current_index = -1
		self.pushHistory(fen)

	def pushHistory(self, fen):
		"""Add a new FEN to the history, trimming any forward states."""
		if not self.validFen(fen):
			raise ValueError("Invalid FEN provided")

		if self.current_index < len(self.history) - 1:
			self.history = self.history[: self.current_index + 1]

		if not self.history or fen != self.history[-1]:
			self.history.append(fen)
			self.current_index = len(self.history) - 1
		self.fen = fen
		return fen

	def popHistory(self):
		"""Remove the most recent FEN from history."""

		if not self.history:
			raise IndexError("No history to pop")

		removed = self.history.pop()
		self.current_index = len(self.history) - 1
		self.fen = self.history[self.current_index] if self.history else None
		return removed

	def get_history(self):
		return list(self.history)

	def fenToMatrix(self, fen = None):
		if not fen:
			fen = self.fen
		if not self.validFen(fen):
			raise ValueError("Invalid FEN provided")

		valid_pieces = set("prnbqkPRNBQK")
		board_state = fen.split()[0]
		ranks = board_state.split("/")
		matrix = []

		for rank in ranks:
			row = []
			for ch in rank:
				if ch.isdigit():
					# expand digits into that many empty squares
					row.extend(["."] * int(ch))
				elif ch in valid_pieces:
					row.append(ch)
				else:
					# invalid character found
					return False
			# each rank must result in exactly 8 files
			if len(row) != 8:
				return False
			matrix.append(row)

		self.matrix = matrix
		return self.matrix

	def displayMatrix(self, matrix = None):
		if matrix is None:
			matrix = self.matrix
		if not matrix:
			return None
		for i in range(0, len(matrix)):
			print(matrix[i])

	def matrixToFen(self, matrix = None):
		if matrix is None:
			matrix = self.matrix
		if not matrix:
			return None
		
		ranks = []
		for row in matrix:
			# each row must have 8 files
			if len(row) != 8:
				return None
			count = 0
			parts = []
			for cell in row:
				# treat '.' or empty string as empty square
				if cell == "." or cell == "":
					count += 1
				else:
					if count:
						parts.append(str(count))
						count = 0
					parts.append(cell)
			if count:
				parts.append(str(count))
			ranks.append("".join(parts))
		
		fen = "/".join(ranks)
		self.fen = fen
		return self.fen

	def rewind(self):
		"""Move one step back in history and return the resulting FEN."""

		if self.current_index <= 0:
			return self.fen

		self.current_index -= 1
		self.fen = self.history[self.current_index]
		return self.fen

	def forward(self):
		"""Move one step forward in history and return the resulting FEN."""

		if self.current_index >= len(self.history) - 1:
			return self.fen

		self.current_index += 1
		self.fen = self.history[self.current_index]
		return self.fen

	def validFen(self, fen):
		"""Perform a lightweight validation of a FEN string."""

		if not isinstance(fen, str) or not fen:
			return False

		board_state = fen.split()[0]
		ranks = board_state.split("/")
		if len(ranks) != 8:
			return False

		valid_pieces = set("prnbqkPRNBQK")
		for rank in ranks:
			file_count = 0
			for char in rank:
				if char.isdigit():
					file_count += int(char)
				elif char in valid_pieces:
					file_count += 1
				else:
					return False
			if file_count != 8:
				return False

		return True
	
	def validMove(self, current_matrix, next_matrix):
		pass


class piece(ABC):
	def __init__(self, pos, chessboard, color):
		self.pos = pos
		self.chessboard = chessboard
		self.color = color
		self.moves = self.move()
		# self.move_ables = self.move_able()

	@abstractmethod
	def move(self):
		pass
	
	@abstractmethod
	def __str__(self):
		return super().__str__()

	def move_able(self):
		self.move_ables = []
		for move in self.moves:
			if (
				self.pos[0] + move[0] <= self.chessboard.size
				and self.pos[0] + move[0] > 0
				and self.pos[1] + move[1] > 0
				and self.pos[1] + move[1] <= self.chessboard.size
			):
				self.move_ables.append(
					[self.pos[0] + move[0], self.pos[1] + move[1]]
				)
		return self.move_ables


class pawn(piece):
	def __init__(self, pos, chessboard, color):
		super().__init__(pos, chessboard)
		self.moves = self.move()
		# self.move_ables = self.move_able()

	def move(self):
		return [[-1, -1], [1, 1]]
	
	def __str__(self):
		if self.color == 'w':
			return 'P'
		return 'p'


class king(piece):
	def __init__(self, pos, chessboard, color):
		super().__init__(pos, chessboard)
		self.moves = self.move()

	def move(self):
		return [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

	def __str__(self):
		if self.color == 'w':
			return 'K'
		return 'k'

class bishop(piece):
	def __init__(self, pos, chessboard, color):
		super().__init__(pos, chessboard)
		self.moves = self.move()

	def move(self):
		return [[-1, -1], [-1, 1], [1, -1], [1, 1]]
	
	def __str__(self):
		if self.color == 'w':
			return 'B'
		return 'b'


class rook(piece):
	def __init__(self, pos, chessboard, color):
		super().__init__(pos, chessboard, color)
		self.moves = self.move()

	def move(self):
		moves_list = []
		for i in range(1, self.chessboard.size):
			moves_list.append([i, 0])
			moves_list.append([-i, 0])
			moves_list.append([0, i])
			moves_list.append([0, -i])
		return moves_list
	
	def __str__(self):
		if self.color == 'w':
			return 'R'
		return 'r'


class queen(piece):
	def __init__(self, pos, chessboard, color):
		super().__init__(pos, chessboard, color)

	def move(self):
		moves_list = []
		# Horizontal and vertical moves (like a rook)
		for i in range(1, self.chessboard.size):
			moves_list.append([i, 0])  # Right
			moves_list.append([-i, 0])  # Left
			moves_list.append([0, i])  # Up
			moves_list.append([0, -i])  # Down

		# Diagonal moves (like a bishop)
		for i in range(1, self.chessboard.size):
			moves_list.append([i, i])  # Top-right
			moves_list.append([-i, -i])  # Bottom-left
			moves_list.append([i, -i])  # Bottom-right
			moves_list.append([-i, i])  # Top-left

		return moves_list

	def __str__(self):
		if self.color == 'w':
			return 'Q'
		return 'q'
	