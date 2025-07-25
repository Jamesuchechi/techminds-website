document.addEventListener('DOMContentLoaded', () => {
    const hamburgerButton = document.getElementById('hamburger-button');
    const navMenu = document.querySelector('.nav-menu');
    const mobileMenu = document.querySelector('.mobile-menu');
    const overlay = document.querySelector('.overlay');

    // Toggle mobile menu and overlay
    hamburgerButton.addEventListener('click', () => {
        mobileMenu.classList.toggle('active');
        hamburgerButton.classList.toggle('active');
        overlay.classList.toggle('active');
        // Optionally toggle nav-menu for consistency, but not necessary if mobile-menu is used
        navMenu.classList.toggle('active');
    });

    // Close mobile menu when clicking a nav link
    document.querySelectorAll('.mobile-menu a').forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.remove('active');
            hamburgerButton.classList.remove('active');
            overlay.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });

    // Close menu and dropdowns when clicking outside
    document.addEventListener('click', (e) => {
        if (!mobileMenu.contains(e.target) && !hamburgerButton.contains(e.target) && !navMenu.contains(e.target)) {
            mobileMenu.classList.remove('active');
            hamburgerButton.classList.remove('active');
            overlay.classList.remove('active');
            navMenu.classList.remove('active');
        }

        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown').forEach(d => d.classList.remove('active'));
        }
    });

    // Dropdown toggle for mobile (click only under 768px)
    document.querySelectorAll('.dropdown-toggle').forEach(dropdown => {
        dropdown.addEventListener('click', e => {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                const parent = dropdown.closest('.dropdown');
                parent.classList.toggle('active');
            }
        });
    });

    // Desktop dropdowns (hover only)
    if (window.innerWidth > 768) {
        document.querySelectorAll('.dropdown').forEach(dropdown => {
            dropdown.addEventListener('mouseenter', () => {
                dropdown.classList.add('active');
            });
            dropdown.addEventListener('mouseleave', () => {
                dropdown.classList.remove('active');
            });
        });
    }

    // Define closeMobileMenu function for HTML onclick attributes
    window.closeMobileMenu = function () {
        mobileMenu.classList.remove('active');
        hamburgerButton.classList.remove('active');
        overlay.classList.remove('active');
        navMenu.classList.remove('active');
    };
});

/* Hero Video Control */
document.addEventListener('DOMContentLoaded', function() {
    const video = document.querySelector('.hero-video');
    if (video) {
        if (window.innerWidth <= 768) {
            video.pause();
        } else {
            video.play().catch(err => console.error('Video playback error:', err));
        }

        const toggleButton = document.createElement('button');
        toggleButton.innerHTML = '⏯';
        toggleButton.style.cssText = `
            position: absolute;
            bottom: 20px;
            right: 20px;
            background: #1e3a8a;
            color: white;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            font-size: 1.2rem;
            cursor: pointer;
            z-index: 2;
            transition: transform 0.3s ease, background 0.3s ease;
        `;
        toggleButton.addEventListener('mouseover', () => {
            toggleButton.style.background = '#2b4db3';
            toggleButton.style.transform = 'scale(1.1)';
        });
        toggleButton.addEventListener('mouseout', () => {
            toggleButton.style.background = '#1e3a8a';
            toggleButton.style.transform = 'scale(1)';
        });
        toggleButton.addEventListener('click', () => {
            if (video.paused) {
                video.play().catch(err => console.error('Video playback error:', err));
                toggleButton.innerHTML = '⏸';
            } else {
                video.pause();
                toggleButton.innerHTML = '▶';
            }
        });
        document.querySelector('.hero-section').appendChild(toggleButton);
    }

    const heroElements = document.querySelectorAll('.hero-title, .hero-subtitle, .hero-cta');
    heroElements.forEach((el, index) => {
        el.style.opacity = '0';
        setTimeout(() => {
            el.style.opacity = '1';
            el.classList.add('fade-in');
        }, index * 200);
    });
});

/* Scroll-triggered Animations */
document.addEventListener('DOMContentLoaded', () => {
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('in-view');
                observer.unobserve(entry.target); // Animate only once
            }
        });
    }, {
        threshold: 0.1 // Trigger when 10% visible
    });

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
});

/* Enhanced Form Submission Handler */
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const action = this.action || window.location.href;
        const method = (this.method || 'POST').toUpperCase();

        const submitBtn = this.querySelector('button[type="submit"], input[type="submit"]');
        const originalBtnText = submitBtn ? submitBtn.innerHTML : '';
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner"></span> Submitting...';
        }

        try {
            const response = await fetch(action, {
                method: method,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json, text/html, /'
                },
                body: formData
            });

            const formParent = this.closest('.contact-form') || this.parentElement;
            let prevResp = formParent.querySelector('.form-response');
            if (prevResp) prevResp.remove();

            let respDiv = document.createElement('div');
            respDiv.className = 'form-response';
            respDiv.style.cssText = `
                margin: 1rem 0;
                padding: 1rem;
                border-radius: 8px;
                font-weight: bold;
                font-size: 1rem;
                animation: fadeIn 0.3s ease-in;
            `;

            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                const data = await response.json();
                if (response.ok && (data.success !== false)) {
                    respDiv.style.background = '#d1fae5';
                    respDiv.style.color = '#065f46';
                    respDiv.style.border = '1px solid #10b981';
                    respDiv.innerHTML = '✅ ' + (data.message || 'Form submitted successfully!');
                    this.reset();
                } else {
                    respDiv.style.background = '#fee2e2';
                    respDiv.style.color = '#b91c1c';
                    respDiv.style.border = '1px solid #ef4444';
                    respDiv.innerHTML = '❌ ' + (data.message || 'Submission failed. Please try again.');
                }
            } else {
                const html = await response.text();
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = html;
                const successEl = tempDiv.querySelector('.success, .alert-success, .message-success, [class*="success"]');
                const errorEl = tempDiv.querySelector('.error, .alert-error, .message-error, [class*="error"]');
                if (successEl) {
                    respDiv.style.background = '#d1fae5';
                    respDiv.style.color = '#065f46';
                    respDiv.style.border = '1px solid #10b981';
                    respDiv.innerHTML = '✅ ' + (successEl.textContent.trim() || 'Form submitted successfully!');
                    this.reset();
                } else if (errorEl) {
                    respDiv.style.background = '#fee2e2';
                    respDiv.style.color = '#b91c1c';
                    respDiv.style.border = '1px solid #ef4444';
                    respDiv.innerHTML = '❌ ' + (errorEl.textContent.trim() || 'Submission failed.');
                } else {
                    respDiv.style.background = '#d1fae5';
                    respDiv.style.color = '#065f46';
                    respDiv.style.border = '1px solid #10b981';
                    respDiv.innerHTML = '✅ Form submitted successfully!';
                    this.reset();
                }
            }

            formParent.appendChild(respDiv);
            respDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } catch (err) {
            console.error('Form submission error:', err);
            const formParent = this.closest('.contact-form') || this.parentElement;
            let prevResp = formParent.querySelector('.form-response');
            if (prevResp) prevResp.remove();

            let respDiv = document.createElement('div');
            respDiv.className = 'form-response';
            respDiv.style.cssText = `
                margin: 1rem 0;
                padding: 1rem;
                border-radius: 8px;
                font-weight: bold;
                font-size: 1rem;
                background: #fee2e2;
                color: #b91c1c;
                border: 1px solid #ef4444;
                animation: fadeIn 0.3s ease-in;
            `;
            respDiv.innerHTML = '❌ Network error. Please check your connection and try again.';
            formParent.appendChild(respDiv);
            respDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } finally {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            }
        }
    });
});

/* Form Response Animation Styles */
if (!document.querySelector('#form-response-styles')) {
    const style = document.createElement('style');
    style.id = 'form-response-styles';
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .spinner {
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 2px solid #ffffff;
            border-top: 2px solid #facc15;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 8px;
            vertical-align: middle;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
}

/* Toast Notification */
function showToast(message, type = 'error') {
    let toast = document.createElement('div');
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        background: ${type === 'error' ? '#dc2626' : '#16a34a'};
        color: white;
        padding: 1rem 2rem;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        z-index: 9999;
        font-weight: bold;
        font-size: 1rem;
    `;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.transition = 'opacity 0.5s';
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 500);
    }, 3000);
}

/* Navbar Scroll Effect */
let scrollTimeout;
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        clearTimeout(scrollTimeout);
        navbar.classList.toggle('scrolled', window.scrollY > 0);
        scrollTimeout = setTimeout(() => {
            navbar.classList.add('scrolled');
        }, 100);
    }
});

/* Scroll to Top Button Functionality */
const scrollToTopBtn = document.getElementById('scrollToTop');
window.addEventListener('scroll', () => {
    const footer = document.getElementById('footer');
    if (!footer || !scrollToTopBtn) return;

    const footerRect = footer.getBoundingClientRect();
    const windowHeight = window.innerHeight;

    if (footerRect.top <= windowHeight && footerRect.bottom >= 0) {
        scrollToTopBtn.style.display = 'block';
    } else {
        scrollToTopBtn.style.display = 'none';
    }
});

if (scrollToTopBtn) {
    scrollToTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// /* Dropdown Toggle Functionality */
// function toggleDropdown(event) {
//     event.preventDefault();
//     const dropdown = event.currentTarget.parentElement;

//     // Close other open dropdowns
//     document.querySelectorAll('.dropdown').forEach(d => {
//         if (d !== dropdown) d.classList.remove('active');
//     });

//     // Toggle this dropdown
//     dropdown.classList.toggle('active');
// }

// // Attach dropdown click handler for desktop/mobile
// document.querySelectorAll('.nav-link.dropdown-toggle').forEach(item => {
//     item.addEventListener('click', toggleDropdown);
// });

// // Close dropdowns when clicking outside
// document.addEventListener('click', function(e) {
//     if (!e.target.closest('.dropdown')) {
//         document.querySelectorAll('.dropdown').forEach(d => d.classList.remove('active'));
//     }
// });