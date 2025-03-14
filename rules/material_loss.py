import chess
import chess.pgn

class MaterialLossRule:
    def evaluate(self, game_state):
        # Check for material loss in the game state
        board = game_state.board()
        for move in game_state.mainline_moves():
            board.push(move)
            if self.lost_piece(board, move) and not self.recovered_within_three_moves(board, game_state, move):
                return f"Material loss detected: {self.lost_piece(board, move)} lost and not recovered within three moves."
        return "No material loss detected."

    def lost_piece(self, board, move):
        # Check if a piece was lost in the move
        if board.is_capture(move):
            return board.piece_at(move.to_square)
        return None

    def recovered_within_three_moves(self, board, game_state, move):
        # Check if the lost piece was recovered within three moves
        lost_piece = self.lost_piece(board, move)
        if not lost_piece:
            return False

        future_board = board.copy()
        for future_move in list(game_state.mainline_moves())[list(game_state.mainline_moves()).index(move) + 1:list(game_state.mainline_moves()).index(move) + 4]:
            future_board.push(future_move)
            if future_board.is_capture(future_move) and future_board.piece_at(future_move.to_square) == lost_piece:
                return True
        return False