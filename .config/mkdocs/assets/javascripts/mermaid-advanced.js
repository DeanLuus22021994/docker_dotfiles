/**
 * Mermaid v10+ Configuration with Interactive Bleeding-Edge Features
 * ==================================================================
 *
 * Features:
 * - Interactive click/hover events
 * - Advanced theming with Material Design integration
 * - Security hardening with trusted domains
 * - Performance optimization
 * - Custom styling for Docker platform diagrams
 */

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    // Check if Mermaid is available
    if (typeof mermaid === 'undefined') {
        console.warn('Mermaid not loaded, attempting dynamic import...');
        import('https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs')
            .then(module => {
                initializeMermaid(module.default);
            })
            .catch(err => console.error('Failed to load Mermaid:', err));
    } else {
        initializeMermaid(mermaid);
    }
});

function initializeMermaid(mermaidModule) {
    // Detect theme from Material Design system
    const getTheme = () => {
        const bodyClass = document.body.getAttribute('data-md-color-scheme');
        return bodyClass === 'slate' ? 'dark' : 'base';
    };

    // Advanced Mermaid Configuration
    const config = {
        // Core settings
        startOnLoad: true,
        theme: getTheme(),
        themeCSS: generateCustomTheme(),

        // Security settings
        secure: ['localhost', '127.0.0.1', 'github.com', 'githubusercontent.com'],
        securityLevel: 'strict',

        // Performance settings
        maxTextSize: 90000,
        maxEdges: 500,

        // Flowchart customization
        flowchart: {
            useMaxWidth: true,
            htmlLabels: true,
            curve: 'basis',
            padding: 20,
            nodeSpacing: 50,
            rankSpacing: 50,
            diagramPadding: 8,
            wrappingWidth: 200
        },

        // Sequence diagram settings
        sequence: {
            useMaxWidth: true,
            diagramMarginX: 50,
            diagramMarginY: 10,
            actorMargin: 50,
            width: 150,
            height: 65,
            boxMargin: 10,
            boxTextMargin: 5,
            noteMargin: 10,
            messageMargin: 35,
            mirrorActors: true,
            bottomMarginAdj: 1,
            rightAngles: false,
            showSequenceNumbers: false,
            actorFontSize: 14,
            actorFontFamily: 'Inter, sans-serif',
            noteFontSize: 12,
            noteFontFamily: 'Inter, sans-serif',
            messageFontSize: 12,
            messageFontFamily: 'Inter, sans-serif'
        },

        // Gantt chart settings
        gantt: {
            useMaxWidth: true,
            leftPadding: 75,
            gridLineStartPadding: 35,
            fontSize: 11,
            fontFamily: 'Inter, sans-serif',
            sectionFontSize: 24,
            numberSectionStyles: 4
        },

        // Class diagram settings
        class: {
            useMaxWidth: true,
            htmlLabels: true
        },

        // State diagram settings
        state: {
            useMaxWidth: true
        },

        // Git graph settings
        gitGraph: {
            useMaxWidth: true,
            theme: getTheme(),
            themeVariables: {
                primaryColor: '#00bcd4',
                primaryTextColor: '#ffffff',
                primaryBorderColor: '#00838f',
                lineColor: '#757575',
                secondaryColor: '#ff5722',
                tertiaryColor: '#fff'
            }
        },

        // Journey diagram settings
        journey: {
            useMaxWidth: true,
            diagramMarginX: 50,
            diagramMarginY: 50,
            leftMargin: 150,
            width: 150,
            height: 50,
            boxMargin: 10,
            boxTextMargin: 5,
            noteMargin: 10,
            messageMargin: 35,
            messageAlign: 'center',
            bottomMarginAdj: 1,
            rightAngles: false,
            taskFontSize: 14,
            taskFontFamily: 'Inter, sans-serif',
            taskMargin: 50,
            activationWidth: 10,
            textPlacement: 'fo',
            actorColours: ['#8FBC8F', '#FFB347', '#87CEEB', '#DDA0DD']
        },

        // Timeline settings
        timeline: {
            useMaxWidth: true,
            diagramMarginX: 50,
            diagramMarginY: 25,
            leftMargin: 150,
            width: 150,
            height: 50
        }
    };

    // Initialize Mermaid with advanced config
    mermaidModule.initialize(config);

    // Add interactive features
    addInteractiveFeatures(mermaidModule);

    // Handle theme changes
    observeThemeChanges(mermaidModule);

    // Add click handlers for Docker-specific diagrams
    addDockerDiagramHandlers();

    console.log('✅ Mermaid v10+ initialized with bleeding-edge features');
}

function generateCustomTheme() {
    return `
        /* Docker Platform Custom Styling */
        .node[id*="docker"] .label {
            fill: #2496ED !important;
            color: white !important;
        }

        .node[id*="postgres"] .label {
            fill: #336791 !important;
            color: white !important;
        }

        .node[id*="redis"] .label {
            fill: #DC382D !important;
            color: white !important;
        }

        .node[id*="nginx"] .label {
            fill: #269539 !important;
            color: white !important;
        }

        .node[id*="grafana"] .label {
            fill: #F46800 !important;
            color: white !important;
        }

        /* Enhanced hover effects */
        .node:hover {
            filter: brightness(1.1);
            transform: scale(1.02);
            transition: all 0.2s ease;
        }

        /* Interactive elements */
        .clickable {
            cursor: pointer;
        }

        /* Animations */
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }

        .animated-node {
            animation: pulse 2s infinite;
        }
    `;
}

function addInteractiveFeatures(mermaidModule) {
    // Find all Mermaid diagrams
    const diagrams = document.querySelectorAll('.mermaid');

    diagrams.forEach((diagram, index) => {
        // Add click event listeners
        diagram.addEventListener('click', function(event) {
            const target = event.target;

            // Handle node clicks
            if (target.closest('.node')) {
                const nodeId = target.closest('.node').id;
                handleNodeClick(nodeId, event);
            }

            // Handle edge clicks
            if (target.closest('.edgePath')) {
                const edgeId = target.closest('.edgePath').id;
                handleEdgeClick(edgeId, event);
            }
        });

        // Add hover effects
        diagram.addEventListener('mouseover', function(event) {
            const target = event.target;

            if (target.closest('.node')) {
                const node = target.closest('.node');
                node.classList.add('hover-active');
                showNodeTooltip(node, event);
            }
        });

        diagram.addEventListener('mouseout', function(event) {
            const target = event.target;

            if (target.closest('.node')) {
                const node = target.closest('.node');
                node.classList.remove('hover-active');
                hideNodeTooltip();
            }
        });
    });
}

function handleNodeClick(nodeId, event) {
    console.log('Node clicked:', nodeId);

    // Docker service specific actions
    if (nodeId.includes('docker')) {
        showDockerServiceInfo(nodeId);
    } else if (nodeId.includes('database')) {
        showDatabaseMetrics(nodeId);
    } else if (nodeId.includes('api')) {
        showAPIEndpoints(nodeId);
    }

    // Generic action
    highlightConnectedNodes(nodeId);
}

function handleEdgeClick(edgeId, event) {
    console.log('Edge clicked:', edgeId);
    showConnectionDetails(edgeId);
}

function showNodeTooltip(node, event) {
    const tooltip = document.createElement('div');
    tooltip.className = 'mermaid-tooltip';
    tooltip.style.cssText = `
        position: absolute;
        background: var(--md-primary-fg-color);
        color: var(--md-primary-bg-color);
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 12px;
        font-family: Inter, sans-serif;
        pointer-events: none;
        z-index: 1000;
        opacity: 0;
        transition: opacity 0.2s ease;
        max-width: 200px;
    `;

    // Get node information
    const nodeText = node.querySelector('.label')?.textContent || 'Unknown';
    const nodeType = getNodeType(node.id);

    tooltip.innerHTML = `
        <strong>${nodeText}</strong><br>
        <small>Type: ${nodeType}</small><br>
        <small>Click for details</small>
    `;

    document.body.appendChild(tooltip);

    // Position tooltip
    const rect = event.target.getBoundingClientRect();
    tooltip.style.left = rect.left + 'px';
    tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';

    // Fade in
    setTimeout(() => tooltip.style.opacity = '1', 10);

    // Store reference for cleanup
    node._tooltip = tooltip;
}

function hideNodeTooltip() {
    const tooltips = document.querySelectorAll('.mermaid-tooltip');
    tooltips.forEach(tooltip => {
        tooltip.style.opacity = '0';
        setTimeout(() => tooltip.remove(), 200);
    });
}

function getNodeType(nodeId) {
    if (nodeId.includes('docker')) return 'Container Service';
    if (nodeId.includes('database')) return 'Database';
    if (nodeId.includes('api')) return 'API Endpoint';
    if (nodeId.includes('cache')) return 'Cache Layer';
    if (nodeId.includes('queue')) return 'Message Queue';
    return 'Service Component';
}

function showDockerServiceInfo(nodeId) {
    const modal = createModal('Docker Service Information', `
        <div class="service-info">
            <h3>Service: ${nodeId}</h3>
            <ul>
                <li><strong>Status:</strong> <span class="status-running">Running</span></li>
                <li><strong>Port:</strong> 8080:80</li>
                <li><strong>Memory:</strong> 256MB</li>
                <li><strong>CPU:</strong> 0.5 cores</li>
                <li><strong>Health:</strong> <span class="health-good">Healthy</span></li>
            </ul>
            <button onclick="viewServiceLogs('${nodeId}')">View Logs</button>
            <button onclick="restartService('${nodeId}')">Restart</button>
        </div>
    `);
}

function showDatabaseMetrics(nodeId) {
    const modal = createModal('Database Metrics', `
        <div class="db-metrics">
            <h3>Database: ${nodeId}</h3>
            <div class="metrics-grid">
                <div class="metric">
                    <strong>Connections:</strong> 45/100
                </div>
                <div class="metric">
                    <strong>Query Time:</strong> 12ms avg
                </div>
                <div class="metric">
                    <strong>Storage:</strong> 2.1GB / 10GB
                </div>
                <div class="metric">
                    <strong>Uptime:</strong> 7d 14h 32m
                </div>
            </div>
            <button onclick="openDatabaseConsole('${nodeId}')">Open Console</button>
        </div>
    `);
}

function showAPIEndpoints(nodeId) {
    const modal = createModal('API Endpoints', `
        <div class="api-info">
            <h3>API: ${nodeId}</h3>
            <div class="endpoints">
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="url">/api/health</span>
                    <span class="status">200</span>
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="url">/api/metrics</span>
                    <span class="status">200</span>
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span>
                    <span class="url">/api/data</span>
                    <span class="status">201</span>
                </div>
            </div>
            <button onclick="openAPITester('${nodeId}')">Test API</button>
        </div>
    `);
}

function createModal(title, content) {
    const modal = document.createElement('div');
    modal.className = 'mermaid-modal';
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
    `;

    modal.innerHTML = `
        <div class="modal-content" style="
            background: var(--md-default-bg-color);
            color: var(--md-default-fg-color);
            padding: 20px;
            border-radius: 8px;
            max-width: 500px;
            width: 90%;
            max-height: 70vh;
            overflow-y: auto;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h2 style="margin: 0;">${title}</h2>
                <button onclick="this.closest('.mermaid-modal').remove()" style="
                    background: none;
                    border: none;
                    font-size: 20px;
                    cursor: pointer;
                    color: var(--md-default-fg-color);
                ">&times;</button>
            </div>
            ${content}
        </div>
    `;

    document.body.appendChild(modal);

    // Close on background click
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    });

    return modal;
}

function observeThemeChanges(mermaidModule) {
    // Watch for Material Design theme changes
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'data-md-color-scheme') {
                // Theme changed, reinitialize Mermaid
                setTimeout(() => {
                    mermaidModule.initialize({
                        ...mermaidModule.getConfig(),
                        theme: getTheme()
                    });
                    mermaidModule.init();
                }, 100);
            }
        });
    });

    observer.observe(document.body, {
        attributes: true,
        attributeFilter: ['data-md-color-scheme']
    });
}

function addDockerDiagramHandlers() {
    // Add specific handlers for Docker platform diagrams
    document.addEventListener('DOMContentLoaded', function() {
        // Auto-animate certain diagram types
        const animatedDiagrams = document.querySelectorAll('[data-diagram-type="monitoring"]');
        animatedDiagrams.forEach(diagram => {
            const nodes = diagram.querySelectorAll('.node');
            nodes.forEach((node, index) => {
                setTimeout(() => {
                    node.classList.add('animated-node');
                }, index * 200);
            });
        });
    });
}

// Global functions for modal actions (called from onclick handlers)
window.viewServiceLogs = function(serviceId) {
    console.log('Viewing logs for:', serviceId);
    // In real implementation, this would open a log viewer
    alert(`Opening logs for ${serviceId}`);
};

window.restartService = function(serviceId) {
    console.log('Restarting service:', serviceId);
    // In real implementation, this would call a restart API
    alert(`Restarting ${serviceId}`);
};

window.openDatabaseConsole = function(dbId) {
    console.log('Opening database console for:', dbId);
    // In real implementation, this would open a DB console
    alert(`Opening database console for ${dbId}`);
};

window.openAPITester = function(apiId) {
    console.log('Opening API tester for:', apiId);
    // In real implementation, this would open an API testing interface
    alert(`Opening API tester for ${apiId}`);
};
