/**
 * StartSmart Animations
 * Custom animations for the StartSmart platform
 */

document.addEventListener('DOMContentLoaded', function() {
    // Animate elements when they come into view
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.animate-on-scroll');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in-up');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        
        elements.forEach(element => {
            observer.observe(element);
        });
    };
    
    // Animate stat counters
    const animateCounters = function() {
        const counters = document.querySelectorAll('.stat-number');
        
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-target') || counter.textContent);
            const duration = 1500; // Animation duration in milliseconds
            const startTime = performance.now();
            const startValue = 0;
            
            const updateCounter = function(currentTime) {
                const elapsedTime = currentTime - startTime;
                
                if (elapsedTime < duration) {
                    const progress = elapsedTime / duration;
                    const easedProgress = easeOutQuad(progress);
                    const currentValue = Math.floor(startValue + (target - startValue) * easedProgress);
                    
                    counter.textContent = currentValue;
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target;
                }
            };
            
            requestAnimationFrame(updateCounter);
        });
    };
    
    // Easing function for smoother animations
    function easeOutQuad(t) {
        return t * (2 - t);
    }
    
    // Initialize animations
    animateOnScroll();
    animateCounters();
    
    // Add animation classes to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.classList.add('animate-on-scroll');
        card.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Add animation classes to job listings
    const jobListings = document.querySelectorAll('.job-listing');
    jobListings.forEach((listing, index) => {
        listing.classList.add('animate-on-scroll');
        listing.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Add animation classes to stats
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((stat, index) => {
        stat.classList.add('animate-on-scroll');
        stat.style.animationDelay = `${index * 0.1}s`;
    });
});