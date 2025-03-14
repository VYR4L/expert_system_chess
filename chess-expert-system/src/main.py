from experta import *

from rules.material_loss import MaterialLossRule
from rules.king_safety import KingSafetyRule
from rules.missed_checkmate import MissedCheckmateRule
from utils.pgn_parser import parse_pgn

class ChessExpertSystem(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action='analyze')

    @Rule(Fact(action='analyze'))
    def analyze_game(self):
        pgn_data = parse_pgn('partida.pgn') 
        self.declare(Fact(pgn_data=pgn_data))

    @Rule(Fact(pgn_data=MATCH.pgn_data))
    def evaluate_rules(self, pgn_data):
        material_loss_rule = MaterialLossRule()
        king_safety_rule = KingSafetyRule()
        missed_checkmate_rule = MissedCheckmateRule(pgn_data)

        material_loss_issues = material_loss_rule.evaluate(pgn_data)
        king_safety_issues = king_safety_rule.evaluate(pgn_data)
        missed_checkmate_issues = missed_checkmate_rule.evaluate()

        if material_loss_issues:
            print("Material Loss Issues:", material_loss_issues)
        if king_safety_issues:
            print("King Safety Issues:", king_safety_issues)
        if missed_checkmate_issues:
            print("Missed Checkmate Opportunities:", missed_checkmate_issues)

if __name__ == "__main__":
    chess_expert_system = ChessExpertSystem()
    chess_expert_system.reset()  # Prepare the engine for the analysis
    chess_expert_system.run()  # Run the expert system