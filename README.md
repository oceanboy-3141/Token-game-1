# 🎯 Token Quest

A research-driven educational game that explores whether Large Language Models place semantically similar words similarly in token space. **Now exclusively running as a Flask web application** with advanced educational features.

## 🆕 Latest Updates - v2.0 Educational Enhancement

**📢 MAJOR UPDATE**: Token Quest has been transformed from a simple word-guessing game into a comprehensive **educational research tool** that teaches players about tokenization while collecting valuable linguistic data.

### 🎓 Educational Features
- **📊 Interactive Token Space Visualization**: See exactly where words exist in the tokenizer's numerical space
- **🧠 Contextual Learning System**: Every interaction teaches tokenization concepts
- **💡 Progressive Discovery**: Journey from semantic understanding to token mechanics
- **📚 Built-in Tokenization Education**: 10+ rotating facts about how AI processes language
- **🔍 Pattern Recognition**: Learn why certain words have similar token IDs

### 🎮 Enhanced Gameplay
- **Three-Tab Hint System**: 
  - 🧠 **Semantic Hints**: Words with similar meanings
  - 🔢 **Token Space Hints**: Words with nearby token IDs from the actual tokenizer
  - 📚 **Educational Tab**: Interactive lessons about tokenization
- **Visual Token Timeline**: Real-time positioning with color-coded distance indicators
- **Smart Feedback**: "Why this happened" explanations for every guess
- **Multiple Game Modes**: Classic, Antonym, Category-focused, and Random modes

## 🔬 Research Purpose

Token Quest investigates **semantic clustering in tokenization space** - a fundamental question about how AI language models organize human language. Do words with similar meanings get assigned similar token IDs?

**Key Research Question**: Does human intuition about word similarity align with tokenization similarity in Large Language Models?

**Educational Impact**: Players learn how AI processes language while generating research data through engaging gameplay.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Installation & Launch

#### Option 1: Standard Setup
1. **Clone and setup**:
   ```bash
   git clone [your-repo-url]
   cd "Token game"
   pip install -r requirements.txt
   ```

2. **Start the web application**:
   ```bash
   python app.py
   ```
   Open your browser to `http://localhost:5000`

#### Option 2: Virtual Environment (Recommended)
1. **Create virtual environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Mac/Linux:
   source .venv/bin/activate
   ```

2. **Install and run**:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

#### Option 3: Network/LAN Play
```bash
python run_network_game.py
```
Share the displayed URL with friends on your network for multiplayer sessions!

## 🎮 Complete Feature Overview

### 🎯 Game Modes
- **🤝 Synonym Hunt**: Find semantically similar words (closer token IDs = higher scores)
- **⚡ Antonym Challenge**: Find opposite words (distant token IDs = higher scores)
- **⚡ Speed Mode**: Race against time with customizable time limits (15-120 seconds)
- **📂 Category Focus**: Deep dive into specific semantic categories
- **🎲 Mixed Mode**: Dynamic combination of all game types

### 🏆 Achievement System
**25+ Achievements** across multiple categories:
- **🎯 Accuracy**: Perfect shots, sharpshooter, marksman medals
- **🔥 Streaks**: Hot streak, on fire, unstoppable chains
- **🌍 Exploration**: Word explorer, vocabulary master, token researcher
- **👑 Mastery**: Synonym specialist, antonym expert, category king
- **🎓 Educational**: Token student, scholar, research contributor
- **🌟 Special**: Lucky shot, comeback kid, night owl, early bird
- **💯 Scoring**: High scorer, point collector achievements

### 🏅 Leaderboard System
- **Multi-Mode Rankings**: Separate leaderboards for each game mode
- **Comprehensive Stats**: Track accuracy, best distances, average performance
- **Player Profiles**: Personal best scores and achievement progress
- **Export Functionality**: Download leaderboard data for analysis
- **Competition Features**: Compare with friends and track improvements

### 🎨 Customization Options
- **4 Visual Themes**: Light, Dark, Ocean, Nature
- **Accessibility Features**: High contrast, font size options
- **Sound Settings**: Audio feedback controls
- **Game Preferences**: Difficulty, category, and mode selection

### 📊 Difficulty & Categories
**8 Semantic Categories** with 3 difficulty tiers each:
- **Emotions**: happy, sad, excited → euphoric, melancholy, elated
- **Size**: big, small, tiny → colossal, minuscule, gargantuan  
- **Speed**: fast, slow, quick → velocity, sluggish, instantaneous
- **Quality**: good, bad, nice → exemplary, atrocious, sublime
- **Temperature**: hot, cold, warm → scorching, frigid, temperate
- **Brightness**: bright, dark, dim → luminous, obscure, radiant
- **Actions**: run, walk, jump → sprint, stroll, leap
- **Difficulty**: easy, hard, simple → effortless, arduous, elementary

## 📁 Project Architecture

```
Token game/
├── app.py                          # 🌐 Main Flask web application (333 lines)
├── run_network_game.py             # 🌐 Network/LAN hosting setup
├── game_logic.py                   # 🎮 Core game mechanics & scoring (623 lines)
├── token_handler.py                # 🔤 tiktoken integration & operations
├── enhanced_data_collector.py      # 📊 Advanced research data logging (637 lines)
├── achievements.py                 # 🏆 Achievement tracking system (327 lines)  
├── leaderboard.py                  # 🏅 Leaderboard & social features (162 lines)
├── data_collector.py               # 📈 Basic data collection utilities
├── templates/                      # 🎨 HTML templates for web interface
│   ├── home.html                   # 🏠 Landing page with mode selection
│   ├── game.html                   # 🎮 Main game interface (515 lines)
│   ├── game_setup.html             # ⚙️ Game configuration screen
│   ├── tutorial.html               # 🎓 Interactive tutorial (693 lines)
│   ├── leaderboards.html           # 🏆 Leaderboard display (219 lines)
│   ├── settings.html               # 🎨 Appearance & preferences (297 lines)
│   └── base.html                   # 📄 Template foundation
├── static/                         # 💎 Web assets & styling
│   ├── css/style.css              # 🎨 Advanced game styling
│   ├── js/game.js                 # ⚡ Interactive JavaScript
│   └── sounds/                    # 🔊 Audio feedback system
├── game_data/                      # 📁 Research data storage
│   ├── session_*.json             # 📝 Individual game sessions
│   ├── daily_log_*.json           # 📊 Daily aggregated analytics  
│   ├── comprehensive_research_data_*.json  # 🔬 Research summaries
│   ├── achievements.json          # 🏆 Player achievement progress
│   └── leaderboard.json           # 🏅 High score rankings
├── .venv/                          # 🐍 Virtual environment (recommended)
├── requirements.txt                # 📦 Python dependencies
└── [Planning Documents]/          # 📋 Development roadmaps & plans
    ├── GAME_PLAN.md               # 🎯 Main project roadmap
    ├── IMPROVEMENT_PLAN.md        # 🚀 Enhancement priorities
    └── MEGA_PLAN.md               # 🌟 Long-term vision
```

## 🧠 Game Mechanics & Scoring

### Core Gameplay Loop
1. **Target Display**: See a word with its token ID and educational context
2. **Player Input**: Enter a word you think is semantically related
3. **Analysis**: Game calculates token distance and provides educational feedback
4. **Visualization**: See your guess positioned on the token space timeline
5. **Learning**: Receive explanations about why tokens are similar/different

### Advanced Scoring System
- **Base Score**: `Score = max(0, 1000 - absolute_token_distance)`
- **Achievement Bonuses**: Unlock achievements for score multipliers
- **Streak Multipliers**: Consecutive correct guesses boost scores
- **Speed Bonuses**: Time-based scoring in Speed Mode
- **Difficulty Modifiers**: Harder categories provide score boosts
- **Educational Engagement**: Points for using hints and tutorials

### Smart Hint System
- **Progressive Revelation**: Start with meaning-based hints, then explore token mechanics
- **Interactive Suggestions**: Click hint words to auto-fill input
- **Token Range Information**: See nearby token IDs with exact distances
- **Educational Context**: Learn why certain tokens cluster together

## 📊 Research Data Collection

Token Quest automatically logs comprehensive research data:

### Comprehensive Data Tracking
- **Game Sessions**: Target words, guesses, distances, timestamps
- **Achievement Progress**: Unlock patterns and completion metrics
- **Leaderboard Data**: High scores, rankings, and competitive analytics
- **Educational Metrics**: Hint usage, tutorial completion, learning progression
- **Performance Analytics**: Accuracy trends, improvement patterns
- **Research Insights**: Token clustering patterns, semantic relationships

### Data Storage & Export
- `game_data/session_[timestamp].json` - Individual session records
- `game_data/achievements.json` - Player achievement progress
- `game_data/leaderboard.json` - High score rankings across modes
- `game_data/daily_log_[date].json` - Daily aggregated analytics
- `game_data/comprehensive_research_data_[date].json` - Research summaries
- **Export Functions**: CSV, JSON, and formatted text exports for analysis

## 🔧 Technical Implementation

### Tokenization Engine
- **Primary Encoding**: `o200k_base` (OpenAI's latest tokenizer)
- **Alternative**: Model-specific encoding via `tiktoken.encoding_for_model("gpt-4o")`
- **Focus**: Single-token words for precise distance calculations
- **Validation**: Real-time token verification and multi-token handling

### Word Database
- **8 Semantic Categories**: emotions, size, speed, quality, temperature, brightness, actions, difficulty
- **3 Difficulty Levels**: easy, medium, hard per category
- **120+ Curated Words**: Optimized for semantic relationship exploration
- **Synonym/Antonym Pairs**: Structured for research analysis

### Educational Engine
- **10+ Tokenization Facts**: Rotating educational content
- **Pattern Recognition**: Automatic identification of word relationship patterns
- **Contextual Explanations**: AI generates explanations for token similarities
- **Progressive Learning**: Adaptive educational content based on player progress

## 📈 Research Applications & Academic Value

Token Quest addresses several key research questions:

### Primary Research Areas
- **Semantic Clustering**: Do semantically similar words cluster in token ID space?
- **Human-AI Alignment**: How does human semantic intuition align with tokenization patterns?
- **Cross-Category Analysis**: Are token relationships consistent across semantic categories?
- **Learning Progression**: How do players develop understanding of tokenization concepts?

### Academic Contributions
- **Novel Dataset**: Human semantic judgments paired with token distance measurements
- **Educational Framework**: Gamified approach to teaching NLP concepts
- **Behavioral Insights**: Understanding how humans learn AI language processing concepts
- **Cross-Linguistic Potential**: Framework extensible to multiple languages and tokenizers

## 🚀 Development Roadmap & Upcoming Features

### 🎯 Current Status: Phase 2.0 - Professional Platform
Token Quest has successfully evolved from a simple prototype into a comprehensive educational research platform with:
- ✅ **Complete Web Interface**: Fully functional Flask application
- ✅ **Advanced Achievement System**: 25+ achievements across 7 categories  
- ✅ **Social Features**: Leaderboards, player profiles, score tracking
- ✅ **Educational Tools**: Interactive tutorial, progressive hint system
- ✅ **Data Analytics**: Comprehensive research data collection
- ✅ **Multi-Mode Gameplay**: 5 distinct game modes with difficulty scaling

### 🚀 Phase 2.5: AI Research Acceleration (Next Priority)
- **🤖 AI Player System**: Automated gameplay for large-scale data generation
  - Multiple AI strategies (random, semantic, token-based, hybrid)
  - Batch processing: Generate 1000+ game sessions overnight
  - Strategy comparison: AI vs human behavioral analysis
- **📊 Advanced Analytics Dashboard**: Real-time research insights
- **🔬 Pattern Discovery**: Automated semantic cluster identification
- **📈 Research Export Tools**: Academic-ready data formatting

### 🌟 Phase 3: Platform Evolution (6-12 Months)
- **🎨 Material Design Overhaul**: Modern, responsive UI/UX
- **📱 Mobile Application**: Native iOS/Android versions
- **🌐 Multi-Language Support**: Tokenization across different languages
- **🏫 Institutional Integration**: University/research partnerships
- **🔗 API Development**: External research access and integration

## 🤝 Contributing to AI Research

Every game session contributes valuable data to understanding how AI processes human language. The more diverse our player base, the richer our insights into:

- **Semantic intuition** across different backgrounds and languages
- **Learning patterns** in AI concept acquisition  
- **Cultural variations** in word association
- **Educational effectiveness** of gamified NLP learning

## 🎓 Educational Applications

Token Quest serves multiple educational purposes:

### For Students
- **Interactive NLP Learning**: Hands-on experience with tokenization concepts
- **AI Literacy**: Understanding how language models process text
- **Semantic Awareness**: Enhanced vocabulary and word relationship understanding

### For Educators
- **Teaching Tool**: Demonstrate AI concepts through engaging gameplay
- **Assessment Data**: Track student understanding of tokenization principles
- **Research Platform**: Collect data on learning effectiveness

### For Researchers
- **Data Collection**: Automated gathering of semantic similarity judgments
- **Hypothesis Testing**: Validate theories about token space organization
- **Cross-Model Comparison**: Compare tokenization across different AI systems

---

## 🎮 Getting Started Tips

### First-Time Players
1. **Start with the Tutorial**: Meet Tokky the Token and learn the basics
2. **Try Synonym Hunt**: Begin with the classic mode to understand token relationships
3. **Explore Categories**: Pick your favorite semantic category (emotions work great!)
4. **Use Hints Wisely**: The three-tab hint system teaches as you play
5. **Track Progress**: Check your achievements and leaderboard position

### For Educators
- **Demo Mode**: Use Speed Mode for quick classroom demonstrations
- **Research Value**: Show students how AI processes language through tokenization
- **Data Export**: Export session data for classroom analysis projects
- **Achievement System**: Motivate students with educational achievements

### For Researchers
- **Data Collection**: Every session contributes to tokenization research
- **Export Tools**: Multiple data formats for statistical analysis
- **Research Insights**: Track patterns in semantic similarity judgments
- **Batch Analysis**: Plan for AI player system to accelerate data generation

---

**🚀 Join the Token Quest community and help unlock the secrets of AI language understanding!**

**Where Research Meets Gaming** - Token Quest proves that complex AI concepts can be both educational and entertaining. Every game you play contributes to advancing our understanding of how language models organize human language.

*🎯 Ready to start your token adventure? Launch the game and discover how AI sees the world of words!* 