// Search Management System
// This file contains all search functionality for the iflow application

class SearchManager {
    constructor() {
        this.searchInput = null;
        this.currentFilters = {
            type: null,
            status: null,
            category: null,
            search: ''
        };
        this.isInitialized = false;
    }

    initialize() {
        this.searchInput = document.getElementById('search-input');
        if (this.searchInput) {
            this.setupEventListeners();
            this.isInitialized = true;
            console.log('Search manager initialized successfully');
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

        // Update the global filter state
        if (typeof currentFilterState !== 'undefined') {
            currentFilterState.search = this.currentFilters.search;
        }

        // Trigger the combined filter application
        if (typeof applyCombinedFilters === 'function') {
            applyCombinedFilters();
        } else {
            console.warn('applyCombinedFilters function not available');
        }
    }

    setSearchValue(value) {
        if (this.searchInput) {
            this.searchInput.value = value;
            this.currentFilters.search = value;
        }
    }

    getSearchValue() {
        return this.currentFilters.search || '';
    }

    clearSearch() {
        this.setSearchValue('');
    }

    updateFilters(newFilters) {
        this.currentFilters = { ...this.currentFilters, ...newFilters };
    }

    getCurrentFilters() {
        return { ...this.currentFilters };
    }

    resetFilters() {
        this.currentFilters = {
            type: null,
            status: null,
            category: null,
            search: ''
        };
        this.clearSearch();
    }

    cleanup() {
        if (this.searchInput) {
            this.searchInput.removeEventListener('input', this.performSearch);
        }
        this.searchInput = null;
        this.currentFilters = {
            type: null,
            status: null,
            category: null,
            search: ''
        };
        this.isInitialized = false;
    }
}
