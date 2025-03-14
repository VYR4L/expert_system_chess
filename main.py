from experta import *
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QLabel
import sys

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
        pgn_data = parse_pgn(self.pgn_file) 
        self.declare(Fact(pgn_data=pgn_data))

    @Rule(Fact(pgn_data=MATCH.pgn_data))
    def evaluate_rules(self, pgn_data):
        material_loss_rule = MaterialLossRule()
        king_safety_rule = KingSafetyRule()
        missed_checkmate_rule = MissedCheckmateRule(pgn_data)

        material_loss_issues = material_loss_rule.evaluate(pgn_data)
        king_safety_issues = king_safety_rule.evaluate(pgn_data)
        missed_checkmate_issues = missed_checkmate_rule.evaluate()

        results = []
        if material_loss_issues:
            results.append(f"Material Loss Issues: {material_loss_issues}")
        if king_safety_issues:
            results.append(f"King Safety Issues: {king_safety_issues}")
        if missed_checkmate_issues:
            results.append(f"Missed Checkmate Opportunities: {missed_checkmate_issues}")

        self.results = "\n".join(results)

def run_expert_system(pgn_file, app):
    chess_expert_system = ChessExpertSystem()
    chess_expert_system.pgn_file = pgn_file
    chess_expert_system.reset()  # Prepare the engine for the analysis
    chess_expert_system.run()  # Run the expert system
    app.display_results(chess_expert_system.results)

class ChessExpertSystemApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Chess Expert System')
        self.setGeometry(100, 100, 600, 600)

        layout = QVBoxLayout()

        self.text_area = QTextEdit(self)
        layout.addWidget(self.text_area)

        self.select_button = QPushButton('Select PGN File', self)
        self.select_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_button)

        self.copy_button = QPushButton('Copy PGN Text', self)
        self.copy_button.clicked.connect(self.copy_pgn_text)
        layout.addWidget(self.copy_button)

        self.results_area = QTextEdit(self)
        self.results_area.setReadOnly(True)
        layout.addWidget(self.results_area)

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open PGN File', '', 'PGN Files (*.pgn)')
        if file_path:
            run_expert_system(file_path, self)

    def copy_pgn_text(self):
        pgn_text = self.text_area.toPlainText()
        with open("temp.pgn", "w") as temp_file:
            temp_file.write(pgn_text)
        run_expert_system("temp.pgn", self)

    def display_results(self, results):
        self.results_area.setText(results)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ChessExpertSystemApp()
    ex.show()
    sys.exit(app.exec())