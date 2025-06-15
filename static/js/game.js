// Game state management
let gameState = {
    gameStarted: false,
    currentRound: 0,
    maxRounds: 10,
    score: 0,
    correctGuesses: 0,
    attemptsLeft: 1,
    gameCompleted: false,
    currentTargetWord: '',
    currentTargetTokenId: null,
    isSpeedMode: false,
    timeLimit: 30,
    timeRemaining: 30,
    timerInterval: null
};

// DOM elements
let elements = {};

// Initialize the game
function initializeGame() {
    console.log('🎮 Initializing Token Quest Web Version');
    
    // Get DOM elements
    elements = {
        // Status elements
        currentRound: document.getElementById('current-round'),
        maxRounds: document.getElementById('max-rounds'),
        currentScore: document.getElementById('current-score'),
        correctGuesses: document.getElementById('correct-guesses'),
        attemptsLeft: document.getElementById('attempts-left'),
        gameProgress: document.getElementById('game-progress'),
        
        // Target elements
        targetWord: document.getElementById('target-word'),
        targetToken: document.getElementById('target-token'),
        targetHint: document.getElementById('target-hint'),
        
        // Input elements
        guessForm: document.getElementById('guess-form'),
        guessInput: document.getElementById('guess-input'),
        submitBtn: document.getElementById('submit-btn'),
        
        // Button elements
        startBtn: document.getElementById('start-btn'),
        hintBtn: document.getElementById('hint-btn'),
        newGameBtn: document.getElementById('new-game-btn'),
        
        // Display elements
        resultsCard: document.getElementById('results-card'),
        resultContent: document.getElementById('result-content'),
        visualizationCard: document.getElementById('visualization-card'),
        tokenCanvas: document.getElementById('token-canvas'),
        
        // Timer elements
        timerDisplay: document.getElementById('timer-display'),
        timeRemaining: document.getElementById('time-remaining'),
        
        // Modal elements
        hintModal: document.getElementById('hint-modal'),
        closeHint: document.getElementById('close-hint'),
        hintContentArea: document.getElementById('hint-content-area'),
        
        // Loading
        loading: document.getElementById('loading')
    };
    
    // Set up event listeners
    setupEventListeners();
    
    // Update initial display
    updateGameDisplay();
    
    console.log('✅ Game initialized successfully');
}

function setupEventListeners() {
    // Start game button
    elements.startBtn.addEventListener('click', startNewGame);
    
    // Guess form submission
    elements.guessForm.addEventListener('submit', function(e) {
        e.preventDefault();
        submitGuess();
    });
    
    // Input validation
    elements.guessInput.addEventListener('input', function() {
        const hasValue = this.value.trim().length > 0;
        elements.submitBtn.disabled = !hasValue || !gameState.gameStarted;
    });
    
    // Hint button
    elements.hintBtn.addEventListener('click', showHintModal);
    
    // New game button
    elements.newGameBtn.addEventListener('click', startCompletelyNewGame);
    
    // Modal close handlers
    elements.closeHint.addEventListener('click', closeHintModal);
    elements.hintModal.addEventListener('click', function(e) {
        if (e.target === elements.hintModal) {
            closeHintModal();
        }
    });
    
    // Hint tab switching
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('tab-btn')) {
            switchHintTab(e.target.dataset.tab);
        }
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && elements.hintModal.style.display !== 'none') {
            closeHintModal();
        }
        if (e.key === 'Enter' && e.ctrlKey && gameState.gameStarted) {
            submitGuess();
        }
    });
}

async function startNewGame() {
    console.log('🚀 Starting new game...');
    showLoading(true);
    
    // Load game settings from localStorage
    const savedSettings = localStorage.getItem('game-settings');
    let gameSettings = {
        game_mode: 'normal',
        difficulty: 'mixed',
        category: 'all',
        rounds: 10,
        is_speed_mode: false,
        time_limit: 30
    };
    
    if (savedSettings) {
        gameSettings = {...gameSettings, ...JSON.parse(savedSettings)};
        console.log('📝 Loaded game settings:', gameSettings);
        
        // Update game state for speed mode
        gameState.isSpeedMode = gameSettings.is_speed_mode || false;
        gameState.timeLimit = gameSettings.time_limit || 30;
    }
    
    try {
        const response = await fetch('/api/start_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(gameSettings)
        });
        
        const data = await response.json();
        
        if (data.success) {
            console.log('✅ Game started successfully', data);
            
            // Update game state
            gameState.gameStarted = true;
            gameState.currentRound = data.round_info.current_round;
            gameState.maxRounds = data.round_info.max_rounds;
            gameState.currentTargetWord = data.round_info.target_word;
            gameState.currentTargetTokenId = data.round_info.target_token_id;
            gameState.attemptsLeft = data.round_info.attempts_left;
            
            // Update UI
            updateGameDisplay();
            enableGameControls();
            
            // Start timer if speed mode
            if (gameState.isSpeedMode) {
                startRoundTimer();
            }
            
            // Focus on input
            elements.guessInput.focus();
            
        } else {
            console.error('❌ Failed to start game:', data);
            showError('Failed to start game: ' + (data.error || 'Unknown error'));
        }
        
    } catch (error) {
        console.error('❌ Error starting game:', error);
        showError('Network error: Could not start game');
    } finally {
        showLoading(false);
    }
}

async function submitGuess() {
    const guess = elements.guessInput.value.trim();
    
    if (!guess || !gameState.gameStarted) {
        return;
    }
    
    console.log('🤔 Submitting guess:', guess);
    showLoading(true);
    
    try {
        const response = await fetch('/api/submit_guess', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                guess: guess
            })
        });
        
        const data = await response.json();
        
        if (data.success && data.result.valid_guess) {
            console.log('✅ Guess processed:', data.result);
            
            // Stop timer if speed mode
            if (gameState.isSpeedMode) {
                stopTimer();
            }
            
            // Update game state
            gameState.score = data.result.total_score || gameState.score;
            gameState.attemptsLeft = data.result.attempts_left;
            
            if (data.result.correct) {
                gameState.correctGuesses++;
            }
            
            // Show result
            showGuessResult(data.result);
            
            // Clear input
            elements.guessInput.value = '';
            elements.submitBtn.disabled = true;
            
            // Update display
            updateGameDisplay();
            
            // Auto-advance to next round after 2 seconds (since we only have 1 attempt)
            setTimeout(() => {
                if (!data.result.game_ended && gameState.currentRound < gameState.maxRounds) {
                    startNextRound();
                } else {
                    showGameCompleted();
                }
            }, 2000);
            
        } else {
            console.warn('⚠️ Invalid guess or error:', data);
            
            // For invalid guesses (like multi-token words), show a nice error message
            // but don't advance to next round - let them try again
            const errorMessage = data.result?.error || data.error || 'Invalid guess';
            
            // Show error in the results card instead of alert
            elements.resultContent.innerHTML = `
                <div class="result-error">
                    <h3>⚠️ Invalid Word</h3>
                    <p><strong>Error:</strong> ${errorMessage}</p>
                    <p><strong>Your guess:</strong> "${guess}"</p>
                    <p><em>This doesn't count as an attempt. Try again with a single-token word!</em></p>
                </div>
            `;
            elements.resultsCard.style.display = 'block';
            elements.visualizationCard.style.display = 'none';
            
            // Clear input but keep it enabled for another try
            elements.guessInput.value = '';
            elements.submitBtn.disabled = true;
            elements.guessInput.focus();
            
            // Hide the error message after 3 seconds
            setTimeout(() => {
                elements.resultsCard.style.display = 'none';
            }, 3000);
        }
        
    } catch (error) {
        console.error('❌ Error submitting guess:', error);
        showError('Network error: Could not submit guess');
    } finally {
        showLoading(false);
    }
}

async function startNextRound() {
    console.log('➡️ Starting next round...');
    await startNewGame(); // Reuse the same function
}

function showGuessResult(result) {
    console.log('📊 Showing result:', result);
    
    // Create result HTML
    let resultHTML = '';
    let resultClass = '';
    
    if (result.points >= 80) {
        resultClass = 'result-excellent';
        if (window.soundManager) window.soundManager.playSound('win');
        resultHTML = `
            <div class="${resultClass}">
                <h3>🎉 Excellent! (+${result.points} points)</h3>
                <p><strong>Distance:</strong> ${result.distance} tokens away</p>
                <p><strong>Your guess:</strong> "${result.guess_word}" (Token ID: ${result.guess_token_id})</p>
                <p><strong>Target:</strong> "${gameState.currentTargetWord}" (Token ID: ${gameState.currentTargetTokenId})</p>
                ${result.feedback ? `<p><em>${result.feedback}</em></p>` : ''}
            </div>
        `;
    } else if (result.points >= 40) {
        resultClass = 'result-good';
        if (window.soundManager) window.soundManager.playSound('success');
        resultHTML = `
            <div class="${resultClass}">
                <h3>👍 Good job! (+${result.points} points)</h3>
                <p><strong>Distance:</strong> ${result.distance} tokens away</p>
                <p><strong>Your guess:</strong> "${result.guess_word}" (Token ID: ${result.guess_token_id})</p>
                <p><strong>Target:</strong> "${gameState.currentTargetWord}" (Token ID: ${gameState.currentTargetTokenId})</p>
                ${result.feedback ? `<p><em>${result.feedback}</em></p>` : ''}
            </div>
        `;
    } else {
        resultClass = 'result-needs-work';
        if (window.soundManager) window.soundManager.playSound('lose');
        
        // Check if this was the last attempt
        const isLastAttempt = gameState.attemptsLeft <= 0;
        const attemptMessage = isLastAttempt ? 
            `<p><strong>⏰ Round Over!</strong> Moving to next word...</p>` : 
            `<p><small>Hint: Try words with similar meanings or closer token IDs</small></p>`;
            
        resultHTML = `
            <div class="${resultClass}">
                <h3>🤔 ${isLastAttempt ? 'Round Complete!' : 'Keep trying!'} (+${result.points} points)</h3>
                <p><strong>Distance:</strong> ${result.distance} tokens away</p>
                <p><strong>Your guess:</strong> "${result.guess_word}" (Token ID: ${result.guess_token_id})</p>
                <p><strong>Target:</strong> "${gameState.currentTargetWord}" (Token ID: ${gameState.currentTargetTokenId})</p>
                ${result.feedback ? `<p><em>${result.feedback}</em></p>` : ''}
                ${attemptMessage}
            </div>
        `;
    }
    
    // Show result card
    elements.resultContent.innerHTML = resultHTML;
    elements.resultsCard.style.display = 'block';
    
    // Draw token visualization
    drawTokenVisualization(result);
    elements.visualizationCard.style.display = 'block';
    
    // Scroll to results
    elements.resultsCard.scrollIntoView({ behavior: 'smooth' });
}

function drawTokenVisualization(result) {
    const canvas = elements.tokenCanvas;
    const ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Calculate positions
    const targetTokenId = gameState.currentTargetTokenId;
    const guessTokenId = result.guess_token_id;
    const distance = Math.abs(targetTokenId - guessTokenId);
    
    // Create a simple linear representation
    const canvasWidth = canvas.width - 60; // Leave margin
    const canvasHeight = canvas.height;
    const centerY = canvasHeight / 2;
    
    // Determine range for visualization
    const range = Math.max(distance * 2, 1000); // Show at least 1000 token range
    const minToken = Math.min(targetTokenId, guessTokenId) - range / 4;
    const maxToken = Math.max(targetTokenId, guessTokenId) + range / 4;
    
    // Helper function to get X position for a token ID
    function getXPosition(tokenId) {
        return 30 + ((tokenId - minToken) / (maxToken - minToken)) * canvasWidth;
    }
    
    // Draw background line
    ctx.strokeStyle = '#E0E0E0';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(30, centerY);
    ctx.lineTo(canvas.width - 30, centerY);
    ctx.stroke();
    
    // Draw target position
    const targetX = getXPosition(targetTokenId);
    ctx.fillStyle = '#1976D2';
    ctx.beginPath();
    ctx.arc(targetX, centerY, 8, 0, 2 * Math.PI);
    ctx.fill();
    
    // Draw guess position
    const guessX = getXPosition(guessTokenId);
    ctx.fillStyle = '#03DAC6';
    ctx.beginPath();
    ctx.arc(guessX, centerY, 8, 0, 2 * Math.PI);
    ctx.fill();
    
    // Draw connection line
    ctx.strokeStyle = '#FF9800';
    ctx.lineWidth = 3;
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.moveTo(targetX, centerY);
    ctx.lineTo(guessX, centerY);
    ctx.stroke();
    ctx.setLineDash([]);
    
    // Draw labels
    ctx.fillStyle = '#333';
    ctx.font = '12px Roboto';
    ctx.textAlign = 'center';
    
    // Target label
    ctx.fillText(`Target: ${gameState.currentTargetWord}`, targetX, centerY - 20);
    ctx.fillText(`(${targetTokenId})`, targetX, centerY - 8);
    
    // Guess label
    ctx.fillText(`Guess: ${result.guess_word}`, guessX, centerY + 25);
    ctx.fillText(`(${guessTokenId})`, guessX, centerY + 37);
    
    // Distance label
    const midX = (targetX + guessX) / 2;
    ctx.fillStyle = '#FF9800';
    ctx.font = '14px Roboto';
    ctx.fillText(`Distance: ${distance}`, midX, centerY + 50);
}

async function showHintModal() {
    console.log('💡 Showing hint modal...');
    showLoading(true);
    
    try {
        const response = await fetch('/api/get_hint');
        const data = await response.json();
        
        if (data) {
            console.log('💡 Hint data received:', data);
            
            // Show modal
            elements.hintModal.style.display = 'flex';
            
            // Initialize with semantic hints
            showSemanticHints(data);
            
        } else {
            showError('Could not get hints');
        }
    } catch (error) {
        console.error('❌ Error getting hints:', error);
        showError('Network error: Could not get hints');
    } finally {
        showLoading(false);
    }
}

function showSemanticHints(hintData) {
    let hintsHTML = '<h4>🧠 Semantic Hints</h4>';
    
    if (hintData.semantic_hints && hintData.semantic_hints.length > 0) {
        hintsHTML += '<p>Try words with similar meanings:</p><ul>';
        hintData.semantic_hints.forEach(hint => {
            hintsHTML += `<li><strong>${hint}</strong></li>`;
        });
        hintsHTML += '</ul>';
    }
    
    if (hintData.contextual_hint) {
        hintsHTML += `<p><em>Context:</em> ${hintData.contextual_hint}</p>`;
    }
    
    if (hintData.educational_fact) {
        hintsHTML += `<div style="background: var(--hint-background); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <strong>💡 Did you know?</strong><br>
            ${hintData.educational_fact}
        </div>`;
    }
    
    elements.hintContentArea.innerHTML = hintsHTML;
}

function switchHintTab(tabType) {
    // Update active tab
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector(`[data-tab="${tabType}"]`).classList.add('active');
    
    // Switch content based on tab
    switch(tabType) {
        case 'semantic':
            // Already implemented above
            break;
        case 'token':
            elements.hintContentArea.innerHTML = `
                <h4>🔢 Token Space Hints</h4>
                <p>Target token ID: <strong>${gameState.currentTargetTokenId}</strong></p>
                <p>Try words with token IDs close to this number.</p>
                <p><em>Tip: Common words often have lower token IDs</em></p>
            `;
            break;
        case 'educational':
            elements.hintContentArea.innerHTML = `
                <h4>📚 Educational Content</h4>
                <p>Tokenization is how language models break down text into smaller units called tokens.</p>
                <p>Each token has a unique ID number. Words with similar meanings sometimes (but not always) have similar token IDs.</p>
                <p><strong>Your task:</strong> Find words that are semantically similar to "<em>${gameState.currentTargetWord}</em>" and see if they have close token IDs!</p>
            `;
            break;
    }
}

function closeHintModal() {
    elements.hintModal.style.display = 'none';
}

async function startCompletelyNewGame() {
    console.log('🔄 Starting completely new game...');
    
    try {
        const response = await fetch('/api/new_game', { method: 'POST' });
        const data = await response.json();
        
        if (data.success) {
            // Reset game state
            gameState = {
                gameStarted: false,
                currentRound: 0,
                maxRounds: 10,
                score: 0,
                correctGuesses: 0,
                attemptsLeft: 3,
                gameCompleted: false,
                currentTargetWord: '',
                currentTargetTokenId: null
            };
            
            // Reset UI
            updateGameDisplay();
            resetGameUI();
            
            console.log('✅ New game session created');
        }
    } catch (error) {
        console.error('❌ Error creating new game:', error);
    }
}

// Timer functions for speed mode
function startRoundTimer() {
    if (!gameState.isSpeedMode) return;
    
    // Clear any existing timer
    if (gameState.timerInterval) {
        clearInterval(gameState.timerInterval);
    }
    
    // Reset timer
    gameState.timeRemaining = gameState.timeLimit;
    elements.timerDisplay.style.display = 'block';
    elements.timeRemaining.textContent = gameState.timeRemaining;
    
    // Start countdown
    gameState.timerInterval = setInterval(() => {
        gameState.timeRemaining--;
        elements.timeRemaining.textContent = gameState.timeRemaining;
        
        // Change color as time runs low
        if (gameState.timeRemaining <= 5) {
            elements.timeRemaining.style.color = '#ff4444';
            elements.timeRemaining.style.fontWeight = 'bold';
        } else if (gameState.timeRemaining <= 10) {
            elements.timeRemaining.style.color = '#ff8800';
        } else {
            elements.timeRemaining.style.color = '';
            elements.timeRemaining.style.fontWeight = '';
        }
        
        // Time's up!
        if (gameState.timeRemaining <= 0) {
            clearInterval(gameState.timerInterval);
            handleTimeOut();
        }
    }, 1000);
}

function stopTimer() {
    if (gameState.timerInterval) {
        clearInterval(gameState.timerInterval);
        gameState.timerInterval = null;
    }
}

function handleTimeOut() {
    console.log('⏰ Time is up!');
    
    // Disable input
    elements.guessInput.disabled = true;
    elements.submitBtn.disabled = true;
    
    // Show timeout message with countdown
    showTimeoutCountdown();
}

function showTimeoutCountdown() {
    let countdown = 3;
    
    // Show initial message
    elements.resultContent.innerHTML = `
        <div class="result-timeout">
            <h3>⏰ Oops! You ran out of time!</h3>
            <p><strong>Target word was:</strong> "${gameState.currentTargetWord}"</p>
            <p style="font-size: 1.2em; font-weight: bold; color: #ff6600;">
                Moving to next word in ${countdown}...
            </p>
        </div>
    `;
    elements.resultsCard.style.display = 'block';
    elements.resultsCard.scrollIntoView({ behavior: 'smooth' });
    
    // Countdown timer
    const countdownInterval = setInterval(() => {
        countdown--;
        const countdownElement = elements.resultContent.querySelector('p:last-child');
        if (countdownElement) {
            countdownElement.innerHTML = `Moving to next word in ${countdown}...`;
        }
        
        if (countdown <= 0) {
            clearInterval(countdownInterval);
            
            // Move to next round
            setTimeout(() => {
                elements.resultsCard.style.display = 'none';
                if (gameState.currentRound < gameState.maxRounds) {
                    startNextRound();
                } else {
                    showGameCompleted();
                }
            }, 500);
        }
    }, 1000);
}

function updateGameDisplay() {
    // Update status display
    elements.currentRound.textContent = gameState.currentRound || '-';
    elements.maxRounds.textContent = gameState.maxRounds || '-';
    elements.currentScore.textContent = gameState.score;
    elements.correctGuesses.textContent = gameState.correctGuesses;
    elements.attemptsLeft.textContent = gameState.attemptsLeft;
    
    // Show/hide timer display based on speed mode
    if (gameState.isSpeedMode) {
        elements.timerDisplay.style.display = 'block';
        elements.timeRemaining.textContent = gameState.timeRemaining;
    } else {
        elements.timerDisplay.style.display = 'none';
    }
    
    // Update progress bar
    const progressPercent = gameState.maxRounds > 0 ? 
        (gameState.currentRound / gameState.maxRounds) * 100 : 0;
    elements.gameProgress.style.width = progressPercent + '%';
    
    // Update target display
    if (gameState.gameStarted && gameState.currentTargetWord) {
        elements.targetWord.textContent = gameState.currentTargetWord;
        elements.targetToken.textContent = `Token ID: ${gameState.currentTargetTokenId}`;
        elements.targetHint.textContent = `Find a word with similar meaning or nearby token ID`;
    }
}

function enableGameControls() {
    elements.startBtn.style.display = 'none';
    elements.hintBtn.disabled = false;
    elements.newGameBtn.style.display = 'inline-flex';
    elements.guessInput.disabled = false;
    
    // Enable submit if input has value
    const hasValue = elements.guessInput.value.trim().length > 0;
    elements.submitBtn.disabled = !hasValue;
    
    // Re-enable input for next round in speed mode
    if (gameState.isSpeedMode) {
        elements.guessInput.disabled = false;
        elements.submitBtn.disabled = !hasValue;
    }
}

function resetGameUI() {
    elements.startBtn.style.display = 'inline-flex';
    elements.newGameBtn.style.display = 'none';
    elements.hintBtn.disabled = true;
    elements.submitBtn.disabled = true;
    elements.guessInput.disabled = false;
    elements.guessInput.value = '';
    
    elements.targetWord.textContent = 'Click "Start Game" to begin!';
    elements.targetToken.textContent = 'Token ID: -';
    elements.targetHint.textContent = 'Find a word with a similar meaning or nearby token ID';
    
    elements.resultsCard.style.display = 'none';
    elements.visualizationCard.style.display = 'none';
    elements.timerDisplay.style.display = 'none';
    
    // Stop any running timer
    if (gameState.timerInterval) {
        clearInterval(gameState.timerInterval);
        gameState.timerInterval = null;
    }
}

function showGameCompleted() {
    console.log('🎉 Game completed!');
    
    elements.resultContent.innerHTML = `
        <div class="result-excellent">
            <h3>🎉 Game Completed!</h3>
            <p><strong>Final Score:</strong> ${gameState.score} points</p>
            <p><strong>Correct Guesses:</strong> ${gameState.correctGuesses} / ${gameState.maxRounds}</p>
            <p>Thank you for contributing to our research!</p>
            <button class="btn btn-success" onclick="startCompletelyNewGame()">
                <span class="material-icons">play_arrow</span>
                Play Again
            </button>
        </div>
    `;
    
    elements.resultsCard.style.display = 'block';
    elements.resultsCard.scrollIntoView({ behavior: 'smooth' });
    
    gameState.gameCompleted = true;
    gameState.gameStarted = false;
    
    // Show score submission modal
    handleGameCompletion();
}

function showLoading(show) {
    elements.loading.style.display = show ? 'flex' : 'none';
}

function showError(message) {
    console.error('❌ Error:', message);
    alert('Error: ' + message); // Simple error handling for now
}

// Export functions for global access
window.initializeGame = initializeGame;
window.startCompletelyNewGame = startCompletelyNewGame;

// Score Submission Functionality
function showScoreSubmissionModal(finalResults) {
    const modal = document.getElementById('score-modal');
    const summary = document.getElementById('score-summary');
    const playerNameInput = document.getElementById('player-name');
    
    // Load saved player name
    const savedName = localStorage.getItem('player-name') || '';
    playerNameInput.value = savedName;
    
    // Populate score summary
    summary.innerHTML = `
        <h4>🎉 Game Complete!</h4>
        <div class="score-highlight">${finalResults.total_score} points</div>
        <div class="score-details">
            <div class="score-detail">
                <div class="score-detail-value">${finalResults.accuracy.toFixed(1)}%</div>
                <div class="score-detail-label">Accuracy</div>
            </div>
            <div class="score-detail">
                <div class="score-detail-value">${finalResults.correct_guesses}/${finalResults.total_rounds}</div>
                <div class="score-detail-label">Correct</div>
            </div>
        </div>
    `;
    
    modal.style.display = 'flex';
    playerNameInput.focus();
}

// Handle score submission
document.addEventListener('DOMContentLoaded', function() {
    // Submit score button
    const submitScoreBtn = document.getElementById('submit-score-btn');
    if (submitScoreBtn) {
        submitScoreBtn.addEventListener('click', async function() {
            const playerName = document.getElementById('player-name').value.trim();
            const resultDiv = document.getElementById('score-result');
            
            if (!playerName) {
                resultDiv.innerHTML = '<div class="error">Please enter your name</div>';
                resultDiv.className = 'score-result error';
                resultDiv.style.display = 'block';
                return;
            }
            
            if (playerName.length > 20) {
                resultDiv.innerHTML = '<div class="error">Name must be 20 characters or less</div>';
                resultDiv.className = 'score-result error';
                resultDiv.style.display = 'block';
                return;
            }
            
            try {
                this.disabled = true;
                this.innerHTML = '<span class="material-icons">hourglass_empty</span> Submitting...';
                
                const response = await fetch('/api/submit_score', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        player_name: playerName
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Save player name
                    localStorage.setItem('player-name', playerName);
                    
                    let resultHTML = `
                        <div class="success">
                            <div class="rank-announcement">🏆 Rank #${data.rank}</div>
                            <div>Score: ${data.score} points</div>
                    `;
                    
                    if (data.is_high_score) {
                        resultHTML += '<span class="high-score-badge">🌟 HIGH SCORE!</span>';
                    }
                    
                    resultHTML += `
                            <div style="margin-top: 1rem;">
                                <a href="/leaderboards" class="btn btn-primary">View Leaderboards</a>
                            </div>
                        </div>
                    `;
                    
                    resultDiv.innerHTML = resultHTML;
                    resultDiv.className = 'score-result success';
                    
                    // Hide the form
                    document.querySelector('.score-form').style.display = 'none';
                    
                } else {
                    resultDiv.innerHTML = `<div class="error">Error: ${data.error}</div>`;
                    resultDiv.className = 'score-result error';
                }
                
                resultDiv.style.display = 'block';
                
            } catch (error) {
                resultDiv.innerHTML = '<div class="error">Network error. Please try again.</div>';
                resultDiv.className = 'score-result error';
                resultDiv.style.display = 'block';
            }
            
            this.disabled = false;
            this.innerHTML = '<span class="material-icons">send</span> Submit Score';
        });
    }

    // Skip score button
    const skipScoreBtn = document.getElementById('skip-score-btn');
    if (skipScoreBtn) {
        skipScoreBtn.addEventListener('click', function() {
            document.getElementById('score-modal').style.display = 'none';
        });
    }

    // Close score modal
    const closeScoreBtn = document.getElementById('close-score');
    if (closeScoreBtn) {
        closeScoreBtn.addEventListener('click', function() {
            document.getElementById('score-modal').style.display = 'none';
        });
    }
});

// Function to handle game completion and show score modal
async function handleGameCompletion() {
    try {
        const response = await fetch('/api/get_final_results');
        const data = await response.json();
        
        if (data.success) {
            showScoreSubmissionModal(data.results);
        }
    } catch (error) {
        console.error('Error getting final results:', error);
    }
} 