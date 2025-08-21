/**
 * Toolbar Management Class
 * Handles all toolbar functionality including filters, buttons, and initialization
 */
class Toolbar {
    constructor() {
        this.flagFilter = null;
        this.searchFilter = null;
        this.categoryFilter = null;
        this.typeFilter = null;
        this.statusFilter = null;
        this.clearAllFilter = null;
        this.initialized = false;
    }
    
    /**
     * Initialize the toolbar with all its components
     */
    async initialize() {
        try {
            console.log('Initializing toolbar...');
            
            // Initialize flag filter control
            this.initializeFlagFilter();
            
            // Initialize text input filters
            this.initializeTextInputFilters();
            
            // Initialize select dropdown filters
            this.initializeSelectFilters();
            
            // Initialize clear all filter
            this.initializeClearAllFilter();
            
            // Initialize refresh button
            this.initializeRefreshButton();
            
            this.initialized = true;
            console.log('Toolbar initialized successfully');
            
        } catch (error) {
            console.error('Error initializing toolbar:', error);
        }
    }
    
    /**
     * Initialize the flag filter control
     */
    initializeFlagFilter() {
        try {
            const flagFilterBtn = document.getElementById('flagFilter');
            if (flagFilterBtn) {
                const filterWrapper = flagFilterBtn.closest('.filter-wrapper');
                if (filterWrapper) {
                    // Start in inactive state
                    filterWrapper.classList.add('filter-inactive');
                    
                    // Initialize the FilterControl system for the flag filter
                    this.flagFilter = new IconFilter(filterWrapper, 'flagged', {
                        inactiveIcon: 'flag-outline',
                        activeIcon: 'flag',
                        disabledIcon: 'flag-outline'
                    });
                    
                    // Add new event listener
                    flagFilterBtn.addEventListener('click', (e) => {
                        e.preventDefault();
                        this.toggleFlagFilter();
                    });
                    
                    console.log('Flag filter control initialized');
                }
            }
        } catch (error) {
            console.error('Error initializing flag filter control:', error);
        }
    }
    
    /**
     * Initialize text input filters using TextInputFilter class
     */
    initializeTextInputFilters() {
        try {
            // Initialize search input filter
            const searchWrapper = document.querySelector('.search-filter[class*="filter-wrapper"]');
            if (searchWrapper) {
                this.searchFilter = new TextInputFilter(searchWrapper, 'search');
                if (window.filterManager) {
                    this.searchFilter.setFilterManager(window.filterManager);
                }
                searchWrapper.textInputFilter = this.searchFilter;
                console.log('Search input filter initialized');
            }
            
            // Initialize category input filter
            const categoryWrapper = document.querySelectorAll('.search-filter[class*="filter-wrapper"]')[1];
            if (categoryWrapper) {
                this.categoryFilter = new TextInputFilter(categoryWrapper, 'category');
                if (window.filterManager) {
                    this.categoryFilter.setFilterManager(window.filterManager);
                }
                categoryWrapper.textInputFilter = this.categoryFilter;
                console.log('Category input filter initialized');
            }
            
        } catch (error) {
            console.error('Error initializing text input filters:', error);
        }
    }
    
    /**
     * Initialize select dropdown filters (type and status)
     */
    initializeSelectFilters() {
        try {
            // Initialize type filter dropdown
            const typeWrapper = document.querySelector('#typeFilter').closest('.filter-wrapper');
            if (typeWrapper) {
                this.typeFilter = new SelectFilter(typeWrapper, 'type');
                if (window.filterManager) {
                    this.typeFilter.setFilterManager(window.filterManager);
                }
                typeWrapper.selectFilterControl = this.typeFilter;
                console.log('Type filter dropdown initialized with SelectFilter');
            }
            
            // Initialize status filter dropdown
            const statusWrapper = document.querySelector('#statusFilter').closest('.filter-wrapper');
            if (statusWrapper) {
                this.statusFilter = new SelectFilter(statusWrapper, 'status');
                if (window.filterManager) {
                    this.statusFilter.setFilterManager(window.filterManager);
                }
                statusWrapper.selectFilterControl = this.statusFilter;
                console.log('Status filter dropdown initialized with SelectFilter');
            }
        } catch (error) {
            console.error('Error initializing select filters:', error);
        }
    }
    
    /**
     * Initialize the clear all filter
     */
    initializeClearAllFilter() {
        try {
            const clearAllWrapper = document.getElementById('clearAllWrapper');
            if (clearAllWrapper) {
                this.clearAllFilter = new ClearFilter(clearAllWrapper, 'all');
                if (window.filterManager) {
                    this.clearAllFilter.setFilterManager(window.filterManager);
                }
                clearAllWrapper.clearFilterControl = this.clearAllFilter;
                console.log('Clear all filter initialized');
            }
        } catch (error) {
            console.error('Error initializing clear all filter:', error);
        }
    }
    
    /**
     * Initialize the refresh button
     */
    initializeRefreshButton() {
        try {
            const refreshBtn = document.querySelector('button[onclick="refreshArtifacts()"]');
            if (refreshBtn) {
                // Remove the inline onclick and add proper event listener
                refreshBtn.removeAttribute('onclick');
                refreshBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.refreshArtifacts();
                });
                console.log('Refresh button initialized');
            }
        } catch (error) {
            console.error('Error initializing refresh button:', error);
        }
    }
    
    /**
     * Toggle the flag filter
     */
    async toggleFlagFilter() {
        try {
            if (this.flagFilter) {
                // Toggle the filter control state
                this.flagFilter.toggle();
                
                // Update the FilterManager
                if (window.filterManager) {
                    const currentState = this.flagFilter.getState();
                    window.filterManager.updateFilter('flagged', currentState === 'active');
                    
                    // Trigger search update
                    window.filterManager.triggerSearchUpdate();
                }
                
                console.log(`Flag filter toggled to: ${this.flagFilter.getState()}`);
            }
        } catch (error) {
            console.error('Error toggling flag filter:', error);
        }
    }
    
    /**
     * Refresh artifacts
     */
    async refreshArtifacts() {
        try {
            if (window.tileManager) {
                await window.tileManager.loadArtifacts();
                console.log('Artifacts refreshed');
            }
        } catch (error) {
            console.error('Error refreshing artifacts:', error);
        }
    }
    
    /**
     * Clear search filter
     */
    clearSearch() {
        if (this.searchFilter) {
            this.searchFilter.clearInput();
        }
    }
    
    /**
     * Clear category filter
     */
    clearCategory() {
        if (this.categoryFilter) {
            this.categoryFilter.clearInput();
        }
    }
    
    /**
     * Clear all filters
     */
    clearAllFilters() {
        try {
            // Clear all filter controls
            if (this.flagFilter) {
                this.flagFilter.setState('inactive');
            }
            if (this.searchFilter) {
                this.searchFilter.clearInput();
            }
            if (this.categoryFilter) {
                this.categoryFilter.clearInput();
            }
            
            // Clear select filters
            if (this.typeFilter) {
                this.typeFilter.clearFilter();
            }
            if (this.statusFilter) {
                this.statusFilter.clearFilter();
            }
            
            // Clear all filter
            if (this.clearAllFilter) {
                this.clearAllFilter.setState('inactive');
            }
            
            // Update FilterManager
            if (window.filterManager) {
                window.filterManager.clearAllFilters();
                window.filterManager.triggerSearchUpdate();
            }
            
            console.log('All filters cleared');
        } catch (error) {
            console.error('Error clearing all filters:', error);
        }
    }
    
    /**
     * Get filter states
     */
    getFilterStates() {
        return {
            flag: this.flagFilter ? this.flagFilter.getState() : 'inactive',
            search: this.searchFilter ? this.searchFilter.getState() : 'inactive',
            category: this.categoryFilter ? this.categoryFilter.getState() : 'inactive',
            type: this.typeFilter ? this.typeFilter.getState() : 'inactive',
            status: this.statusFilter ? this.statusFilter.getState() : 'inactive'
        };
    }
    
    /**
     * Destroy the toolbar and clean up
     */
    destroy() {
        try {
            if (this.flagFilter) {
                this.flagFilter.destroy();
            }
            if (this.searchFilter) {
                this.searchFilter.destroy();
            }
            if (this.categoryFilter) {
                this.categoryFilter.destroy();
            }
            if (this.typeFilter) {
                this.typeFilter.destroy();
            }
            if (this.statusFilter) {
                this.statusFilter.destroy();
            }
            if (this.clearAllFilter) {
                this.clearAllFilter.destroy();
            }
            
            this.initialized = false;
            console.log('Toolbar destroyed');
        } catch (error) {
            console.error('Error destroying toolbar:', error);
        }
    }
}

// Create global toolbar instance
window.toolbar = new Toolbar();
