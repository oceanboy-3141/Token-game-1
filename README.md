# 🎯 Token Synonym Game

A research game that explores whether Large Language Models place synonyms similarly in token space.

## 🔬 Research Purpose

This game is designed to investigate **token ID clustering** - do words with similar meanings have similar token IDs in LLM tokenization schemes? Players guess synonyms while the game measures token ID distances, generating valuable research data.

## 🎮 How to Play

1. **Target Word**: You'll see a word displayed on screen with its token ID
2. **Your Goal**: Find a word that you think is similar/synonymous 
3. **Scoring**: Get points based on how close your word's token ID is to the target's token ID
4. **Research**: Your guesses help us understand semantic clustering in tokenization!

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- tkinter (usually included with Python)

### Installation

1. **Install tiktoken**:
   ```bash
   pip install tiktoken
   ```

2. **Run the game**:
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
Token game/
├── main.py              # Main entry point
├── gui_interface.py     # GUI using tkinter
├── game_logic.py        # Core game mechanics
├── token_handler.py     # tiktoken operations
├── data_collector.py    # Research data logging
├── requirements.txt     # Dependencies
├── GAME_PLAN.md        # Project roadmap
└── README.md           # This file
```

## 🧠 Game Mechanics

- **Scoring**: `Score = max(0, 1000 - token_distance)`
- **Feedback**: Encouraging messages based on how close you get
- **Hints**: Shows nearby words in token space
- **Data**: All guesses logged for research analysis

## 📊 Research Data

The game automatically collects:
- Target words and their token IDs
- Player guesses and their token IDs  
- Token ID distances
- Timestamps and session info

Data is saved to:
- `game_data/session_[timestamp].json` - Session files
- `game_data/daily_log_[date].json` - Daily aggregated logs
- `game_data/token_game_data_[session].csv` - CSV exports

## 🎯 Game Features

- **Clean Interface**: Simple, NYT-style game design
- **Real-time Feedback**: Instant scoring and encouragement
- **Statistics**: Track your performance over time
- **Data Export**: Export your gameplay data for analysis
- **Hint System**: Get suggestions for nearby tokens

## 🔧 Technical Details

- **Encoding**: Uses `o200k_base` (OpenAI's latest tokenizer)
- **Token Distance**: Calculated as absolute difference between token IDs
- **Single Tokens**: Game focuses on words that tokenize to single tokens
- **Word List**: Curated list of common words good for synonyms

## 📈 Research Applications

This data helps answer:
- Do synonyms cluster in token ID space?
- How does human intuition align with tokenization similarity?
- What patterns exist in semantic token relationships?
- Can token distance predict semantic similarity?

## 🤝 Contributing to Research

Every game you play contributes valuable data! The more diverse players and word associations we collect, the better our understanding of tokenization patterns.

---

**Have fun playing and contributing to language model research!** 🚀 