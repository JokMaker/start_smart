/**
 * Intelligent Loading System
 * Creates engaging loading experiences with progress tracking
 */

class LoadingSystem {
    constructor() {
        this.isLoading = false;
        this.currentProgress = 0;
        this.loadingSteps = [
            { message: "Initializing StartSmart...", progress: 20 },
            { message: "Loading job opportunities...", progress: 40 },
            { message: "Connecting to mentors...", progress: 60 },
            { message: "Setting up your dashboard...", progress: 80 },
            { message: "Almost ready!", progress: 100 }
        ];
        this.init();
    }

    init() {
        this.createLoadingHTML();
        this.setupPageLoadHandler();
    }

    createLoadingHTML() {
        const loadingHTML = `
            <div id="smartLoading" class="smart-loading-overlay">
                <div class="loading-container">
                    <!-- Animated Logo -->
                    <div class="loading-logo">
                        <div class="logo-circle">
                            <i class="fas fa-rocket"></i>
                        </div>
                        <h2 class="loading-title">StartSmart</h2>
                        <p class="loading-subtitle">Launching Your Future</p>
                    </div>

                    <!-- Progress Section -->
                    <div class="loading-progress-section">
                        <div class="progress-container">
                            <div class="progress-bar">
                                <div class="progress-fill" id="progressFill"></div>
                                <div class="progress-particles"></div>
                            </div>
                            <div class="progress-percentage">
                                <span id="progressText">0%</span>
                            </div>
                        </div>
                        
                        <div class="loading-message">
                            <span id="loadingMessage">Preparing your experience...</span>
                        </div>
                    </div>

                    <!-- Feature Highlights -->
                    <div class="loading-features">
                        <div class="feature-item">
                            <i class="fas fa-briefcase"></i>
                            <span>1000+ Job Opportunities</span>
                        </div>
                        <div class="feature-item">
                            <i class="fas fa-rocket"></i>
                            <span>500+ Startups</span>
                        </div>
                        <div class="feature-item">
                            <i class="fas fa-handshake"></i>
                            <span>Expert Mentorship</span>
                        </div>
                    </div>

                    <!-- Loading Animation -->
                    <div class="loading-animation">
                        <div class="floating-elements">
                            <div class="float-element">💼</div>
                            <div class="float-element">🚀</div>
                            <div class="float-element">💡</div>
                            <div class="float-element">🎯</div>
                            <div class="float-element">📈</div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Add to document if not exists
        if (!document.getElementById('smartLoading')) {
            document.body.insertAdjacentHTML('afterbegin', loadingHTML);
        }
    }

    show(customSteps = null) {
        this.isLoading = true;
        this.currentProgress = 0;
        
        if (customSteps) {
            this.loadingSteps = customSteps;
        }

        const loadingOverlay = document.getElementById('smartLoading');
        if (loadingOverlay) {
            loadingOverlay.style.display = 'flex';
            setTimeout(() => {
                loadingOverlay.classList.add('active');
                this.startProgressAnimation();
            }, 100);
        }
    }

    hide() {
        this.isLoading = false;
        const loadingOverlay = document.getElementById('smartLoading');
        
        if (loadingOverlay) {
            loadingOverlay.classList.add('fade-out');
            setTimeout(() => {
                loadingOverlay.style.display = 'none';
                loadingOverlay.classList.remove('active', 'fade-out');
                this.resetProgress();
            }, 800);
        }
    }

    startProgressAnimation() {
        let stepIndex = 0;
        
        const animateStep = () => {
            if (!this.isLoading || stepIndex >= this.loadingSteps.length) {
                return;
            }

            const step = this.loadingSteps[stepIndex];
            this.updateProgress(step.progress, step.message);
            
            stepIndex++;
            
            if (stepIndex < this.loadingSteps.length) {
                setTimeout(animateStep, 800 + Math.random() * 400);
            } else {
                setTimeout(() => {
                    if (this.isLoading) {
                        this.hide();
                    }
                }, 1000);
            }
        };

        setTimeout(animateStep, 500);
    }

    updateProgress(targetProgress, message) {
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        const loadingMessage = document.getElementById('loadingMessage');
        
        if (progressFill && progressText && loadingMessage) {
            // Animate progress bar
            progressFill.style.width = `${targetProgress}%`;
            
            // Animate percentage counter
            let currentProgress = this.currentProgress;
            const animateProgress = () => {
                if (currentProgress < targetProgress) {
                    currentProgress += 2;
                    progressText.textContent = `${Math.min(currentProgress, targetProgress)}%`;
                    requestAnimationFrame(animateProgress);
                }
            };
            animateProgress();
            
            // Update message with fade effect
            loadingMessage.style.opacity = '0';
            setTimeout(() => {
                loadingMessage.textContent = message;
                loadingMessage.style.opacity = '1';
            }, 200);
            
            this.currentProgress = targetProgress;
        }
    }

    resetProgress() {
        this.currentProgress = 0;
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        const loadingMessage = document.getElementById('loadingMessage');
        
        if (progressFill && progressText && loadingMessage) {
            progressFill.style.width = '0%';
            progressText.textContent = '0%';
            loadingMessage.textContent = 'Preparing your experience...';
            loadingMessage.style.opacity = '1';
        }
    }

    setupPageLoadHandler() {
        // Show loading on page transitions
        document.addEventListener('DOMContentLoaded', () => {
            // Hide loading when page is ready
            if (this.isLoading) {
                setTimeout(() => this.hide(), 500);
            }
        });

        // Show loading for form submissions
        document.addEventListener('submit', (e) => {
            if (e.target.tagName === 'FORM') {
                this.show([
                    { message: "Processing your request...", progress: 30 },
                    { message: "Validating information...", progress: 60 },
                    { message: "Updating database...", progress: 90 },
                    { message: "Complete!", progress: 100 }
                ]);
            }
        });

        // Show loading for navigation
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href]');
            if (link && !link.href.includes('#') && !link.target) {
                this.show();
            }
        });
    }
}

// Initialize loading system
const smartLoading = new LoadingSystem();

// Add loading styles
const loadingStyles = document.createElement('style');
loadingStyles.textContent = `
    .smart-loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        z-index: 99999;
        display: none;
        justify-content: center;
        align-items: center;
        opacity: 0;
        transition: opacity 0.5s ease;
    }

    .smart-loading-overlay.active {
        opacity: 1;
    }

    .smart-loading-overlay.fade-out {
        opacity: 0;
        transition: opacity 0.8s ease;
    }

    .loading-container {
        text-align: center;
        color: white;
        max-width: 500px;
        padding: 40px;
    }

    .loading-logo {
        margin-bottom: 40px;
        animation: logoFloat 3s ease-in-out infinite;
    }

    @keyframes logoFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    .logo-circle {
        width: 100px;
        height: 100px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 20px;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        animation: logoSpin 4s linear infinite;
    }

    @keyframes logoSpin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .logo-circle i {
        font-size: 2.5rem;
        color: #ffd700;
        animation: rocketBounce 2s ease-in-out infinite;
    }

    @keyframes rocketBounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }

    .loading-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 8px;
        background: linear-gradient(45deg, #ffd700, #ffed4e);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: titleGlow 2s ease-in-out infinite alternate;
    }

    @keyframes titleGlow {
        from { filter: brightness(1); }
        to { filter: brightness(1.2); }
    }

    .loading-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-bottom: 0;
    }

    .loading-progress-section {
        margin: 40px 0;
    }

    .progress-container {
        margin-bottom: 20px;
    }

    .progress-bar {
        width: 100%;
        height: 8px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        margin-bottom: 12px;
        position: relative;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #ffd700, #ffed4e, #ffd700);
        border-radius: 20px;
        width: 0%;
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        background-size: 200% 100%;
        animation: progressShimmer 2s linear infinite;
    }

    @keyframes progressShimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    .progress-particles {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        border-radius: 20px;
    }

    .progress-particles::before {
        content: '';
        position: absolute;
        top: 50%;
        left: -10px;
        width: 6px;
        height: 6px;
        background: #ffd700;
        border-radius: 50%;
        animation: particleMove 2s linear infinite;
    }

    @keyframes particleMove {
        0% { left: -10px; opacity: 0; }
        50% { opacity: 1; }
        100% { left: calc(100% + 10px); opacity: 0; }
    }

    .progress-percentage {
        text-align: center;
        font-size: 1.2rem;
        font-weight: 600;
    }

    .loading-message {
        font-size: 1rem;
        opacity: 0.9;
        min-height: 24px;
        transition: opacity 0.3s ease;
    }

    .loading-features {
        display: flex;
        justify-content: space-around;
        margin: 40px 0;
        flex-wrap: wrap;
        gap: 20px;
    }

    .feature-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        opacity: 0.8;
        animation: featurePulse 3s ease-in-out infinite;
    }

    .feature-item:nth-child(2) { animation-delay: 0.5s; }
    .feature-item:nth-child(3) { animation-delay: 1s; }

    @keyframes featurePulse {
        0%, 100% { opacity: 0.8; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.05); }
    }

    .feature-item i {
        font-size: 1.5rem;
        margin-bottom: 8px;
        color: #ffd700;
    }

    .feature-item span {
        font-size: 0.9rem;
        white-space: nowrap;
    }

    .loading-animation {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
    }

    .floating-elements {
        position: relative;
        width: 100%;
        height: 100%;
    }

    .float-element {
        position: absolute;
        font-size: 2rem;
        opacity: 0.1;
        animation: floatAround 15s linear infinite;
    }

    .float-element:nth-child(1) { 
        top: 10%; 
        left: 10%; 
        animation-delay: 0s; 
    }
    .float-element:nth-child(2) { 
        top: 20%; 
        right: 15%; 
        animation-delay: 3s; 
    }
    .float-element:nth-child(3) { 
        bottom: 30%; 
        left: 20%; 
        animation-delay: 6s; 
    }
    .float-element:nth-child(4) { 
        bottom: 20%; 
        right: 25%; 
        animation-delay: 9s; 
    }
    .float-element:nth-child(5) { 
        top: 50%; 
        left: 50%; 
        animation-delay: 12s; 
    }

    @keyframes floatAround {
        0% { transform: translate(0, 0) rotate(0deg); opacity: 0.1; }
        25% { transform: translate(50px, -30px) rotate(90deg); opacity: 0.3; }
        50% { transform: translate(-30px, 50px) rotate(180deg); opacity: 0.1; }
        75% { transform: translate(-50px, -20px) rotate(270deg); opacity: 0.3; }
        100% { transform: translate(0, 0) rotate(360deg); opacity: 0.1; }
    }

    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .loading-container {
            padding: 20px;
            max-width: 320px;
        }
        
        .loading-title {
            font-size: 2rem;
        }
        
        .logo-circle {
            width: 80px;
            height: 80px;
        }
        
        .logo-circle i {
            font-size: 2rem;
        }
        
        .loading-features {
            flex-direction: column;
            gap: 16px;
        }
        
        .feature-item span {
            font-size: 0.8rem;
        }
    }
`;

document.head.appendChild(loadingStyles);

// Show loading on initial page load
document.addEventListener('DOMContentLoaded', () => {
    // Only show if page is not from cache
    if (!window.performance || performance.navigation.type !== 2) {
        smartLoading.show();
    }
});
