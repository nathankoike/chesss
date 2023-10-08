import chess
from player import Player

class Human_Player(Player):

	def get_move(self, board):
		''' make a completely random, legal move '''
		# get the legal moves in san
		legal_moves = [board.san(move) for move in list(board.legal_moves)]

		print("Legal moves:")
		print([board.san(move) for move in list(board.legal_moves)], "\n")

		# get a legal move
		move = input("Enter a move: ")
		while move not in legal_moves:
			print()
			move = input("Enter a legal move: ")

		return board.parse_san(move)

def main():
	board = chess.Board()
	human = Human(color=True)

	print(human.get_move(board))

if __name__ == "__main__":
	main()