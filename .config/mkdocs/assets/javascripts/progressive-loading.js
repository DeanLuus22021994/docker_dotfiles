/**
 * Progressive Image Loading System
 * Implements lazy loading with blur-to-sharp transitions
 * and WebP format detection for bleeding-edge performance
 */

class ProgressiveImageLoader {
    constructor(options = {}) {
        this.options = {
            threshold: 0.1,
            rootMargin: '50px',
            blurRadius: 20,
            transitionDuration: 300,
            enableWebP: true,
            quality: {
                placeholder: 10,
                full: 85
            },
            ...options
        };
        
        this.observer = null;
        this.webpSupported = null;
        this.images = [];
        
        this.init();
    }
    
    async init() {
        // Detect WebP support
        this.webpSupported = await this.checkWebPSupport();
        
        // Initialize Intersection Observer
        this.setupObserver();
        
        // Process existing images
        this.processImages();
        
        // Monitor for new images
        this.setupMutationObserver();
    }
    
    async checkWebPSupport() {
        return new Promise((resolve) => {
            const webp = new Image();
            webp.onload = webp.onerror = () => {
                resolve(webp.height === 2);
            };
            webp.src = 'data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA';
        });
    }
    
    setupObserver() {
        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.loadImage(entry.target);
                }
            });
        }, {
            threshold: this.options.threshold,
            rootMargin: this.options.rootMargin
        });
    }
    
    setupMutationObserver() {
        const mutationObserver = new MutationObserver((mutations) => {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1) { // Element node
                        const images = node.tagName === 'IMG' ? [node] : 
                                      node.querySelectorAll ? node.querySelectorAll('img[data-src]') : [];
                        images.forEach(img => this.processImage(img));
                    }
                });
            });
        });
        
        mutationObserver.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
    
    processImages() {
        const images = document.querySelectorAll('img[data-src]');
        images.forEach(img => this.processImage(img));
    }
    
    processImage(img) {
        if (img.dataset.processed) return;
        
        img.dataset.processed = 'true';
        this.images.push(img);
        
        // Create placeholder
        this.createPlaceholder(img);
        
        // Start observing
        this.observer.observe(img);
    }
    
    createPlaceholder(img) {
        const placeholder = this.generatePlaceholder(img);
        
        img.style.cssText = 
            background-image: url('data:image/svg+xml;base64,');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            filter: blur(px);
            transition: filter ms ease-out;
        ;
    }
    
    generatePlaceholder(img) {
        const width = img.getAttribute('width') || 800;
        const height = img.getAttribute('height') || 600;
        
        // Create a simple gradient placeholder
        return 
            <svg width="" height="" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#f0f0f0;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#e0e0e0;stop-opacity:1" />
                    </linearGradient>
                </defs>
                <rect width="100%" height="100%" fill="url(#grad)"/>
                <text x="50%" y="50%" text-anchor="middle" dy=".3em" 
                      fill="#999" font-family="Arial" font-size="14">Loading...</text>
            </svg>
        ;
    }
    
    async loadImage(img) {
        const originalSrc = img.dataset.src;
        if (!originalSrc) return;
        
        try {
            // Determine optimal format
            const optimizedSrc = this.getOptimizedSrc(originalSrc);
            
            // Preload the image
            const imagePromise = this.preloadImage(optimizedSrc);
            
            // Show loading state
            this.showLoadingState(img);
            
            // Wait for image to load
            await imagePromise;
            
            // Apply the loaded image
            this.applyLoadedImage(img, optimizedSrc);
            
            // Stop observing
            this.observer.unobserve(img);
            
        } catch (error) {
            console.warn('Failed to load image:', originalSrc, error);
            this.handleImageError(img, originalSrc);
        }
    }
    
    getOptimizedSrc(src) {
        if (!this.webpSupported || !this.options.enableWebP) {
            return src;
        }
        
        // Check if we can convert to WebP
        const extension = src.split('.').pop().toLowerCase();
        if (['jpg', 'jpeg', 'png'].includes(extension)) {
            return src.replace(/\.(jpg|jpeg|png)$/i, '.webp');
        }
        
        return src;
    }
    
    preloadImage(src) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => resolve(img);
            img.onerror = reject;
            img.src = src;
        });
    }
    
    showLoadingState(img) {
        img.classList.add('progressive-loading');
        
        // Add loading animation
        const loadingOverlay = document.createElement('div');
        loadingOverlay.className = 'progressive-loading-overlay';
        loadingOverlay.innerHTML = 
            <div class="progressive-spinner">
                <div class="spinner-ring"></div>
            </div>
        ;
        
        img.parentNode.insertBefore(loadingOverlay, img.nextSibling);
    }
    
    applyLoadedImage(img, src) {
        img.src = src;
        img.classList.remove('progressive-loading');
        img.classList.add('progressive-loaded');
        
        // Remove blur and show sharp image
        setTimeout(() => {
            img.style.filter = 'none';
        }, 50);
        
        // Remove loading overlay
        const overlay = img.parentNode.querySelector('.progressive-loading-overlay');
        if (overlay) {
            overlay.remove();
        }
        
        // Trigger loaded event
        img.dispatchEvent(new CustomEvent('progressiveLoaded', {
            detail: { src, webpUsed: this.webpSupported }
        }));
    }
    
    handleImageError(img, originalSrc) {
        img.classList.add('progressive-error');
        
        // Try fallback to original format
        if (originalSrc !== img.dataset.src) {
            this.preloadImage(img.dataset.src)
                .then(() => this.applyLoadedImage(img, img.dataset.src))
                .catch(() => {
                    img.style.filter = 'none';
                    img.alt = 'Failed to load image';
                });
        }
    }
    
    // Performance monitoring
    getMetrics() {
        const loadedImages = this.images.filter(img => img.classList.contains('progressive-loaded'));
        const failedImages = this.images.filter(img => img.classList.contains('progressive-error'));
        
        return {
            total: this.images.length,
            loaded: loadedImages.length,
            failed: failedImages.length,
            webpSupported: this.webpSupported,
            loadingRate: this.images.length > 0 ? loadedImages.length / this.images.length : 0
        };
    }
}

// CSS for progressive loading effects
const progressiveCSS = 
    .progressive-loading {
        position: relative;
    }
    
    .progressive-loading-overlay {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 10;
    }
    
    .progressive-spinner {
        width: 40px;
        height: 40px;
    }
    
    .spinner-ring {
        width: 100%;
        height: 100%;
        border: 3px solid rgba(0, 123, 255, 0.1);
        border-top: 3px solid #007bff;
        border-radius: 50%;
        animation: progressive-spin 1s linear infinite;
    }
    
    @keyframes progressive-spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .progressive-loaded {
        animation: progressive-fade-in 300ms ease-out;
    }
    
    @keyframes progressive-fade-in {
        from { opacity: 0.8; }
        to { opacity: 1; }
    }
    
    .progressive-error {
        background-color: #f8f9fa;
        border: 2px dashed #dee2e6;
        min-height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #6c757d;
    }
    
    .progressive-error::before {
        content: "⚠️ Image failed to load";
        font-size: 14px;
    }
;

// Inject CSS
if (!document.querySelector('#progressive-loading-styles')) {
    const style = document.createElement('style');
    style.id = 'progressive-loading-styles';
    style.textContent = progressiveCSS;
    document.head.appendChild(style);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.progressiveLoader = new ProgressiveImageLoader({
            enableWebP: true,
            quality: { placeholder: 20, full: 90 }
        });
    });
} else {
    window.progressiveLoader = new ProgressiveImageLoader({
        enableWebP: true,
        quality: { placeholder: 20, full: 90 }
    });
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ProgressiveImageLoader;
}
