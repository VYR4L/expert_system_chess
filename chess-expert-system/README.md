# Chess Expert System

This project is an expert system designed to analyze chess games in Portable Game Notation (PGN) format. It identifies mistakes made during the game, focusing on material loss, king safety, and missed checkmate opportunities.

## Features

- **Material Loss Detection**: Identifies if a player has lost material without recovering it within three moves.
- **King Safety Evaluation**: Assesses whether the king is in a safe position and checks if castling has been performed.
- **Missed Checkmate Opportunities**: Detects situations where a player could have delivered checkmate but failed to do so.

## Project Structure

```
chess-expert-system
├── src
│   ├── main.py               # Entry point of the expert system
│   ├── rules
│   │   ├── material_loss.py  # Rule for detecting material loss
│   │   ├── king_safety.py    # Rule for evaluating king safety
│   │   └── missed_checkmate.py # Rule for identifying missed checkmates
│   └── utils
│       └── pgn_parser.py     # Utility functions for parsing PGN files
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd chess-expert-system
pip install -r requirements.txt
```

## Usage

To run the expert system, execute the following command:

```bash
python src/main.py <path-to-pgn-file>
```

Replace `<path-to-pgn-file>` with the path to the PGN file you want to analyze.

## Requirements

This project requires the following Python packages:

- experta
- Any other necessary packages listed in `requirements.txt`

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.