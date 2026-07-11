document.addEventListener('DOMContentLoaded', () => {
    // Reveal animations on scroll
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Apply visibility to sections
    document.querySelectorAll('section').forEach(section => {
        section.style.opacity = "0";
        section.style.transition = "opacity 1s ease, transform 1s ease";
        section.style.transform = "translateY(20px)";
        observer.observe(section);
    });

    // Custom visible class
    const style = document.createElement('style');
    style.textContent = `
        section.visible {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);

    document.body.setAttribute('oncontextmenu', 'return false');
    document.body.setAttribute('ondragstart', 'return false');

    let privacyTimer;
    const activatePrivacyPause = (duration = 2500) => {
        document.body.classList.add('privacy-paused');
        window.clearTimeout(privacyTimer);
        privacyTimer = window.setTimeout(() => {
            if (document.hasFocus() && document.visibilityState === 'visible') {
                document.body.classList.remove('privacy-paused');
            }
        }, duration);
    };

    const protectedImages = document.querySelectorAll('img');
    protectedImages.forEach(image => {
        image.setAttribute('draggable', 'false');
        image.setAttribute('oncontextmenu', 'return false');
        image.setAttribute('ondragstart', 'return false');
        image.setAttribute('loading', image.getAttribute('loading') || 'lazy');
        image.classList.add('protected-media');
    });

    document.addEventListener('contextmenu', event => {
        event.preventDefault();
        event.stopPropagation();
        return false;
    }, true);

    document.addEventListener('dragstart', event => {
        event.preventDefault();
        event.stopPropagation();
        return false;
    }, true);

    document.addEventListener('drop', event => {
        event.preventDefault();
        event.stopPropagation();
        return false;
    }, true);

    document.addEventListener('selectstart', event => {
        if (event.target.closest('img, .protected-media')) {
            event.preventDefault();
        }
    }, true);

    document.addEventListener('mousedown', event => {
        if (event.target.closest('img, .protected-media') && event.button !== 0) {
            event.preventDefault();
            event.stopPropagation();
            return false;
        }
    }, true);

    document.addEventListener('keydown', event => {
        const key = event.key.toLowerCase();
        const blockedShortcut = (event.ctrlKey || event.metaKey) && ['s', 'p', 'u', 'c', 'x', 'a'].includes(key);
        const possibleSnipShortcut = event.shiftKey && key === 's';
        if (blockedShortcut || possibleSnipShortcut || key === 'printscreen') {
            event.preventDefault();
            event.stopPropagation();
            activatePrivacyPause(3200);
            return false;
        }
    }, true);

    document.addEventListener('keyup', event => {
        if (event.key.toLowerCase() === 'printscreen') {
            activatePrivacyPause(3200);
        }
    }, true);

    window.addEventListener('blur', () => {
        activatePrivacyPause(4000);
    });

    window.addEventListener('focus', () => {
        window.setTimeout(() => {
            document.body.classList.remove('privacy-paused');
        }, 500);
    });

    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState !== 'visible') {
            activatePrivacyPause(4000);
        }
    });

    window.addEventListener('beforeprint', () => {
        activatePrivacyPause(4000);
    });

    document.addEventListener('mouseleave', () => {
        activatePrivacyPause(1600);
    });

    const lightbox = document.createElement('div');
    lightbox.className = 'image-lightbox';
    lightbox.setAttribute('aria-hidden', 'true');
    lightbox.innerHTML = `
        <div class="image-lightbox__toolbar">
            <button type="button" data-zoom="out" aria-label="Zoom out">-</button>
            <button type="button" data-zoom="reset" aria-label="Reset zoom">100%</button>
            <button type="button" data-zoom="in" aria-label="Zoom in">+</button>
            <button type="button" data-close aria-label="Close image viewer">x</button>
        </div>
        <div class="image-lightbox__stage">
            <img class="image-lightbox__image protected-media" alt="" draggable="false">
        </div>
    `;
    document.body.appendChild(lightbox);

    const lightboxImage = lightbox.querySelector('.image-lightbox__image');
    let zoomLevel = 1;

    const setZoom = value => {
        zoomLevel = Math.min(Math.max(value, 1), 3);
        lightboxImage.style.transform = `scale(${zoomLevel})`;
        lightbox.querySelector('[data-zoom="reset"]').textContent = `${Math.round(zoomLevel * 100)}%`;
    };

    const closeLightbox = () => {
        lightbox.classList.remove('is-open');
        lightbox.setAttribute('aria-hidden', 'true');
        lightboxImage.removeAttribute('src');
        setZoom(1);
    };

    document.querySelectorAll('.zoomable-image').forEach(image => {
        image.addEventListener('click', event => {
            event.preventDefault();
            event.stopPropagation();
            lightboxImage.src = image.currentSrc || image.src;
            lightboxImage.alt = image.alt || '';
            lightbox.classList.add('is-open');
            lightbox.setAttribute('aria-hidden', 'false');
            setZoom(1);
        });
    });

    lightbox.addEventListener('click', event => {
        if (event.target === lightbox || event.target.dataset.close !== undefined) {
            closeLightbox();
        }
        if (event.target.dataset.zoom === 'in') setZoom(zoomLevel + 0.25);
        if (event.target.dataset.zoom === 'out') setZoom(zoomLevel - 0.25);
        if (event.target.dataset.zoom === 'reset') setZoom(1);
    });

    lightbox.addEventListener('wheel', event => {
        event.preventDefault();
        setZoom(zoomLevel + (event.deltaY < 0 ? 0.15 : -0.15));
    }, { passive: false });

    document.addEventListener('keydown', event => {
        if (event.key === 'Escape' && lightbox.classList.contains('is-open')) {
            closeLightbox();
        }
    });

    const getCookie = (name) => {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) {
            return parts.pop().split(';').shift();
        }
        return '';
    };

    // Like buttons on highlights page
    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', async () => {
            const likeUrl = button.dataset.likeUrl;
            const countEl = button.querySelector('.like-count');
            if (!likeUrl || !countEl || button.disabled) return;

            button.disabled = true;
            try {
                const response = await fetch(likeUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                if (!response.ok) {
                    button.disabled = false;
                    return;
                }
                const data = await response.json();
                countEl.textContent = data.likes;
                button.classList.add('liked');
            } catch (error) {
                button.disabled = false;
            }
        });
    });
});
