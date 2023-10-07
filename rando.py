import chess
import random
from player import Player

class Rando(Player):

	def get_move(self, board):
		''' make a completely random, legal move '''
		return random.choice(list(board.legal_moves))