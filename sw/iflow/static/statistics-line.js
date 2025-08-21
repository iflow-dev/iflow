/**
 * Statistics Line Management Class
 * Handles the statistics bar above the artifacts container
 */
class StatisticsLine {
    constructor() {
        this.statsBar = null;
        this.initialized = false;
    }
    
    /**
     * Initialize the statistics line
     */
    initialize() {
        try {
            this.statsBar = document.getElementById('stats-bar');
            
            if (this.statsBar) {
                this.initialized = true;
                this.showLoading();
                console.log('Statistics line initialized');
            } else {
                console.error('Statistics bar element not found');
            }
        } catch (error) {
            console.error('Error initializing statistics line:', error);
        }
    }
    
    /**
     * Show loading state
     */
    showLoading() {
        if (!this.initialized || !this.statsBar) return;
        
        try {
            this.statsBar.innerHTML = '<div class="loading">Loading statistics...</div>';
        } catch (error) {
            console.error('Error showing loading state:', error);
        }
    }
    
    /**
     * Show statistics content
     */
    showStatistics(statisticsHtml) {
        if (!this.initialized || !this.statsBar) return;
        
        try {
            this.statsBar.innerHTML = statisticsHtml;
        } catch (error) {
            console.error('Error showing statistics:', error);
        }
    }
    
    /**
     * Show error state
     */
    showError(errorMessage) {
        if (!this.initialized || !this.statsBar) return;
        
        try {
            this.statsBar.innerHTML = `<div class="error">Error loading statistics: ${errorMessage}</div>`;
        } catch (error) {
            console.error('Error showing error state:', error);
        }
    }
    
    /**
     * Show empty state
     */
    showEmpty() {
        if (!this.initialized || !this.statsBar) return;
        
        try {
            this.statsBar.innerHTML = '<div class="loading">No statistics available</div>';
        } catch (error) {
            console.error('Error showing empty state:', error);
        }
    }
    
    /**
     * Update statistics with new data
     */
    updateStatistics(statisticsData) {
        if (!this.initialized || !this.statsBar) return;
        
        try {
            if (statisticsData && statisticsData.length > 0) {
                // Generate statistics HTML
                const statsHtml = this.generateStatisticsHtml(statisticsData);
                this.showStatistics(statsHtml);
            } else {
                this.showEmpty();
            }
        } catch (error) {
            console.error('Error updating statistics:', error);
            this.showError('Failed to update statistics');
        }
    }
    
    /**
     * Generate statistics HTML from data
     */
    generateStatisticsHtml(statisticsData) {
        try {
            let html = '';
            
            statisticsData.forEach(stat => {
                html += `
                    <div class="stat-item">
                        <div class="stat-number">${stat.value}</div>
                        <div class="stat-label">${stat.label}</div>
                    </div>
                `;
            });
            
            return html;
        } catch (error) {
            console.error('Error generating statistics HTML:', error);
            return '<div class="error">Error generating statistics</div>';
        }
    }
    
    /**
     * Clear the statistics
     */
    clear() {
        if (!this.initialized || !this.statsBar) return;
        
        try {
            this.statsBar.innerHTML = '';
        } catch (error) {
            console.error('Error clearing statistics:', error);
        }
    }
    
    /**
     * Get current statistics content
     */
    getContent() {
        if (!this.initialized || !this.statsBar) return null;
        
        return this.statsBar.innerHTML;
    }
    
    /**
     * Check if statistics are currently loading
     */
    isLoading() {
        if (!this.initialized || !this.statsBar) return false;
        
        return this.statsBar.querySelector('.loading') !== null;
    }
    
    /**
     * Check if there's an error
     */
    hasError() {
        if (!this.initialized || !this.statsBar) return false;
        
        return this.statsBar.querySelector('.error') !== null;
    }
    
    /**
     * Destroy the statistics line
     */
    destroy() {
        try {
            this.statsBar = null;
            this.initialized = false;
            console.log('Statistics line destroyed');
        } catch (error) {
            console.error('Error destroying statistics line:', error);
        }
    }
}

// Create global statistics line instance
window.statisticsLine = new StatisticsLine();
