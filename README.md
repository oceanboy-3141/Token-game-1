# 🎯 Token Quest

A research game that explores whether Large Language Models place semantically similar words similarly in token space.

## 🆕 NEW in v2.0 - Educational Enhancement Update

### 📊 Visual Token Space Visualization
- **Interactive timeline** showing where your guesses land in token space
- **Color-coded distance indicators** (green=close, red=far)
- **Real-time visual feedback** with target and guess positioning

### 🧠 Educational Feedback System  
- **"Why this happened" explanations** for every guess result
- **Rotating tokenization facts** - learn something new each round!
- **Pattern recognition insights** about word relationships

### 💡 Enhanced Hint System
- **🧠 Semantic Hints Tab**: Words with similar meanings
- **🔢 Token Space Hints Tab**: Words with nearby token IDs  
- **📚 Educational Tab**: Learn about tokenization concepts
- **Progressive revelation** from meaning to mechanics

## 🔬 Research Purpose

This game is designed to investigate **token ID clustering** - do words with similar meanings have similar token IDs in LLM tokenization schemes? Players guess semantically related words while the game measures token ID distances, generating valuable research data.

**NOW WITH EDUCATIONAL VALUE**: Learn how AI language models process text through tokenization!

## 🎮 How to Play

1. **Target Word**: You'll see a word displayed on screen with its token ID
2. **Your Goal**: Find a word that you think is semantically related 
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

2. **Run the game with mode selection**:
   ```bash
   python play.py
   ```
   OR
   ```bash
   python main.py
   ```

### 🎮 Game Modes Available

When you start the game, you'll see a setup screen with options for:

- **🎯 Classic Mode**: Find semantically similar words (close token IDs = higher scores)
- **🔄 Antonym Mode**: Find opposite words (distant token IDs = higher scores)  
- **📂 Category Mode**: Focus on specific word types (emotions, size, speed, etc.)
- **⚡ Random Mode**: Mix of all modes for variety

### 🎨 Themes Available

- **☀️ Light Theme**: Clean white interface
- **🌙 Dark Theme**: Dark mode for low-light gaming
- **💙 Ocean Theme**: Blue color scheme
- **🌿 Nature Theme**: Green color scheme

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

- **📊 Visual Token Space**: See exactly where your guesses land on the token timeline
- **🧠 Educational Feedback**: Learn WHY words have similar/different token IDs
- **💡 Smart Hint System**: Three-tab interface with semantic, token-based, and educational hints
- **🎓 Tokenization Learning**: Rotating facts and insights about how AI processes language
- **📈 Interactive Visualization**: Color-coded distance indicators and real-time positioning
- **🔍 Pattern Recognition**: Discover surprising relationships between words and tokens
- **Clean Interface**: Simple, NYT-style game design with enhanced educational value
- **Real-time Feedback**: Instant scoring with contextual explanations
- **Statistics**: Track your performance over time
- **Data Export**: Export your gameplay data for analysis

## 🔧 Technical Details

- **Encoding**: Uses `o200k_base` (OpenAI's latest tokenizer)
- **Token Distance**: Calculated as absolute difference between token IDs
- **Single Tokens**: Game focuses on words that tokenize to single tokens
- **Word List**: Curated list of common words good for semantic relationships

## 📈 Research Applications

This data helps answer:
- Do semantically similar words cluster in token ID space?
- How does human intuition align with tokenization similarity?
- What patterns exist in semantic token relationships?
- Can token distance predict semantic similarity?

## 🤝 Contributing to Research

Every game you play contributes valuable data! The more diverse players and word associations we collect, the better our understanding of tokenization patterns.

---

**Have fun playing and contributing to language model research!** 🚀 