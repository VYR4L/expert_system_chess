import chess
import chess.pgn
import pyke.knowledge_engine as ke

# Criar um mecanismo de inferência do Pyke
engine = ke.engine(__file__)


def verify_material_loss(board, move):
    material_before = sum([len(board.pieces(piece, color)) for color in (chess.WHITE, chess.BLACK) for piece in range(1, 7)])
    board.push(move)
    material_after = sum([len(board.pieces(piece, color)) for color in (chess.WHITE, chess.BLACK) for piece in range(1, 7)])
    if material_after < material_before:
        return True
    return False


def verify_king_excessive_moves(board, move):
    if board.is_kingside_castling(move) or board.is_queenside_castling(move):
        return False
    if board.is_capture(move):
        return False
    if board.is_en_passant(move):
        return False
    return True


def verify_castling_timing(board, move):
    '''
    Verifica se o roque foi feito em um momento inadequado
    '''
    if board.is_kingside_castling(move) or board.is_queenside_castling(move):
        if board.is_check():
            return False
        if board.is_checkmate():
            return False
        if board.is_stalemate():
            return False
        if board.is_insufficient_material():
            return False
        if board.is_seventyfive_moves():
            return False
        if board.is_fivefold_repetition():
            return False
        return True
    return False


def rate_move(board, move):
    '''
    Avalia um lance de acordo com as regras definidas
    '''
    if verify_material_loss(board, move):
        return -1
    if verify_king_excessive_moves(board, move):
        return -1
    if verify_castling_timing(board, move):
        return -1
    return 1


# Função para carregar um jogo PGN
def load_pgn(caminho_pgn):
    with open(caminho_pgn) as pgn:
        game = chess.pgn.read_game(pgn)
    return game

# Avaliação simples do tabuleiro com material
def rate_board(board):
    valores = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9}
    score = 0
    for piece in board.piece_map().values():
        score += valores.get(piece.symbol().lower(), 0) * (1 if piece.color else -1)
    return score

# Identificar o lance que "desandou"
def detect_error(game):
    board = game.board()
    last_score = rate_board(board)
    erro_lance = None
    lance_numero = 0

    for move in game.mainline_moves():
        board.push(move)
        current_score = rate_board(board)

        # Se a diferença na avaliação for muito grande, é um erro
        if last_score - current_score > 3:
            erro_lance = move
            break

        last_score = current_score
        lance_numero += 1

    return lance_numero, erro_lance

if __name__ == "__main__":
    game = load_pgn("partida2.pgn")
    lance, erro = detect_error(game)

    if erro:
        print(f"A partida começou a desandar no lance {round(lance/2)}: {erro}")
    else:
        print("Nenhum erro crítico detectado.")
