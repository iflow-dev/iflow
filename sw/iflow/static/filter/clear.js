/**
 * Clear Filter Control
 * Extends FilterControl to provide clear filter functionality
 */
class ClearFilter extends FilterControl {
    constructor(container, filterType, options = {}) {
        super(container, filterType, options);
        
        // Get the clear button element
        this.clearButton = this.container.querySelector('button');
        
        // Initialize with proper styling
        this.updateIcon();
    }
    
    /**
     * Override updateVisualState to include clear button updates
     */
    updateVisualState() {
        super.updateVisualState();
        this.updateIcon();
    }
    
    /**
     * Update the clear button based on current state
     */
    updateIcon() {
        if (!this.clearButton) return;
        
        // Apply CSS classes based on state
        this.updateIconColors();
    }
    
    /**
     * Update icon colors using CSS classes
     */
    updateIconColors() {
        if (!this.clearButton) return;
        
        // Remove all state classes
        this.container.classList.remove('filter-active', 'filter-inactive', 'filter-disabled');
        
        // Add the current state class
        this.container.classList.add(`filter-${this.state}`);
        
        console.log(`ClearFilter: Applied CSS class filter-${this.state}`);
    }
    
    /**
     * Override updateFilterManager to provide specific filter updates
     */
    updateFilterManager() {
        if (!this.filterManager) return;
        
        if (this.state === 'active') {
            // Clear the specific filter type
            this.filterManager.updateFilter(this.filterType, false);
        }
        
        console.log(`ClearFilter ${this.filterType} updated FilterManager: ${this.state}`);
    }
    
    /**
     * Override bindEvents to handle clear button interactions
     */
    bindEvents() {
        if (this.clearButton) {
            this.clearButton.addEventListener('click', (e) => {
                e.preventDefault();
                this.executeClear();
            });
        }
    }
    
    /**
     * Execute the clear action
     */
    executeClear() {
        // Clear the specific filter
        if (this.filterType === 'search') {
            this.clearSearchFilter();
        } else if (this.filterType === 'category') {
            this.clearCategoryFilter();
        } else if (this.filterType === 'all') {
            this.clearAllFilters();
        }
        
        // Reset to inactive state
        this.setState('inactive');
    }
    
    /**
     * Clear search filter
     */
    clearSearchFilter() {
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.value = '';
        }
        if (window.searchManager) {
            window.searchManager.setSearchValue('');
        }
        console.log('Search filter cleared');
    }
    
    /**
     * Clear category filter
     */
    clearCategoryFilter() {
        const categoryInput = document.getElementById('categoryFilter');
        if (categoryInput) {
            categoryInput.value = '';
        }
        if (window.filterManager) {
            window.filterManager.updateFilter('category', '');
        }
        console.log('Category filter cleared');
    }
    
    /**
     * Clear all filters
     */
    clearAllFilters() {
        if (window.filterManager) {
            window.filterManager.clearAllFilters();
        }
        console.log('All filters cleared');
    }
    
    /**
     * Override destroy to clean up event listeners
     */
    destroy() {
        if (this.clearButton) {
            this.clearButton.removeEventListener('click', this.executeClear);
        }
    }
}
