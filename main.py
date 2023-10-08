import chess
from mcts import MCTS_Player as MCTS
from human import Human_Player as Human

def main():
	board = chess.Board()

	p1 = Human(color=True)
	p2 = MCTS(color=False, turn_time=10, thread_cap=16)

	turn = True # true for p1, false for p2

	while not board.is_game_over():
		print(board, "\n")
		board.push(p1.get_move(board) if turn else p2.get_move(board))
		turn = not turn
		print()

if __name__ == "__main__":
	main()