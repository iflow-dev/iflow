// Search Management System
// This file contains all search functionality for the iflow application

class SearchManager {
    constructor() {
        if (SearchManager.instance) {
            return SearchManager.instance;
        }
        
        this.searchInput = null;
        this.isInitialized = false;
        this.tileManager = null;
        this.currentFilters = {}; // Initialize currentFilters object
        
        // Store the singleton instance
        SearchManager.instance = this;
        
        // Make it globally accessible
        window.searchManager = this;
        
        console.log('SearchManager singleton created');
    }

    /**
     * Get the singleton instance
     */
    static getInstance() {
        if (!SearchManager.instance) {
            new SearchManager();
        }
        return SearchManager.instance;
    }

    initialize(tileManager) {
        this.tileManager = tileManager;
        this.searchInput = document.getElementById('search-input');
        if (this.searchInput) {
            this.setupEventListeners();
            this.isInitialized = true;
            console.log('Search manager initialized successfully with TileManager');
        } else {
            console.error('Search input element not found');
        }
    }

    setupEventListeners() {
        if (this.searchInput) {
            this.searchInput.addEventListener('input', (e) => {
                this.currentFilters.search = e.target.value;
                this.performSearch();
            });
        }
    }

    performSearch() {
        if (!this.isInitialized) {
            console.warn('Search manager not initialized');
            return;
        }

        // Get the current search value
        const searchValue = this.getSearchValue();
        
        // Update the filter manager
        if (window.filterManager) {
            window.filterManager.updateFilter('search', searchValue);
        } else {
            console.warn('FilterManager not available');
        }
    }

    setSearchValue(value) {
        if (this.searchInput) {
            this.searchInput.value = value;
            this.currentFilters.search = value;
            // Update active class based on search value
            if (value && value !== '') {
                this.searchInput.classList.add('active');
            } else {
                this.searchInput.classList.remove('active');
            }
            
            // Update clear button visibility if the function exists
            if (typeof updateClearButtonVisibility === 'function') {
                updateClearButtonVisibility();
            }
        }
    }

    getSearchValue() {
        return this.searchInput ? this.searchInput.value : '';
    }

    clearSearch() {
        this.setSearchValue('');
        // Ensure active class is removed when clearing
        if (this.searchInput) {
            this.searchInput.classList.remove('active');
        }
    }



    /**
     * Update search results based on current filters
     * This method is called by FilterManager when filters change
     */
    async updateSearchResults(filters) {
        if (!this.isInitialized) {
            console.warn('Search manager not initialized');
            return;
        }

        console.log('Updating search results with filters:', filters);
        
        try {
            // Fetch filtered artifacts from API
            const artifacts = await this.fetchFilteredArtifacts(filters);
            
            // Update the DOM with new artifact tiles
            this.updateArtifactDisplay(artifacts);
            
        } catch (error) {
            console.error('Error updating search results:', error);
            this.showErrorInStatusLine('Failed to update search results: ' + error.message);
        }
    }

    /**
     * Fetch filtered artifacts from the API
     */
    async fetchFilteredArtifacts(filters) {
        let url = '/api/artifacts';
        const params = new URLSearchParams();
        
        if (filters.type && filters.type !== '') {
            params.append('type', filters.type);
        }
        if (filters.status && filters.status !== '') {
            params.append('status', filters.status);
        }
        if (filters.category && filters.category !== '') {
            params.append('category', filters.category);
        }
        if (filters.search && filters.search !== '') {
            params.append('search', filters.search);
        }
        
        if (params.toString()) {
            url += '?' + params.toString();
        }
        
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }

    /**
     * Update the DOM with new artifact tiles
     */
    updateArtifactDisplay(artifacts) {
        // Update filtered count display
        this.updateFilteredCount(artifacts.length);
        
        if (this.tileManager) {
            // Use TileManager to update the display
            this.tileManager.updateArtifacts(artifacts);
            this.tileManager.displayArtifacts(artifacts);
            console.log(`Updated display with ${artifacts.length} artifacts`);
        } else {
            // Fallback to direct DOM update
            this.updateArtifactDisplayFallback(artifacts);
        }
    }

    /**
     * Update filtered count display
     */
    updateFilteredCount(count) {
        const filteredCountElement = document.getElementById('filtered-count');
        if (filteredCountElement) {
            filteredCountElement.textContent = count;
        }
    }

    /**
     * Fallback method for updating artifact display
     */
    updateArtifactDisplayFallback(artifacts) {
        const container = document.getElementById('artifacts-container');
        if (!container) {
            console.error('Artifacts container not found');
            return;
        }
        
        // Clear existing content
        container.innerHTML = '';
        
        if (artifacts.length === 0) {
            container.innerHTML = '<div class="no-results">No artifacts found matching the current filters</div>';
            return;
        }
        
        // Create simple artifact tiles
        artifacts.forEach(artifact => {
            const tile = document.createElement('div');
            tile.className = 'artifact-tile';
            tile.innerHTML = `
                <div class="tile-header">
                    <span class="artifact-id">${artifact.artifact_id}</span>
                    <span class="artifact-type">${artifact.type || 'N/A'}</span>
                    <span class="artifact-status">${artifact.status || 'N/A'}</span>
                </div>
                <div class="tile-summary">${artifact.summary || 'No summary'}</div>
                <div class="tile-category">${artifact.category || 'No category'}</div>
            `;
            container.appendChild(tile);
        });
        
        console.log(`Updated display with ${artifacts.length} artifacts (fallback method)`);
    }

    /**
     * Show error message in status line
     */
    showErrorInStatusLine(message) {
        if (window.showErrorInStatusLine) {
            window.showErrorInStatusLine(message);
        } else {
            console.error('Status line error display not available:', message);
        }
    }



    cleanup() {
        if (this.searchInput) {
            this.searchInput.removeEventListener('input', this.performSearch);
            this.searchInput.classList.remove('active');
        }
        this.searchInput = null;
        this.isInitialized = false;
    }
}
