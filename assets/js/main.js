/**
 * Main JavaScript file for Juan Felipe Imbet's academic website
 */

document.addEventListener('DOMContentLoaded', function() {
    // Highlight the current page in the navigation
    highlightCurrentPage();

    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
      // Toggle paper abstracts
    document.querySelectorAll('.toggle-abstract').forEach(button => {
        button.addEventListener('click', function() {
            const abstractDiv = this.previousElementSibling;
            abstractDiv.classList.toggle('show');
            
            // Change button text based on visibility
            if (abstractDiv.classList.contains('show')) {
                this.textContent = 'Hide Abstract';
            } else {
                this.textContent = 'Show Abstract';
            }
        });
    });
    
    // Toggle media mentions
    document.querySelectorAll('.toggle-mentions').forEach(button => {
        button.addEventListener('click', function() {
            const mentionsDiv = this.previousElementSibling;
            mentionsDiv.classList.toggle('show');
            
            // Change button text based on visibility
            if (mentionsDiv.classList.contains('show')) {
                this.textContent = 'Hide Media Mentions';
            } else {
                this.textContent = 'Show Media Mentions';
            }
        });
    });
    
    // Toggle regulator mentions
    document.querySelectorAll('.toggle-regulator-mentions').forEach(button => {
        button.addEventListener('click', function() {
            const mentionsDiv = this.previousElementSibling;
            mentionsDiv.classList.toggle('show');
            
            // Change button text based on visibility
            if (mentionsDiv.classList.contains('show')) {
                this.textContent = 'Hide Regulator Mentions';
            } else {
                this.textContent = 'Show Regulator Mentions';
            }
        });
    });
});

/**
 * Highlight the current page in the navigation
 */
function highlightCurrentPage() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        
        // Remove active class from all links
        link.classList.remove('active');
        
        // Check if this is the current page
        if (href === currentPath || 
            (href === '#about' && (currentPath === '/' || currentPath === '/index.html')) ||
            (currentPath.includes(href) && href !== '#about')) {
            link.classList.add('active');
        }
    });
}
