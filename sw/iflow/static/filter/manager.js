/**
 * Filter Manager - Manages all filter state and coordinates with SearchManager
 * Uses singleton pattern for global access
 */
class FilterManager {
    constructor() {
        if (FilterManager.instance) {
            return FilterManager.instance;
        }
        
        // Initialize filter state
        this.currentFilters = {
            type: '',
            status: '',
            category: '',
            search: '',
            flagged: false
        };
        
        // Reference to search manager
        this.searchManager = null;
        
        // Store the singleton instance
        FilterManager.instance = this;
        
        // Make it globally accessible
        window.filterManager = this;
        
        console.log('FilterManager singleton created');
    }

    /**
     * Get the singleton instance
     */
    static getInstance() {
        if (!FilterManager.instance) {
            new FilterManager();
        }
        return FilterManager.instance;
    }

    /**
     * Initialize the filter manager with search manager reference
     */
    initialize(searchManager) {
        this.searchManager = searchManager;
        console.log('FilterManager initialized with SearchManager');
    }

    /**
     * Get current filter settings
     */
    getFilter() {
        return { ...this.currentFilters };
    }

    /**
     * Update a specific filter
     */
    updateFilter(filterType, value) {
        if (filterType in this.currentFilters) {
            this.currentFilters[filterType] = value;
            console.log(`Filter updated: ${filterType} = ${value}`);
            
            // Trigger search manager update
            this.triggerSearchUpdate();
        } else {
            console.warn(`Unknown filter type: ${filterType}`);
        }
    }

    /**
     * Update multiple filters at once
     */
    updateFilters(filters) {
        Object.assign(this.currentFilters, filters);
        console.log('Multiple filters updated:', filters);
        
        // Trigger search manager update
        this.triggerSearchUpdate();
    }

    /**
     * Clear a specific filter
     */
    clearFilter(filterType) {
        if (filterType in this.currentFilters) {
            this.currentFilters[filterType] = '';
            console.log(`Filter cleared: ${filterType}`);
            
            // Trigger search manager update
            this.triggerSearchUpdate();
        }
    }

    /**
     * Clear all filters
     */
    clearAllFilters() {
        this.currentFilters = {
            type: '',
            status: '',
            category: '',
            search: '',
            flagged: false
        };
        console.log('All filters cleared');
        
        // Trigger search manager update
        this.triggerSearchUpdate();
    }

    /**
     * Toggle flag filter
     */
    toggleFlagFilter() {
        this.currentFilters.flagged = !this.currentFilters.flagged;
        console.log(`Flag filter toggled to: ${this.currentFilters.flagged}`);
        
        // Trigger search manager update
        this.triggerSearchUpdate();
    }

    /**
     * Check if any filters are active
     */
    hasActiveFilters() {
        return (
            (this.currentFilters.type && this.currentFilters.type !== '') ||
            (this.currentFilters.status && this.currentFilters.status !== '') ||
            (this.currentFilters.category && this.currentFilters.category !== '') ||
            (this.currentFilters.search && this.currentFilters.search !== '') ||
            this.currentFilters.flagged
        );
    }

    /**
     * Get active filter count
     */
    getActiveFilterCount() {
        let count = 0;
        if (this.currentFilters.type && this.currentFilters.type !== '') count++;
        if (this.currentFilters.status && this.currentFilters.status !== '') count++;
        if (this.currentFilters.category && this.currentFilters.category !== '') count++;
        if (this.currentFilters.search && this.currentFilters.search !== '') count++;
        if (this.currentFilters.flagged) count++;
        return count;
    }

    /**
     * Trigger search manager update with current filters
     */
    triggerSearchUpdate() {
        console.log(`triggerSearchUpdate called for filter: ${JSON.stringify(this.currentFilters)}`);
        
        if (this.searchManager) {
            console.log('SearchManager available, calling updateSearchResults');
            this.searchManager.updateSearchResults(this.currentFilters);
        } else {
            console.warn('SearchManager not available for filter update');
        }
    }

    /**
     * Apply filter state from external source
     */
    applyFilterState(filterState) {
        this.currentFilters = { ...filterState };
        console.log('External filter state applied:', filterState);
        
        // Trigger search manager update
        this.triggerSearchUpdate();
    }

    /**
     * Reset to default filter state
     */
    resetToDefaults() {
        this.currentFilters = {
            type: '',
            status: '',
            category: '',
            search: '',
            flagged: false
        };
        console.log('Filters reset to defaults');
        
        // Trigger search manager update
        this.triggerSearchUpdate();
    }
}
