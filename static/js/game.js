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

// Game mode information
const GAME_MODE_INFO = {
    normal: {
        name: 'Normal Mode',
        icon: '🎯',
        description: 'Classic token hunting experience',
        color: 'normal',
        rules: [
            'Find words with similar meanings to the target word',
            'Closer token IDs give higher scores',
            'You have one guess per round',
            'Perfect matches (distance 0) give maximum points'
        ],
        tips: 'Think about synonyms, related concepts, and words that might appear in similar contexts!'
    },
    synonym: {
        name: 'Synonym Hunt',
        icon: '🤝',
        description: 'Find words with similar meanings',
        color: 'synonym', 
        rules: [
            'Look for words that mean the same thing as the target',
            'Exact synonyms often have close token IDs',
            'Consider different word forms (big/large, happy/glad)',
            'Bonus points for perfect semantic matches'
        ],
        tips: 'Use a thesaurus mindset - what other words could replace the target word in a sentence?'
    },
    antonym: {
        name: 'Antonym Challenge',
        icon: '⚡',
        description: 'Find words with opposite meanings',
        color: 'antonym',
        rules: [
            'Find words that mean the opposite of the target',
            'Larger distances between tokens can give higher scores',
            'Think about semantic opposites, not just negatives',
            'Consider context - what would be the opposite in this situation?'
        ],
        tips: 'Opposite meanings often have distant token IDs - embrace the challenge of finding true opposites!'
    },
    speed: {
        name: 'Speed Mode',
        icon: '⚡',
        description: 'Race against time',
        color: 'speed',
        rules: [
            'Same rules as Normal Mode, but with time pressure',
            'Each round has a strict time limit',
            'Bonus points for quick, accurate answers',
            'Time out = 0 points for that round'
        ],
        tips: 'Trust your instincts! The first synonym that comes to mind is often correct.'
    }
};

// Mobile touch and gesture support
let touchSupport = {
    startX: 0,
    startY: 0,
    endX: 0,
    endY: 0,
    minSwipeDistance: 50,
    isTouch: false
};

// Initialize the game
function initializeGame() {
    console.log('🎮 Initializing Token Quest Web Version');
    
    // Get DOM elements
    elements = {
        // Mode display elements
        gameModeDisplay: document.getElementById('game-mode-display'),
        modeIcon: document.getElementById('mode-icon'),
        modeName: document.getElementById('mode-name'),
        modeDescription: document.getElementById('mode-description'),
        difficultyValue: document.getElementById('difficulty-value'),
        categoryValue: document.getElementById('category-value'),
        timeLimitDetail: document.getElementById('time-limit-detail'),
        timeLimitValue: document.getElementById('time-limit-value'),
        modeHelpBtn: document.getElementById('mode-help-btn'),
        
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
        modeHelpModal: document.getElementById('mode-help-modal'),
        closeModeHelp: document.getElementById('close-mode-help'),
        modeHelpTitle: document.getElementById('mode-help-title'),
        modeHelpContent: document.getElementById('mode-help-content'),
        modeHelpTips: document.getElementById('mode-help-tips'),
        
        // Loading
        loading: document.getElementById('loading')
    };
    
    // Set up event listeners
    setupEventListeners();
    
    // Initialize mobile support
    initializeMobileSupport();
    addMobileTouchCSS();
    
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
    
    // Mode help modal handlers
    elements.modeHelpBtn.addEventListener('click', showModeHelpModal);
    elements.closeModeHelp.addEventListener('click', closeModeHelpModal);
    elements.modeHelpModal.addEventListener('click', function(e) {
        if (e.target === elements.modeHelpModal) {
            closeModeHelpModal();
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

// Add mobile-specific enhancements
function initializeMobileSupport() {
    // Detect touch capability
    touchSupport.isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    
    if (touchSupport.isTouch) {
        console.log('📱 Touch device detected - enabling mobile optimizations');
        document.body.classList.add('touch-device');
        
        // Add touch event listeners for swipe gestures
        setupSwipeGestures();
        
        // Enhance button feedback
        enhanceTouchFeedback();
        
        // Optimize input behavior
        optimizeInputsForMobile();
        
        // Add haptic feedback support
        setupHapticFeedback();
    }
}

function setupSwipeGestures() {
    // Swipe to navigate hints
    elements.hintModal.addEventListener('touchstart', handleTouchStart, { passive: true });
    elements.hintModal.addEventListener('touchend', handleTouchEnd, { passive: true });
    
    // Swipe on game cards for quick actions
    if (elements.resultsCard) {
        elements.resultsCard.addEventListener('touchstart', handleTouchStart, { passive: true });
        elements.resultsCard.addEventListener('touchend', handleTouchEnd, { passive: true });
    }
}

function handleTouchStart(e) {
    const touch = e.touches[0];
    touchSupport.startX = touch.clientX;
    touchSupport.startY = touch.clientY;
}

function handleTouchEnd(e) {
    const touch = e.changedTouches[0];
    touchSupport.endX = touch.clientX;
    touchSupport.endY = touch.clientY;
    
    const deltaX = touchSupport.endX - touchSupport.startX;
    const deltaY = touchSupport.endY - touchSupport.startY;
    
    // Check if swipe distance is significant
    if (Math.abs(deltaX) > touchSupport.minSwipeDistance && Math.abs(deltaX) > Math.abs(deltaY)) {
        if (deltaX > 0) {
            // Swipe right
            handleSwipeRight(e.target);
        } else {
            // Swipe left
            handleSwipeLeft(e.target);
        }
    }
}

function handleSwipeRight(target) {
    // If in hint modal, go to previous hint tab
    if (elements.hintModal.style.display !== 'none') {
        const currentTab = document.querySelector('.tab-btn.active');
        const tabs = document.querySelectorAll('.tab-btn');
        const currentIndex = Array.from(tabs).indexOf(currentTab);
        if (currentIndex > 0) {
            tabs[currentIndex - 1].click();
            triggerHapticFeedback('light');
        }
    }
}

function handleSwipeLeft(target) {
    // If in hint modal, go to next hint tab
    if (elements.hintModal.style.display !== 'none') {
        const currentTab = document.querySelector('.tab-btn.active');
        const tabs = document.querySelectorAll('.tab-btn');
        const currentIndex = Array.from(tabs).indexOf(currentTab);
        if (currentIndex < tabs.length - 1) {
            tabs[currentIndex + 1].click();
            triggerHapticFeedback('light');
        }
    }
}

function enhanceTouchFeedback() {
    // Add enhanced touch feedback to all interactive elements
    const interactiveElements = document.querySelectorAll('.btn, .action-btn, .submit-button, .theme-btn, .mode-card');
    
    interactiveElements.forEach(element => {
        element.addEventListener('touchstart', function() {
            this.classList.add('touch-active');
            triggerHapticFeedback('light');
        }, { passive: true });
        
        element.addEventListener('touchend', function() {
            setTimeout(() => {
                this.classList.remove('touch-active');
            }, 150);
        }, { passive: true });
        
        element.addEventListener('touchcancel', function() {
            this.classList.remove('touch-active');
        }, { passive: true });
    });
}

function optimizeInputsForMobile() {
    // Prevent zoom on input focus (iOS)
    elements.guessInput.addEventListener('focus', function() {
        this.style.fontSize = '16px';
    });
    
    // Add better mobile keyboard handling
    elements.guessInput.addEventListener('keyup', function(e) {
        if (e.key === 'Enter' && touchSupport.isTouch) {
            e.preventDefault();
            this.blur(); // Hide mobile keyboard
            if (elements.submitBtn && !elements.submitBtn.disabled) {
                elements.submitBtn.click();
            }
        }
    });
    
    // Smooth scroll to input when focused on mobile
    elements.guessInput.addEventListener('focus', function() {
        if (touchSupport.isTouch) {
            setTimeout(() => {
                this.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'center',
                    inline: 'nearest'
                });
            }, 300); // Wait for keyboard animation
        }
    });
}

function setupHapticFeedback() {
    // Modern browsers with Vibration API
    if ('vibrate' in navigator) {
        console.log('📳 Haptic feedback supported');
    }
}

function triggerHapticFeedback(type = 'light') {
    if (!touchSupport.isTouch || !('vibrate' in navigator)) return;
    
    const patterns = {
        light: [10],
        medium: [20],
        heavy: [30],
        success: [10, 50, 10],
        error: [50, 30, 50, 30, 50]
    };
    
    navigator.vibrate(patterns[type] || patterns.light);
}

// Enhanced mobile-specific UI feedback
function showMobileSuccessFeedback(message) {
    const feedback = document.createElement('div');
    feedback.className = 'success-feedback mobile-feedback';
    feedback.textContent = message;
    feedback.style.cssText = `
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 10000;
        max-width: 90%;
        text-align: center;
    `;
    
    document.body.appendChild(feedback);
    triggerHapticFeedback('success');
    
    setTimeout(() => {
        feedback.style.opacity = '0';
        setTimeout(() => feedback.remove(), 300);
    }, 2000);
}

function showMobileErrorFeedback(message) {
    const feedback = document.createElement('div');
    feedback.className = 'error-feedback mobile-feedback';
    feedback.textContent = message;
    feedback.style.cssText = `
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 10000;
        max-width: 90%;
        text-align: center;
    `;
    
    document.body.appendChild(feedback);
    triggerHapticFeedback('error');
    
    setTimeout(() => {
        feedback.style.opacity = '0';
        setTimeout(() => feedback.remove(), 300);
    }, 2000);
}

// Enhanced loading states for mobile
function showMobileLoading(show, message = 'Loading...') {
    const existingLoader = document.getElementById('mobile-loader');
    
    if (show) {
        if (existingLoader) return;
        
        const loader = document.createElement('div');
        loader.id = 'mobile-loader';
        loader.innerHTML = `
            <div class="mobile-loader-backdrop">
                <div class="mobile-loader-content">
                    <div class="loading-robot">🤖</div>
                    <div class="loading-text">${message}</div>
                </div>
            </div>
        `;
        loader.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 10001;
            display: flex;
            align-items: center;
            justify-content: center;
        `;
        
        document.body.appendChild(loader);
    } else {
        if (existingLoader) {
            existingLoader.style.opacity = '0';
            setTimeout(() => existingLoader.remove(), 300);
        }
    }
}

async function startNewGame() {
    console.log('🚀 Starting new game...');
    
    if (touchSupport.isTouch) {
        showMobileLoading(true, 'Starting new game...');
        triggerHapticFeedback('medium');
    } else {
        showLoading(true);
    }
    
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
            gameState.gameCompleted = false;
            
            // Show achievement notifications if any
            if (data.newly_unlocked_achievements && data.newly_unlocked_achievements.length > 0) {
                showAchievementNotifications(data.newly_unlocked_achievements);
            }
            
            // Update mode display with current settings
            updateModeDisplay(data.settings || gameSettings);
            
            // Update UI
            updateGameDisplay();
            enableGameControls();
            
            // Start timer if speed mode
            if (gameState.isSpeedMode) {
                startRoundTimer();
            }
            
            // Focus on input
            elements.guessInput.focus();
            
            if (touchSupport.isTouch) {
                showMobileSuccessFeedback('Game started! 🎮');
            }
            
        } else {
            console.error('❌ Failed to start game:', data);
            showError('Failed to start game: ' + (data.error || 'Unknown error'));
            if (touchSupport.isTouch) {
                showMobileErrorFeedback('Failed to start game');
            }
        }
        
    } catch (error) {
        console.error('❌ Error starting game:', error);
        showError('Network error: Could not start game');
        if (touchSupport.isTouch) {
            showMobileErrorFeedback('Network error occurred');
        }
    } finally {
        if (touchSupport.isTouch) {
            showMobileLoading(false);
        } else {
            showLoading(false);
        }
    }
}

async function submitGuess() {
    const guess = elements.guessInput.value.trim();
    
    if (!guess || !gameState.gameStarted) {
        return;
    }
    
    console.log('🤔 Submitting guess:', guess);
    
    if (touchSupport.isTouch) {
        triggerHapticFeedback('medium');
        // Hide mobile keyboard
        elements.guessInput.blur();
        showMobileLoading(true, 'Processing guess...');
    } else {
        showLoading(true);
    }
    
    try {
        const response = await fetch('/api/submit_guess', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ guess: guess })
        });
        
        const data = await response.json();
        
        if (data.success && data.result.valid_guess) {
            console.log('✅ Guess processed:', data.result);
            
            // Stop timer if speed mode
            if (gameState.isSpeedMode) {
                stopTimer();
            }
            
            // Update game state
            gameState.attemptsLeft = data.result.attempts_left || 0;
            gameState.score = data.result.total_score || gameState.score;
            
            if (data.result.correct) {
                gameState.correctGuesses++;
                if (touchSupport.isTouch) {
                    triggerHapticFeedback('success');
                }
            }
            
            // Show achievement notifications if any
            if (data.newly_unlocked_achievements && data.newly_unlocked_achievements.length > 0) {
                showAchievementNotifications(data.newly_unlocked_achievements);
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
                // Check if game ended from the API response
                if (data.result.game_ended || gameState.currentRound >= gameState.maxRounds) {
                    console.log('🎉 Game completed! Final results:', {
                        score: gameState.score,
                        correctGuesses: gameState.correctGuesses,
                        rounds: gameState.maxRounds
                    });
                    showGameCompleted();
                } else {
                    startNextRound();
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
            
            if (touchSupport.isTouch) {
                triggerHapticFeedback('error');
            }
            
            // Hide the error message after 3 seconds
            setTimeout(() => {
                elements.resultsCard.style.display = 'none';
            }, 3000);
        }
        
    } catch (error) {
        console.error('❌ Error submitting guess:', error);
        showError('Network error: Could not submit guess');
        if (touchSupport.isTouch) {
            showMobileErrorFeedback('Network error occurred');
        }
    } finally {
        if (touchSupport.isTouch) {
            showMobileLoading(false);
        } else {
            showLoading(false);
        }
    }
}

// Add CSS for touch states
function addMobileTouchCSS() {
    const style = document.createElement('style');
    style.textContent = `
        .touch-device .touch-active {
            transform: scale(0.95) !important;
            opacity: 0.8 !important;
        }
        
        .mobile-feedback {
            font-weight: 600;
            font-size: 0.9rem;
            border-radius: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            transition: opacity 0.3s ease;
        }
        
        .mobile-loader-backdrop {
            background: rgba(0,0,0,0.7);
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .mobile-loader-content {
            background: white;
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            min-width: 200px;
        }
        
        .loading-text {
            margin-top: 1rem;
            font-weight: 600;
            color: #333;
        }
        
        @media (max-width: 480px) {
            .mobile-loader-content {
                margin: 0 1rem;
                padding: 1.5rem;
            }
        }
    `;
    document.head.appendChild(style);
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
            
            // Show achievement notifications if any
            if (data.newly_unlocked_achievements && data.newly_unlocked_achievements.length > 0) {
                showAchievementNotifications(data.newly_unlocked_achievements);
            }
            
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
                if (gameState.currentRound >= gameState.maxRounds) {
                    console.log('🎉 Game completed after timeout! Final results:', {
                        score: gameState.score,
                        correctGuesses: gameState.correctGuesses,
                        rounds: gameState.maxRounds
                    });
                    showGameCompleted();
                } else {
                    startNextRound();
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
    
    // Calculate accuracy
    const accuracy = gameState.maxRounds > 0 ? (gameState.correctGuesses / gameState.maxRounds * 100) : 0;
    
    // Determine performance level
    let performanceLevel = '';
    let performanceIcon = '';
    let performanceColor = '';
    
    if (accuracy >= 80) {
        performanceLevel = 'Outstanding!';
        performanceIcon = '🏆';
        performanceColor = '#FFD700';
    } else if (accuracy >= 60) {
        performanceLevel = 'Great Job!';
        performanceIcon = '🥇';
        performanceColor = '#4CAF50';
    } else if (accuracy >= 40) {
        performanceLevel = 'Good Effort!';
        performanceIcon = '🥈';
        performanceColor = '#FF9800';
    } else {
        performanceLevel = 'Keep Practicing!';
        performanceIcon = '🥉';
        performanceColor = '#FF6B6B';
    }
    
    elements.resultContent.innerHTML = `
        <div class="result-excellent game-complete-summary">
            <div class="performance-header" style="color: ${performanceColor}">
                <h2>${performanceIcon} ${performanceLevel}</h2>
            </div>
            
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">${gameState.score}</div>
                    <div class="stat-label">Total Points</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${accuracy.toFixed(1)}%</div>
                    <div class="stat-label">Accuracy</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${gameState.correctGuesses}/${gameState.maxRounds}</div>
                    <div class="stat-label">Correct</div>
                </div>
            </div>
            
            <div class="completion-message">
                <p>🎯 Game Complete! Submit your score to the leaderboard!</p>
                <p><em>Your score modal should appear shortly...</em></p>
            </div>
            
            <div class="action-buttons">
                <button class="btn btn-primary" onclick="handleGameCompletion()">
                    <span class="material-icons">leaderboard</span>
                    Submit Score
                </button>
                <button class="btn btn-secondary" onclick="startCompletelyNewGame()">
                    <span class="material-icons">play_arrow</span>
                    Play Again
                </button>
            </div>
        </div>
    `;
    
    elements.resultsCard.style.display = 'block';
    elements.resultsCard.scrollIntoView({ behavior: 'smooth' });
    
    gameState.gameCompleted = true;
    gameState.gameStarted = false;
    
    // Show score submission modal after a short delay
    setTimeout(() => {
        handleGameCompletion();
    }, 1000);
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
function initializeScoreHandlers() {
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
                    
                    // Show achievement notifications if any
                    if (data.newly_unlocked_achievements && data.newly_unlocked_achievements.length > 0) {
                        showAchievementNotifications(data.newly_unlocked_achievements);
                    }
                    
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
}

// Function to handle game completion and show score modal
async function handleGameCompletion() {
    console.log('🎯 Handling game completion...');
    try {
        const response = await fetch('/api/get_final_results');
        const data = await response.json();
        
        console.log('📊 Final results response:', data);
        
        if (data.success) {
            console.log('✅ Showing score submission modal');
            showScoreSubmissionModal(data.results);
        } else {
            console.error('❌ Failed to get final results:', data.error);
            alert('Could not load final results: ' + data.error);
        }
    } catch (error) {
        console.error('❌ Error getting final results:', error);
        alert('Network error getting final results. You can still play again!');
    }
}

// ===== MODE DISPLAY FUNCTIONS =====

// Update the mode display with current settings
function updateModeDisplay(settings) {
    const gameMode = settings.game_mode || 'normal';
    const isSpeedMode = settings.is_speed_mode || false;
    const actualMode = isSpeedMode ? 'speed' : gameMode;
    
    const modeInfo = GAME_MODE_INFO[actualMode] || GAME_MODE_INFO.normal;
    
    // Update mode display elements
    elements.modeIcon.textContent = modeInfo.icon;
    elements.modeName.textContent = modeInfo.name;
    elements.modeDescription.textContent = modeInfo.description;
    
    // Update difficulty and category
    elements.difficultyValue.textContent = capitalizeFirst(settings.difficulty || 'mixed');
    elements.categoryValue.textContent = capitalizeFirst(settings.category || 'all');
    
    // Show/hide time limit for speed mode
    if (isSpeedMode && settings.time_limit) {
        elements.timeLimitDetail.style.display = 'flex';
        elements.timeLimitValue.textContent = settings.time_limit + 's';
    } else {
        elements.timeLimitDetail.style.display = 'none';
    }
    
    // Update mode-specific styling
    elements.gameModeDisplay.className = `game-mode-display mode-${modeInfo.color}`;
    
    console.log('🎮 Mode display updated:', modeInfo.name);
}

// Show the mode help modal
function showModeHelpModal() {
    const savedSettings = localStorage.getItem('game-settings');
    let gameSettings = {
        game_mode: 'normal',
        is_speed_mode: false
    };
    
    if (savedSettings) {
        gameSettings = {...gameSettings, ...JSON.parse(savedSettings)};
    }
    
    const gameMode = gameSettings.game_mode || 'normal';
    const isSpeedMode = gameSettings.is_speed_mode || false;
    const actualMode = isSpeedMode ? 'speed' : gameMode;
    
    const modeInfo = GAME_MODE_INFO[actualMode] || GAME_MODE_INFO.normal;
    
    // Update modal title
    elements.modeHelpTitle.innerHTML = `${modeInfo.icon} ${modeInfo.name} Guide`;
    
    // Create help content
    const helpContent = `
        <div class="mode-help-section">
            <h4>📋 How to Play</h4>
            <p>${modeInfo.description}</p>
            <ul class="mode-help-list">
                ${modeInfo.rules.map(rule => `<li>${rule}</li>`).join('')}
            </ul>
        </div>
        
        <div class="mode-help-section">
            <h4>🎯 Current Settings</h4>
            <p><strong>Difficulty:</strong> ${capitalizeFirst(gameSettings.difficulty || 'mixed')}</p>
            <p><strong>Category:</strong> ${capitalizeFirst(gameSettings.category || 'all')}</p>
            ${isSpeedMode && gameSettings.time_limit ? 
                `<p><strong>Time Limit:</strong> ${gameSettings.time_limit} seconds per round</p>` : ''
            }
        </div>
    `;
    
    const tipsContent = `
        <h4>💡 Pro Tips</h4>
        <p>${modeInfo.tips}</p>
    `;
    
    elements.modeHelpContent.innerHTML = helpContent;
    elements.modeHelpTips.innerHTML = tipsContent;
    
    // Show modal
    elements.modeHelpModal.style.display = 'flex';
    
    console.log('📖 Mode help modal shown for:', modeInfo.name);
}

// Close the mode help modal
function closeModeHelpModal() {
    elements.modeHelpModal.style.display = 'none';
}

// Helper function to capitalize first letter
function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// Initialize mode display on page load
function initializeModeDisplay() {
    const savedSettings = localStorage.getItem('game-settings');
    let gameSettings = {
        game_mode: 'normal',
        difficulty: 'mixed',
        category: 'all',
        is_speed_mode: false,
        time_limit: 30
    };
    
    if (savedSettings) {
        gameSettings = {...gameSettings, ...JSON.parse(savedSettings)};
    }
    
    updateModeDisplay(gameSettings);
}

// Update the DOM ready event listener to include all initialization functions
document.addEventListener('DOMContentLoaded', function() {
    initializeGame();
    initializeModeDisplay();
    initializeScoreHandlers();
});