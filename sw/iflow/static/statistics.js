// Statistics Management System
// This file contains all statistics functionality for the iflow application

class StatisticsManager {
    constructor() {
        this.currentStats = null;
        this.projectConfig = null;
        this.isInitialized = false;
        this.statsBarElement = null;
    }

    initialize(projectConfig) {
        this.projectConfig = projectConfig;
        this.statsBarElement = document.getElementById('stats-bar');
        this.isInitialized = true;
        console.log('Statistics manager initialized successfully');
    }

    async loadStats() {
        try {
            console.log('loadStats called');
            
            const response = await fetch(`${API_BASE}/stats`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const stats = await response.json();
            console.log('Stats received:', stats);
            this.currentStats = stats;
            this.displayStats(stats);
            return stats;
        } catch (error) {
            console.error('Error loading stats:', error);
            console.error('Error details:', error.message, error.stack);
            if (this.statsBarElement) {
                this.statsBarElement.innerHTML = '<div class="error">Error loading statistics: ' + error.message + '</div>';
            }
            throw error;
        }
    }

    displayStats(stats) {
        if (!this.statsBarElement) {
            console.error('Stats bar element not found');
            return;
        }

        let projectVersion = '';
        if (this.projectConfig && this.projectConfig.version) {
            projectVersion = `<div class="stat-item">
                <div class="stat-number">v${this.projectConfig.version}</div>
                <div class="stat-label">Version</div>
            </div>`;
        }
        
        // Format last tag display
        let lastTagDisplay = '';
        if (stats.last_tag) {
            lastTagDisplay = `<div class="stat-item">
                <div class="stat-number">${stats.last_tag}</div>
                <div class="stat-label">Last Tag</div>
            </div>`;
        }
        
        // Format current branch display
        let currentBranchDisplay = '';
        if (stats.current_branch) {
            currentBranchDisplay = `<div class="stat-item">
                <div class="stat-number">${stats.current_branch}</div>
                <div class="stat-label">Branch</div>
            </div>`;
        }
        
        this.statsBarElement.innerHTML = `
            <div class="stat-item">
                <div class="stat-number">${stats.total_artifacts}</div>
                <div class="stat-label">Total Artifacts</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">${stats.total_commits}</div>
                <div class="stat-label">Total Commits</div>
            </div>
            ${lastTagDisplay}
            ${currentBranchDisplay}
            <div class="stat-item">
                <div class="stat-number">${Object.keys(stats.by_type).length}</div>
                <div class="stat-label">Artifact Types</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">${stats.last_commit ? '✓' : '✗'}</div>
                <div class="stat-label">Git Status</div>
            </div>
            ${projectVersion}
        `;
    }

    refreshStats() {
        if (this.isInitialized) {
            return this.loadStats();
        }
    }

    getCurrentStats() {
        return this.currentStats;
    }

    getStatsByType(typeId) {
        if (this.currentStats && this.currentStats.by_type) {
            return this.currentStats.by_type[typeId] || 0;
        }
        return 0;
    }

    getTotalArtifacts() {
        return this.currentStats ? this.currentStats.total_artifacts : 0;
    }

    getTotalCommits() {
        return this.currentStats ? this.currentStats.total_commits : 0;
    }

    getLastCommit() {
        return this.currentStats ? this.currentStats.last_commit : null;
    }

    cleanup() {
        this.currentStats = null;
        this.projectConfig = null;
        this.isInitialized = false;
        this.statsBarElement = null;
    }
}

