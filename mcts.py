import chess
import random
import time
import math
from player import Player
from rando import Rando

class MCTS_Player(Player):
	def __init__(self, color, turn_time=2.5):
		super(MCTS_Player, self).__init__(color)

		# some constant to help with tweaking the confidence check
		self.constant = math.sqrt(2)

		# the amount of time given per turn, represented in seconds
		self.turn_time = turn_time

	def get_confidence(self, move):
		''' get the confidence of a move, represented as [wins, plays] '''
		if move[1] == 0:
			return float('inf')
		return move[0] / (move[1] ** self.constant)

	def get_move(self, board):
		''' simulate the game for a bit, then choose a move '''
		moves = list(board.legal_moves) # choose a move from here

		# keep track of the win and play counts for each move
		move_ratios = [[0, 0] for _ in moves]

		i = 0
		start_time = time.time() # current time in seconds

		# 2.5s per turn
		while time.time() < start_time + self.turn_time:
			board_copy = board.copy() # creates a deep copy of the board

			# get a confidence score for every move
			confidences = [self.get_confidence(move) for move in move_ratios]

			# find and make the first move with the highest confidence score
			best_move = confidences.index(max(confidences))
			board_copy.push(moves[best_move])

			# randomly simulate the game until a winner is found
			while not board_copy.is_game_over():
				board_copy.push(random.choice(list(board_copy.legal_moves)))

			# get the applicable value for the outcome
			result = board_copy.outcome().result().split('-')[0 if self.color else 1]

			# get the wins and plays for the selected move
			[best_move_wins, best_move_plays] = move_ratios[best_move]

			# adjust the counts accordingly
			move_ratios[best_move] = [best_move_wins + eval(result), best_move_plays + 1]

		# get a pure win/loss ratio for each of the moves
		confidences = [self.get_confidence(move) for move in move_ratios]

		# return the first move with the highest confidence
		print(move_ratios)
		print(sum([ratio[1] for ratio in move_ratios]))
		return moves[confidences.index(max(confidences))]

def main():
	board = chess.Board()
	mctsp = MCTS_Player(color=True, turn_time=5)

	print(mctsp.get_move(board))

if __name__ == "__main__":
	main()