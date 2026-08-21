// ============== CLEAN & SIMPLE EXPERTISE PAGE JAVASCRIPT ===============

document.addEventListener('DOMContentLoaded', function() {
    console.log('Clean Expertise page loaded');
    
    // Simple hover effects for service cards
    const serviceCards = document.querySelectorAll('.services-section .col-lg-4');
    
    serviceCards.forEach(card => {
        const cardElement = card.querySelector('div');
        
        card.addEventListener('mouseenter', function() {
            cardElement.style.transform = 'translateY(-5px)';
            cardElement.style.boxShadow = '0 8px 30px rgba(0,0,0,0.12)';
        });
        
        card.addEventListener('mouseleave', function() {
            cardElement.style.transform = 'translateY(0)';
            cardElement.style.boxShadow = '0 4px 20px rgba(0,0,0,0.08)';
        });
    });
    
    // Simple smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    console.log('Clean expertise page initialized');
}); 