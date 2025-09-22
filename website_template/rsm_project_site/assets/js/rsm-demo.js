/**
 * RSM Interactive Demo
 * Real-time symbolic reasoning demonstration
 */

class RSMDemo {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.loadSampleData();
    }

    initializeElements() {
        this.tarotSelect = document.getElementById('tarot-select');
        this.astrologySelect = document.getElementById('astrology-select');
        this.sajuSelect = document.getElementById('saju-select');
        this.calculateBtn = document.getElementById('calculate-btn');
        this.resultsContainer = document.getElementById('demo-results');
    }

    bindEvents() {
        this.calculateBtn.addEventListener('click', () => this.calculateRSM());

        // Auto-calculate when selections change
        [this.tarotSelect, this.astrologySelect, this.sajuSelect].forEach(select => {
            select.addEventListener('change', () => this.autoCalculate());
        });
    }

    loadSampleData() {
        // Sample data from our experimental results
        this.symbolicData = {
            tarot: {
                "The Fool": { chaos: 0.8, rebirth: 0.9, transformation: 0.7, confidence: 0.85 },
                "Death": { chaos: 0.7, rebirth: 1.0, transformation: 1.0, confidence: 0.95 },
                "The Magician": { chaos: 0.3, rebirth: 0.6, transformation: 0.9, confidence: 0.9 },
                "The Tower": { chaos: 1.0, rebirth: 0.7, transformation: 0.8, confidence: 0.9 },
                "The High Priestess": { chaos: 0.2, rebirth: 0.8, transformation: 0.6, confidence: 0.8 }
            },
            astrology: {
                "Aries": { chaos: 0.9, rebirth: 0.8, transformation: 0.7, confidence: 0.85 },
                "Taurus": { chaos: 0.2, rebirth: 0.3, transformation: 0.4, confidence: 0.8 },
                "Gemini": { chaos: 0.7, rebirth: 0.6, transformation: 0.8, confidence: 0.75 },
                "Cancer": { chaos: 0.4, rebirth: 0.9, transformation: 0.6, confidence: 0.8 },
                "Leo": { chaos: 0.6, rebirth: 0.7, transformation: 0.8, confidence: 0.85 },
                "Scorpio": { chaos: 0.8, rebirth: 1.0, transformation: 1.0, confidence: 0.9 },
                "Pisces": { chaos: 0.5, rebirth: 0.8, transformation: 0.7, confidence: 0.7 }
            },
            saju: {
                "Fire Yang": { chaos: 0.8, rebirth: 0.6, transformation: 0.9, confidence: 0.9 },
                "Water Yang": { chaos: 0.5, rebirth: 0.9, transformation: 0.4, confidence: 0.85 },
                "Wood Yang": { chaos: 0.4, rebirth: 0.8, transformation: 0.7, confidence: 0.85 },
                "Metal Yin": { chaos: 0.3, rebirth: 0.3, transformation: 0.5, confidence: 0.8 },
                "Earth Yang": { chaos: 0.2, rebirth: 0.4, transformation: 0.3, confidence: 0.8 }
            }
        };
    }

    autoCalculate() {
        // Only auto-calculate if at least one input is selected
        const hasInput = this.tarotSelect.value || this.astrologySelect.value || this.sajuSelect.value;
        if (hasInput) {
            setTimeout(() => this.calculateRSM(), 300); // Small delay for better UX
        }
    }

    calculateRSM() {
        const input = this.gatherInput();

        if (Object.keys(input).length === 0) {
            this.showPlaceholder();
            return;
        }

        // Show loading state
        this.showLoading();

        // Simulate calculation (in real implementation, this would call the actual RSM API)
        setTimeout(() => {
            const result = this.performRSMCalculation(input);
            this.displayResults(result);
            this.trackDemoUsage(input, result);
        }, 800);
    }

    gatherInput() {
        const input = {};

        if (this.tarotSelect.value) {
            input.tarot = this.tarotSelect.value;
        }
        if (this.astrologySelect.value) {
            input.astrology = this.astrologySelect.value;
        }
        if (this.sajuSelect.value) {
            input.saju = this.sajuSelect.value;
        }

        return input;
    }

    performRSMCalculation(input) {
        // Simulate the actual RSM calculation based on our experimental data
        const vectors = [];
        const systems = [];
        const confidences = [];

        // Extract vectors from symbolic data
        Object.keys(input).forEach(system => {
            const symbol = input[system];
            if (this.symbolicData[system] && this.symbolicData[system][symbol]) {
                const data = this.symbolicData[system][symbol];
                vectors.push([data.chaos, data.rebirth, data.transformation]);
                systems.push(system);
                confidences.push(data.confidence);
            }
        });

        // Calculate VME (Vector of Meaning Energy)
        let vme;
        if (vectors.length === 0) {
            vme = [0.577, 0.577, 0.577]; // Default normalized vector
        } else {
            // Average the vectors
            const avgVector = [0, 0, 0];
            vectors.forEach(v => {
                avgVector[0] += v[0];
                avgVector[1] += v[1];
                avgVector[2] += v[2];
            });
            avgVector[0] /= vectors.length;
            avgVector[1] /= vectors.length;
            avgVector[2] /= vectors.length;

            // Normalize
            const norm = Math.sqrt(avgVector[0]**2 + avgVector[1]**2 + avgVector[2]**2);
            vme = avgVector.map(x => x / norm);
        }

        // Calculate Resonance Index (RI)
        const contextWeights = [1.0, 1.0, 1.0]; // Equal weights
        const weightedProjection = vme[0] * contextWeights[0] + vme[1] * contextWeights[1] + vme[2] * contextWeights[2];
        const normFactor = Math.sqrt(contextWeights[0]**2 + contextWeights[1]**2 + contextWeights[2]**2);

        // Calculate symbolic conflicts penalty
        const penalty = this.calculateSymbolicConflicts(vme);

        const ri = Math.max(0, Math.min(1, (weightedProjection / normFactor) - penalty));

        // Calculate confidence
        const overallConfidence = confidences.length > 0 ?
            confidences.reduce((a, b) => a + b, 0) / confidences.length : 0.5;

        // Determine drift status
        const driftStatus = ri > 0.7 ? 'STABLE' : ri > 0.4 ? 'WARNING' : 'CRITICAL';

        return {
            input: input,
            vme: vme,
            ri: ri,
            confidence: overallConfidence,
            systems: systems,
            driftStatus: driftStatus,
            timestamp: new Date().toISOString()
        };
    }

    calculateSymbolicConflicts(vme) {
        const [chaos, rebirth, transformation] = vme;

        // Primary conflicts
        const conflict1 = Math.abs(chaos - rebirth) * 0.15;
        const conflict2 = Math.abs(rebirth - transformation) * 0.1;
        const conflict3 = Math.abs(chaos - transformation) * 0.12;

        // Secondary conflicts
        const highChaosPenalty = Math.max(0, chaos - 0.8) * 0.05;
        const lowEnergyPenalty = Math.max(0, 0.2 - Math.min(chaos, rebirth, transformation)) * 0.08;

        const totalPenalty = conflict1 + conflict2 + conflict3 + highChaosPenalty + lowEnergyPenalty;

        return Math.min(0.3, totalPenalty);
    }

    showLoading() {
        this.resultsContainer.innerHTML = `
            <div class="loading-state">
                <div class="loading-spinner"></div>
                <p>Calculating resonant structures...</p>
            </div>
        `;
    }

    showPlaceholder() {
        this.resultsContainer.innerHTML = `
            <div class="results-placeholder">
                <i class="fas fa-brain"></i>
                <p>Select symbolic inputs and click "Calculate RSM" to see the magic happen!</p>
            </div>
        `;
    }

    displayResults(result) {
        const vmeValues = result.vme.map(v => v.toFixed(3));
        const riPercent = (result.ri * 100).toFixed(1);
        const confidencePercent = (result.confidence * 100).toFixed(0);

        const statusClass = result.driftStatus.toLowerCase();
        const statusColors = {
            stable: '#28a745',
            warning: '#fd7e14',
            critical: '#dc3545'
        };

        this.resultsContainer.innerHTML = `
            <div class="rsm-results">
                <div class="results-header">
                    <h3>RSM Analysis Results</h3>
                    <div class="status-indicator ${statusClass}">
                        <i class="fas fa-circle"></i>
                        ${result.driftStatus}
                    </div>
                </div>

                <div class="results-grid">
                    <div class="result-section">
                        <h4>Vector of Meaning Energy (VME)</h4>
                        <div class="vme-visualization">
                            <div class="vme-component">
                                <span class="label">Chaos</span>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: ${result.vme[0] * 100}%"></div>
                                </div>
                                <span class="value">${vmeValues[0]}</span>
                            </div>
                            <div class="vme-component">
                                <span class="label">Rebirth</span>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: ${result.vme[1] * 100}%"></div>
                                </div>
                                <span class="value">${vmeValues[1]}</span>
                            </div>
                            <div class="vme-component">
                                <span class="label">Transformation</span>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: ${result.vme[2] * 100}%"></div>
                                </div>
                                <span class="value">${vmeValues[2]}</span>
                            </div>
                        </div>
                    </div>

                    <div class="result-section">
                        <h4>Resonance Metrics</h4>
                        <div class="metrics-grid">
                            <div class="metric-card">
                                <div class="metric-value">${riPercent}%</div>
                                <div class="metric-label">Resonance Index</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value">${confidencePercent}%</div>
                                <div class="metric-label">Confidence</div>
                            </div>
                        </div>
                    </div>

                    <div class="result-section">
                        <h4>Systems Used</h4>
                        <div class="systems-list">
                            ${result.systems.map(system => `
                                <span class="system-tag">${system}</span>
                            `).join('')}
                        </div>
                    </div>
                </div>

                <div class="results-interpretation">
                    <h4>Interpretation</h4>
                    <p>${this.generateInterpretation(result)}</p>
                </div>

                <div class="results-actions">
                    <button class="btn btn-outline btn-sm" onclick="rsm.exportResults()">
                        <i class="fas fa-download"></i>
                        Export Results
                    </button>
                    <button class="btn btn-outline btn-sm" onclick="rsm.shareResults()">
                        <i class="fas fa-share"></i>
                        Share
                    </button>
                </div>
            </div>
        `;

        // Add animation
        this.resultsContainer.querySelector('.rsm-results').classList.add('animate-in');
    }

    generateInterpretation(result) {
        const ri = result.ri;
        const vme = result.vme;
        const [chaos, rebirth, transformation] = vme;

        let interpretation = "";

        if (ri > 0.8) {
            interpretation = "Strong symbolic resonance detected. The selected symbols demonstrate excellent interpretive alignment and cultural coherence.";
        } else if (ri > 0.6) {
            interpretation = "Moderate symbolic resonance. The combination shows good alignment with some minor interpretive tensions.";
        } else if (ri > 0.4) {
            interpretation = "Weak symbolic resonance. Significant interpretive conflicts detected between the selected symbols.";
        } else {
            interpretation = "Very low symbolic resonance. The selected combination shows substantial interpretive discord.";
        }

        // Add dimension-specific insights
        const dominantDimension = chaos > rebirth && chaos > transformation ? 'chaos' :
                                rebirth > transformation ? 'rebirth' : 'transformation';

        const dimensionInsights = {
            chaos: "The analysis reveals a strong chaotic influence, suggesting themes of disruption and dynamic change.",
            rebirth: "Rebirth emerges as the dominant theme, indicating powerful transformative potential and renewal.",
            transformation: "Transformation takes precedence, highlighting deliberate change and evolutionary progression."
        };

        return `${interpretation} ${dimensionInsights[dominantDimension]}`;
    }

    exportResults() {
        // In a real implementation, this would generate a downloadable report
        alert('Export functionality would generate a comprehensive RSM analysis report.');
    }

    shareResults() {
        // In a real implementation, this would create a shareable link
        alert('Share functionality would create a unique URL for this RSM analysis.');
    }

    trackDemoUsage(input, result) {
        // Track demo usage for analytics
        if (typeof gtag !== 'undefined') {
            gtag('event', 'demo_usage', {
                'paper_title': 'RSM Ontology',
                'demo_type': 'rsm_calculation',
                'input_systems': Object.keys(input).join(','),
                'resonance_index': result.ri,
                'drift_status': result.driftStatus
            });
        }
    }
}

// Initialize demo when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.rsm = new RSMDemo();
});

// Add CSS for demo-specific styling
const demoStyles = `
<style>
.demo-section {
    background: #f8f9fa;
}

.demo-container {
    max-width: 1000px;
    margin: 0 auto;
    background: white;
    border-radius: var(--radius-lg);
    padding: var(--spacing-xl);
    box-shadow: var(--shadow-md);
}

.demo-controls {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-xl);
}

.control-group label {
    display: block;
    font-weight: 500;
    margin-bottom: var(--spacing-xs);
    color: var(--flamehaven-secondary);
}

.form-control {
    width: 100%;
    padding: var(--spacing-sm);
    border: 2px solid var(--flamehaven-light);
    border-radius: var(--radius-md);
    font-family: var(--font-primary);
    transition: border-color 0.3s ease;
}

.form-control:focus {
    outline: none;
    border-color: var(--flamehaven-primary);
}

.demo-btn {
    grid-column: 1 / -1;
    justify-self: center;
    min-width: 200px;
}

.demo-results {
    min-height: 300px;
    position: relative;
}

.results-placeholder, .loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 300px;
    color: var(--flamehaven-text);
    opacity: 0.6;
}

.results-placeholder i, .loading-state i {
    font-size: 3rem;
    margin-bottom: var(--spacing-md);
    color: var(--flamehaven-primary);
}

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid var(--flamehaven-light);
    border-top: 4px solid var(--flamehaven-primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: var(--spacing-md);
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.rsm-results {
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.5s ease;
}

.rsm-results.animate-in {
    opacity: 1;
    transform: translateY(0);
}

.results-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-lg);
    padding-bottom: var(--spacing-md);
    border-bottom: 2px solid var(--flamehaven-light);
}

.status-indicator {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.9rem;
}

.status-indicator.stable { color: #28a745; }
.status-indicator.warning { color: #fd7e14; }
.status-indicator.critical { color: #dc3545; }

.results-grid {
    display: grid;
    gap: var(--spacing-lg);
    margin-bottom: var(--spacing-lg);
}

.result-section h4 {
    margin-bottom: var(--spacing-md);
    color: var(--flamehaven-secondary);
}

.vme-component {
    display: grid;
    grid-template-columns: 100px 1fr 60px;
    align-items: center;
    gap: var(--spacing-sm);
    margin-bottom: var(--spacing-sm);
}

.progress-bar {
    height: 8px;
    background: var(--flamehaven-light);
    border-radius: var(--radius-sm);
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: var(--flamehaven-primary);
    transition: width 0.8s ease;
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: var(--spacing-md);
}

.metric-card {
    text-align: center;
    padding: var(--spacing-md);
    background: var(--flamehaven-light);
    border-radius: var(--radius-md);
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--flamehaven-primary);
}

.metric-label {
    font-size: 0.9rem;
    color: var(--flamehaven-text);
    margin-top: var(--spacing-xs);
}

.systems-list {
    display: flex;
    gap: var(--spacing-sm);
    flex-wrap: wrap;
}

.system-tag {
    background: var(--flamehaven-primary);
    color: white;
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--radius-sm);
    font-size: 0.9rem;
    font-weight: 500;
}

.results-interpretation {
    background: rgba(255, 107, 53, 0.05);
    padding: var(--spacing-md);
    border-radius: var(--radius-md);
    border-left: 4px solid var(--flamehaven-primary);
    margin-bottom: var(--spacing-lg);
}

.results-actions {
    display: flex;
    gap: var(--spacing-sm);
    justify-content: center;
    flex-wrap: wrap;
}
</style>
`;

document.head.insertAdjacentHTML('beforeend', demoStyles);