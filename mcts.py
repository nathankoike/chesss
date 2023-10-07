import chess
import random
import time
import math
import threading
from functools import reduce
from player import Player
from rando import Rando

class MCTS_Player(Player):
	def __init__(self, color, turn_time=2.5, thread_count=16):
		super(MCTS_Player, self).__init__(color)

		# some constant to help with tweaking the confidence check
		self.constant = math.sqrt(2)

		# the amount of time given per turn, represented in seconds
		self.turn_time = turn_time

		# the max number of threads that can be used
		self.thread_count = thread_count

	def get_confidence(self, move):
		''' get the confidence of a move, represented as [wins, plays] '''
		if move[1] == 0:
			return float('inf')

		return move[0] / (move[1] ** self.constant)

	def get_performances(self, moves, board):
		''' simulate the game for a bit, then return the performance ratios'''
		# keep track of the win and play counts for each move
		move_ratios = [[0, 0] for _ in moves]

		start_time = time.time() # current time in seconds

		# time each turn
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

		return move_ratios

	def get_performances_threaded(self, moves, board, returns):
		''' simulate the game for a bit, then modify a list for the return'''
		returns.append(self.get_performances(moves, board))

	def get_move_threaded(self, board):
		''' simulate the game for a bit with multithreading, then choose a move '''
		threads = []

		moves = list(board.legal_moves)

		# threads can't return, so the return values will go here
		thread_returns = []

		# make a bunch of threads
		while len(threads) < self.thread_count:
			thread = threading.Thread(target=self.get_performances_threaded, args=(moves, board, thread_returns))
			thread.start()
			threads.append(thread)

		# let the threads finish
		for thread in threads:
			thread.join()

		# [print(returns) for returns in thread_returns]

		move_ratios = thread_returns.pop(0)

		for returns in thread_returns:
			for i in range(len(move_ratios)):
				move_ratios[i][0] += returns[i][0]
				move_ratios[i][1] += returns[i][1]

		confidences = [self.get_confidence(move) for move in move_ratios]

		print(move_ratios)
		print(sum([ratio[1] for ratio in move_ratios]))
		return moves[confidences.index(max(confidences))]

	def get_move(self, board):
		''' simulate the game for a bit, then choose a move '''
		moves = list(board.legal_moves) # choose a move from here
		move_ratios = self.get_performances(moves, board)

		# get a pure win/loss ratio for each of the moves
		confidences = [self.get_confidence(move) for move in move_ratios]

		# return the first move with the highest confidence
		print(move_ratios)
		print(sum([ratio[1] for ratio in move_ratios]))
		return moves[confidences.index(max(confidences))]

def main():
	board = chess.Board()
	mctsp = MCTS_Player(color=True, turn_time=5)

	print(mctsp.get_move_threaded(board))

if __name__ == "__main__":
	main()