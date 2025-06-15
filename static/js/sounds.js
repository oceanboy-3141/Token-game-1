// Sound Manager for Token Quest
class SoundManager {
    constructor() {
        this.soundEnabled = localStorage.getItem('soundEnabled') !== 'false';
        this.volume = parseFloat(localStorage.getItem('soundVolume')) || 0.7;
        
        this.audioContext = null;
        this.initAudioContext();
        this.createSoundEffects();
    }
    
    initAudioContext() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.log('Web Audio API not supported');
        }
    }
    
    createSoundEffects() {
        this.sounds = {
            click: () => this.createTone(800, 400, 0.1, 'sine', 0.3),
            win: () => this.createWinSound(),
            lose: () => this.createLoseSound(),
            success: () => this.createTone(1000, 1500, 0.3, 'sine', 0.3)
        };
    }
    
    createTone(startFreq, endFreq, duration, type, volume) {
        if (!this.soundEnabled || !this.audioContext) return;
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.frequency.setValueAtTime(startFreq, this.audioContext.currentTime);
        if (startFreq !== endFreq) {
            oscillator.frequency.exponentialRampToValueAtTime(endFreq, this.audioContext.currentTime + duration);
        }
        
        gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
        gainNode.gain.linearRampToValueAtTime(this.volume * volume, this.audioContext.currentTime + 0.01);
        gainNode.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + duration);
        
        oscillator.type = type;
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + duration);
    }
    
    createWinSound() {
        if (!this.soundEnabled || !this.audioContext) return;
        
        const frequencies = [523.25, 659.25, 783.99]; // C5, E5, G5
        frequencies.forEach((freq, index) => {
            setTimeout(() => this.createTone(freq, freq, 0.8, 'triangle', 0.4), index * 100);
        });
    }
    
    createLoseSound() {
        if (!this.soundEnabled || !this.audioContext) return;
        
        const frequencies = [440, 370, 220]; // A4, F#4, A3 - "dun dun DUN"
        frequencies.forEach((freq, index) => {
            setTimeout(() => this.createTone(freq, freq, 0.4, 'sawtooth', 0.5), index * 200);
        });
    }
    

    
    playSound(soundName) {
        if (this.sounds[soundName]) {
            this.sounds[soundName]();
        }
    }
    
    // Method to update settings from localStorage
    updateSettings() {
        this.soundEnabled = localStorage.getItem('soundEnabled') !== 'false';
        this.volume = parseFloat(localStorage.getItem('soundVolume')) || 0.7;
    }
    
    initializeButtonSounds() {
        document.addEventListener('click', (e) => {
            if (e.target.matches('button, .btn, .theme-btn, .mode-card')) {
                this.playSound('click');
            }
        });
        

        
    }
}

// Initialize sound manager
let soundManager;
document.addEventListener('DOMContentLoaded', () => {
    soundManager = new SoundManager();
    setTimeout(() => soundManager.initializeButtonSounds(), 500);
});

window.soundManager = soundManager; 