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
1. Set up basic Python environment with tiktoken
2. Create simple command-line prototype
3. Build basic GUI interface
4. Implement scoring system
5. Add data logging functionality
6. Test with initial word sets

---
*This game serves as both entertainment and a research tool to understand how tokenization reflects semantic relationships in language.* 