/**
 * Demo Mode - Interactive Presentation Features
 * Adds guided tour and live demonstration capabilities
 */

class DemoMode {
    constructor() {
        this.isActive = false;
        this.currentStep = 0;
        this.steps = [];
        this.overlay = null;
        this.tooltip = null;
        this.init();
    }

    init() {
        this.createDemoButton();
        this.setupKeyboardShortcuts();
        this.defineDemoSteps();
    }

    createDemoButton() {
        const demoButton = document.createElement('div');
        demoButton.className = 'demo-mode-toggle';
        demoButton.innerHTML = `
            <button class="btn-demo" onclick="demoMode.toggle()">
                <i class="fas fa-play-circle"></i>
                <span>Demo Mode</span>
            </button>
        `;
        document.body.appendChild(demoButton);
    }

    defineDemoSteps() {
        this.steps = [
            {
                target: '.navbar-brand',
                title: '🚀 Welcome to StartSmart!',
                content: 'Africa\'s premier platform for connecting youth with job opportunities and entrepreneurship resources.',
                position: 'bottom'
            },
            {
                target: '.search-input-modern',
                title: '🔍 Smart Search',
                content: 'Our AI-powered search helps users find jobs, startups, and mentorship opportunities instantly.',
                position: 'bottom',
                action: () => this.simulateSearch()
            },
            {
                target: '.stat-card:first-child',
                title: '📊 Real-time Impact',
                content: 'Watch our live statistics showing active users, job placements, and startup success stories.',
                position: 'top',
                action: () => this.animateStats()
            },
            {
                target: '.btn-gradient',
                title: '💼 Job Marketplace',
                content: 'Browse thousands of verified job opportunities from top African companies and startups.',
                position: 'top'
            },
            {
                target: '.feature-icon-container',
                title: '🌟 Key Features',
                content: 'Job matching, startup incubation, mentorship programs, and skills development - all in one platform.',
                position: 'right'
            },
            {
                target: '.btn-outline-light:last-child',
                title: '🤝 Mentorship Network',
                content: 'Connect with industry experts and successful entrepreneurs for personalized career guidance.',
                position: 'top'
            }
        ];
    }

    toggle() {
        if (this.isActive) {
            this.stop();
        } else {
            this.start();
        }
    }

    start() {
        this.isActive = true;
        this.currentStep = 0;
        this.createOverlay();
        this.showStep(0);
        
        // Update demo button
        const btn = document.querySelector('.btn-demo');
        btn.innerHTML = `
            <i class="fas fa-stop-circle"></i>
            <span>Stop Demo</span>
        `;
        btn.classList.add('active');
    }

    stop() {
        this.isActive = false;
        this.removeOverlay();
        this.removeTooltip();
        
        // Reset demo button
        const btn = document.querySelector('.btn-demo');
        btn.innerHTML = `
            <i class="fas fa-play-circle"></i>
            <span>Demo Mode</span>
        `;
        btn.classList.remove('active');
    }

    createOverlay() {
        this.overlay = document.createElement('div');
        this.overlay.className = 'demo-overlay';
        document.body.appendChild(this.overlay);
    }

    removeOverlay() {
        if (this.overlay) {
            this.overlay.remove();
            this.overlay = null;
        }
    }

    showStep(stepIndex) {
        if (stepIndex >= this.steps.length) {
            this.stop();
            this.showCompletionMessage();
            return;
        }

        const step = this.steps[stepIndex];
        const target = document.querySelector(step.target);
        
        if (!target) {
            this.nextStep();
            return;
        }

        this.highlightElement(target);
        this.showTooltip(target, step);
        
        // Execute step action if defined
        if (step.action) {
            setTimeout(step.action, 500);
        }
    }

    highlightElement(element) {
        // Remove previous highlights
        document.querySelectorAll('.demo-highlight').forEach(el => {
            el.classList.remove('demo-highlight');
        });
        
        // Add highlight to current element
        element.classList.add('demo-highlight');
        
        // Scroll element into view
        element.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center',
            inline: 'center'
        });
    }

    showTooltip(target, step) {
        this.removeTooltip();
        
        this.tooltip = document.createElement('div');
        this.tooltip.className = 'demo-tooltip';
        this.tooltip.innerHTML = `
            <div class="tooltip-header">
                <h4>${step.title}</h4>
                <span class="step-counter">${this.currentStep + 1}/${this.steps.length}</span>
            </div>
            <div class="tooltip-content">
                <p>${step.content}</p>
            </div>
            <div class="tooltip-footer">
                <button class="btn btn-sm btn-outline-secondary" onclick="demoMode.previousStep()">
                    <i class="fas fa-arrow-left"></i> Previous
                </button>
                <button class="btn btn-sm btn-primary" onclick="demoMode.nextStep()">
                    Next <i class="fas fa-arrow-right"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="demoMode.stop()">
                    <i class="fas fa-times"></i> Exit
                </button>
            </div>
        `;
        
        document.body.appendChild(this.tooltip);
        this.positionTooltip(target, step.position);
    }

    positionTooltip(target, position) {
        const targetRect = target.getBoundingClientRect();
        const tooltipRect = this.tooltip.getBoundingClientRect();
        
        let top, left;
        
        switch (position) {
            case 'top':
                top = targetRect.top - tooltipRect.height - 20;
                left = targetRect.left + (targetRect.width - tooltipRect.width) / 2;
                break;
            case 'bottom':
                top = targetRect.bottom + 20;
                left = targetRect.left + (targetRect.width - tooltipRect.width) / 2;
                break;
            case 'left':
                top = targetRect.top + (targetRect.height - tooltipRect.height) / 2;
                left = targetRect.left - tooltipRect.width - 20;
                break;
            case 'right':
                top = targetRect.top + (targetRect.height - tooltipRect.height) / 2;
                left = targetRect.right + 20;
                break;
            default:
                top = targetRect.bottom + 20;
                left = targetRect.left;
        }
        
        // Ensure tooltip stays within viewport
        top = Math.max(20, Math.min(top, window.innerHeight - tooltipRect.height - 20));
        left = Math.max(20, Math.min(left, window.innerWidth - tooltipRect.width - 20));
        
        this.tooltip.style.top = `${top + window.scrollY}px`;
        this.tooltip.style.left = `${left + window.scrollX}px`;
    }

    removeTooltip() {
        if (this.tooltip) {
            this.tooltip.remove();
            this.tooltip = null;
        }
    }

    nextStep() {
        this.currentStep++;
        this.showStep(this.currentStep);
    }

    previousStep() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.showStep(this.currentStep);
        }
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            if (!this.isActive) return;
            
            switch (e.key) {
                case 'ArrowRight':
                case ' ':
                    e.preventDefault();
                    this.nextStep();
                    break;
                case 'ArrowLeft':
                    e.preventDefault();
                    this.previousStep();
                    break;
                case 'Escape':
                    e.preventDefault();
                    this.stop();
                    break;
            }
        });
    }

    simulateSearch() {
        const searchInput = document.querySelector('.search-input-modern');
        if (searchInput) {
            const searchText = 'Software Developer';
            let i = 0;
            
            const typeText = () => {
                if (i < searchText.length) {
                    searchInput.value += searchText[i];
                    i++;
                    setTimeout(typeText, 100);
                } else {
                    // Simulate search results
                    setTimeout(() => {
                        searchInput.value = '';
                    }, 2000);
                }
            };
            
            searchInput.value = '';
            typeText();
        }
    }

    animateStats() {
        const statNumbers = document.querySelectorAll('.stat-number');
        statNumbers.forEach(stat => {
            const target = parseInt(stat.getAttribute('data-target'));
            let current = 0;
            const increment = target / 50;
            
            const animate = () => {
                if (current < target) {
                    current += increment;
                    stat.textContent = Math.floor(current);
                    requestAnimationFrame(animate);
                } else {
                    stat.textContent = target;
                }
            };
            
            animate();
        });
    }

    showCompletionMessage() {
        const completion = document.createElement('div');
        completion.className = 'demo-completion';
        completion.innerHTML = `
            <div class="completion-content">
                <div class="completion-icon">
                    <i class="fas fa-check-circle"></i>
                </div>
                <h3>Demo Complete! 🎉</h3>
                <p>You've explored the key features of StartSmart. Ready to get started?</p>
                <div class="completion-actions">
                    <a href="/register" class="btn btn-primary btn-lg">
                        <i class="fas fa-user-plus"></i> Sign Up Now
                    </a>
                    <button class="btn btn-outline-primary btn-lg" onclick="this.parentElement.parentElement.parentElement.remove()">
                        <i class="fas fa-redo"></i> Restart Demo
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(completion);
        
        setTimeout(() => {
            completion.remove();
        }, 10000);
    }
}

// Initialize demo mode
const demoMode = new DemoMode();

// Add demo mode styles
const demoStyles = document.createElement('style');
demoStyles.textContent = `
    .demo-mode-toggle {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 10000;
        animation: pulse 2s infinite;
    }

    .btn-demo {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 25px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .btn-demo:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
    }

    .btn-demo.active {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        animation: none;
    }

    .demo-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        z-index: 9999;
        backdrop-filter: blur(2px);
    }

    .demo-highlight {
        position: relative;
        z-index: 10001 !important;
        box-shadow: 0 0 0 4px rgba(255, 107, 107, 0.8), 0 0 0 8px rgba(255, 107, 107, 0.4) !important;
        border-radius: 8px !important;
        animation: demoHighlight 2s infinite;
    }

    @keyframes demoHighlight {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }

    .demo-tooltip {
        position: absolute;
        background: white;
        border-radius: 12px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        padding: 0;
        z-index: 10002;
        min-width: 300px;
        max-width: 400px;
        animation: tooltipAppear 0.3s ease-out;
    }

    @keyframes tooltipAppear {
        from { opacity: 0; transform: scale(0.9) translateY(10px); }
        to { opacity: 1; transform: scale(1) translateY(0); }
    }

    .tooltip-header {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        padding: 16px 20px;
        border-radius: 12px 12px 0 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .tooltip-header h4 {
        margin: 0;
        font-size: 1.1rem;
        font-weight: 600;
    }

    .step-counter {
        background: rgba(255, 255, 255, 0.2);
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .tooltip-content {
        padding: 20px;
    }

    .tooltip-content p {
        margin: 0;
        line-height: 1.5;
        color: #555;
    }

    .tooltip-footer {
        padding: 16px 20px;
        border-top: 1px solid #eee;
        display: flex;
        gap: 8px;
        justify-content: space-between;
    }

    .demo-completion {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 10003;
        background: white;
        border-radius: 16px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
        animation: completionAppear 0.5s ease-out;
    }

    @keyframes completionAppear {
        from { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
        to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
    }

    .completion-content {
        padding: 40px;
        text-align: center;
    }

    .completion-icon {
        font-size: 4rem;
        color: #2ecc71;
        margin-bottom: 20px;
        animation: checkBounce 0.6s ease-out 0.3s both;
    }

    @keyframes checkBounce {
        0% { transform: scale(0); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }

    .completion-content h3 {
        color: #333;
        margin-bottom: 16px;
    }

    .completion-content p {
        color: #666;
        margin-bottom: 30px;
    }

    .completion-actions {
        display: flex;
        gap: 16px;
        justify-content: center;
    }

    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .demo-mode-toggle {
            bottom: 10px;
            right: 10px;
        }
        
        .btn-demo {
            padding: 10px 16px;
            font-size: 0.9rem;
        }
        
        .demo-tooltip {
            min-width: 280px;
            max-width: 320px;
        }
        
        .tooltip-footer {
            flex-direction: column;
        }
        
        .completion-content {
            padding: 30px 20px;
        }
        
        .completion-actions {
            flex-direction: column;
        }
    }
`;

document.head.appendChild(demoStyles);
