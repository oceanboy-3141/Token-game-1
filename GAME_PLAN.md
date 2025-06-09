# Token Synonym Game - Project Plan

## Research Objective
**Primary Goal**: Investigate whether Large Language Models (LLMs) place synonyms similarly in token space by analyzing token IDs.

**Research Question**: Do synonyms have similar/close token IDs in the tokenization space?

## Game Concept

### Core Gameplay
- **Genre**: Word puzzle game (inspired by New York Times games)
- **Mechanics**: 
  - Display a target word on screen (preferably single token, but multi-token allowed)
  - Player must find/guess a word with the **closest token ID** to the target word
  - Scoring based on how close the guessed token ID is to the target token ID

### Research Integration
- Each gameplay session generates data about:
  - Which words players associate as "similar" 
  - Actual token ID distances between chosen words
  - Whether human intuition about word similarity aligns with tokenization similarity

## Technical Requirements

### Core Dependencies
```python
import tiktoken

# Primary encoding to use
enc = tiktoken.get_encoding("o200k_base")

# Alternative: Model-specific encoding
enc = tiktoken.encoding_for_model("gpt-4o")

# Installation
pip install tiktoken
```

### Key Technical Features
- Token encoding/decoding functionality
- Token ID comparison and distance calculation
- Word input validation
- Score calculation based on token ID proximity

## Development Strategy

### Phase 1: MVP (Current - Cursor Development)
- **Focus**: Core functionality over graphics
- **Goal**: Proof of concept and initial data collection
- **Graphics**: Minimal, functional UI

### Phase 2: Polish (Future - Replit Development)
- **Focus**: Enhanced UI/UX and graphics
- **Goal**: Refined user experience

## Game Flow Design

1. **Start Screen**: Game explanation and research context
2. **Main Game**: 
   - Display target word
   - Show target word's token ID (optional - for transparency)
   - Input field for player's guess
   - Submit and feedback system
3. **Scoring/Feedback**:
   - Show guessed word's token ID
   - Calculate and display ID distance
   - Provide encouragement/scoring
4. **Data Collection**: Log word pairs and ID distances for research

## Data Points to Collect
- Target word and its token ID
- Player's guessed word and its token ID  
- Token ID distance/difference
- Timestamp and session info
- Player's reasoning (optional feedback)

## Success Metrics
- **Gameplay**: Engaging and educational experience
- **Research**: Clear patterns in synonym token ID clustering
- **Data Quality**: Sufficient data points for meaningful analysis

## Next Steps
1. ✅ Set up basic Python environment with tiktoken
2. ✅ Create simple command-line prototype
3. ✅ Build basic GUI interface
4. ✅ Implement scoring system
5. ✅ Add data logging functionality
6. ✅ Test with initial word sets
7. ✅ Enhanced hint system with contextual suggestions
8. ✅ Expanded word categories and difficulty levels
9. ✅ Added progress bars and visual feedback

## 🚀 Completed Immediate Improvements (Phase 1.5)

### ✅ Enhanced Hint System
- **Contextual hints** based on word categories (emotions, size, speed, etc.)
- **Suggested word buttons** that can be clicked to auto-fill
- **Token range information** showing nearby token IDs
- **Interactive hint window** with better UX

### ✅ Better Scoring Visualization
- **Progress bars** showing game completion and round attempts
- **Enhanced visual feedback** with colored results
- **Real-time progress updates** as players make guesses

### ✅ Word List Expansion
- **8 semantic categories**: emotions, size, speed, quality, temperature, brightness, actions, difficulty
- **3 difficulty levels** per category: easy, medium, hard
- **Synonym/antonym pairs** for research analysis
- **120+ total words** vs original 48 words

## 🔧 Medium-term Enhancements (Phase 2)

### 🤝 Multiplayer/Social Features
- **Share results** with friends via exportable summaries
- **Local leaderboards** stored in game data
- **"Word of the day"** challenges with special scoring
- **Session comparison** tools to track improvement

### 🎮 Advanced Game Modes
- **Antonym Mode**: Find words with maximum token distance (opposite meanings)
- **Category Mode**: All words from same semantic category (emotions only, etc.)
- **Speed Mode**: Time-based challenges with countdown timers
- **Explorer Mode**: Let players choose their own target words
- **Difficulty Settings**: Choose easy/medium/hard word sets
- **Custom Word Lists**: Allow users to add their own word categories

### 📊 Research Dashboard
- **Real-time data visualization** showing distance patterns
- **Pattern discovery tools** to find semantic clusters
- **Export research summaries** with statistical analysis
- **Correlation analysis** between categories and token distances
- **Interactive charts** showing player performance trends

## 🌟 Long-term Vision (Phase 3)

### 🤖 AI Integration
- **LLM validation**: Use actual language models to validate semantic similarity
- **Embedding comparison**: Compare token distance vs. embedding similarity (cosine similarity)
- **Intelligent hints**: Generate contextual hints using GPT-4 based on semantic relationships
- **Semantic scoring**: Bonus points for semantically similar words regardless of token distance
- **Dynamic difficulty**: AI adjusts word difficulty based on player performance

### 📚 Educational Features
- **Tutorial mode** explaining tokenization concepts step-by-step
- **Insights panels** showing how LLMs "see" language through tokens
- **Mini-lessons** on linguistics, NLP, and language model architecture
- **Research explanations** of why token clustering matters
- **Interactive token explorer** to browse the full token vocabulary

### 🔬 Advanced Research Tools
- **Cluster analysis**: Automatically identify semantic clusters in token space
- **Cross-language comparison**: Compare tokenization across different languages
- **Model comparison**: Compare token distances across different LLM tokenizers
- **Longitudinal studies**: Track how token relationships change over time
- **Publication tools**: Generate research papers from collected data

---
*This game serves as both entertainment and a research tool to understand how tokenization reflects semantic relationships in language.* 