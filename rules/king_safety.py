import chess

class KingSafetyRule:
    def evaluate(self, game_state):
        # Check if the king is in a safe position
        king_in_check = self.is_king_in_check(game_state)
        castling_done = self.has_castled(game_state)

        if king_in_check and not castling_done:
            return "The king is in check and has not castled, which is a safety concern."
        elif not castling_done:
            return "The king has not castled, which may lead to safety issues."
        return "The king is safe."

    def is_king_in_check(self, game_state):
        # Implement logic to determine if the king is in check
        board = game_state.board()
        for move in game_state.mainline_moves():
            board.push(move)
        return board.is_check()

    def has_castled(self, game_state):
        # Implement logic to check if castling has been performed
        board = game_state.board()
        for move in game_state.mainline_moves():
            board.push(move)
        return not (board.has_kingside_castling_rights(chess.WHITE) or board.has_kingside_castling_rights(chess.BLACK) or 
                    board.has_queenside_castling_rights(chess.WHITE) or board.has_queenside_castling_rights(chess.BLACK))