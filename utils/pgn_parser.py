import chess.pgn

def read_pgn(file_path):
    with open(file_path, 'r') as file:
        pgn_data = file.read()
    return pgn_data

def parse_pgn(file_path):
    with open(file_path) as pgn_file:
        game = chess.pgn.read_game(pgn_file)
    return game

def extract_moves(game):
    moves = []
    for move in game:
        moves.extend(move.split())
    return moves

def convert_pgn_to_analysis_format(file_path):
    pgn_data = read_pgn(file_path)
    games = parse_pgn(pgn_data)
    return [extract_moves(game) for game in games]