// ============================================================================
// Custom JavaScript - MkDocs Material Enhanced Functionality
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {

  // ============================================================================
  // Keyboard Shortcuts
  // ============================================================================
  document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K: Focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      const searchInput = document.querySelector('.md-search__input');
      if (searchInput) {
        searchInput.focus();
        searchInput.select();
      }
    }

    // Escape: Close search
    if (e.key === 'Escape') {
      const searchInput = document.querySelector('.md-search__input');
      if (searchInput && document.activeElement === searchInput) {
        searchInput.blur();
      }
    }
  });

  // ============================================================================
  // Smooth Scroll for Anchor Links
  // ============================================================================
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

  // ============================================================================
  // External Link Handling
  // ============================================================================
  document.querySelectorAll('a[href^="http"]').forEach(link => {
    if (!link.hostname.includes(window.location.hostname)) {
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');

      // Add external link icon
      if (!link.querySelector('.external-icon')) {
        const icon = document.createElement('span');
        icon.className = 'external-icon';
        icon.innerHTML = ' ↗';
        link.appendChild(icon);
      }
    }
  });

  // ============================================================================
  // Code Block Enhancements
  // ============================================================================
  document.querySelectorAll('pre code').forEach(block => {
    const language = block.className.match(/language-(\w+)/);
    if (language) {
      const label = document.createElement('div');
      label.className = 'code-language-label';
      label.textContent = language[1].toUpperCase();
      block.parentElement.insertBefore(label, block);
    }
  });

  // ============================================================================
  // Progress Indicator
  // ============================================================================
  const progressBar = document.createElement('div');
  progressBar.id = 'reading-progress';
  progressBar.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 0%;
    height: 3px;
    background: linear-gradient(90deg, var(--md-primary-fg-color), var(--md-accent-fg-color));
    z-index: 1000;
    transition: width 0.1s ease;
  `;
  document.body.appendChild(progressBar);

  window.addEventListener('scroll', function() {
    const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (window.scrollY / windowHeight) * 100;
    progressBar.style.width = scrolled + '%';
  });

  // ============================================================================
  // Table of Contents Highlight
  // ============================================================================
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      const id = entry.target.getAttribute('id');
      const tocLink = document.querySelector(`.md-nav__link[href="#${id}"]`);

      if (entry.intersectionRatio > 0) {
        document.querySelectorAll('.md-nav__link').forEach(link => {
          link.classList.remove('md-nav__link--active');
        });
        if (tocLink) {
          tocLink.classList.add('md-nav__link--active');
        }
      }
    });
  }, {
    rootMargin: '-20% 0% -35% 0%'
  });

  document.querySelectorAll('h2[id], h3[id]').forEach(heading => {
    observer.observe(heading);
  });

  console.log('🚀 MkDocs Material Enhanced - Loaded');
});
