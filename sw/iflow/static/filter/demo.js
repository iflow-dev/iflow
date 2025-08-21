/**
 * Demo implementation showing how to use FilterControl and IconFilter classes
 * This demonstrates the new architecture for filter controls
 */

// Example: How to create a flag filter using IconFilter
function createFlagFilter() {
    // Find the flag filter container
    const flagContainer = document.querySelector('#flagFilter').closest('.filter-wrapper');
    
    if (!flagContainer) {
        console.error('Flag filter container not found');
        return null;
    }
    
    // Create IconFilter instance
    const flagFilter = new IconFilter(flagContainer, 'flagged', {
        inactiveIcon: 'flag',        // Use flag.svg for both states
        activeIcon: 'flag',          // Use flag.svg for both states
        disabledIcon: 'flag'         // Use flag.svg for both states
    }, {
        activeColor: '#ff8c00',      // Orange when active
        inactiveColor: '#6c757d',    // Grey when inactive
        disabledColor: '#dee2e6'     // Light grey when disabled
    });
    
    // Set the filter manager reference
    if (window.filterManager) {
        flagFilter.setFilterManager(window.filterManager);
    }
    
    return flagFilter;
}

// Example: How to create other types of filter controls
function createTypeFilter() {
    const typeContainer = document.querySelector('#typeFilter').closest('.filter-wrapper');
    
    if (!typeContainer) return null;
    
    // This would be a different type of filter control
    // (e.g., SelectFilter that extends FilterControl)
    console.log('Type filter container found:', typeContainer);
}

// Example: How to manage multiple filter controls
class FilterControlManager {
    constructor() {
        this.controls = new Map();
        this.filterManager = null;
    }
    
    setFilterManager(filterManager) {
        this.filterManager = filterManager;
        this.controls.forEach(control => {
            control.setFilterManager(filterManager);
        });
    }
    
    addControl(filterType, control) {
        this.controls.set(filterType, control);
        if (this.filterManager) {
            control.setFilterManager(this.filterManager);
        }
    }
    
    getControl(filterType) {
        return this.controls.get(filterType);
    }
    
    getAllControls() {
        return Array.from(this.controls.values());
    }
    
    activateFilter(filterType) {
        const control = this.getControl(filterType);
        if (control) {
            control.activate();
        }
    }
    
    deactivateFilter(filterType) {
        const control = this.getControl(filterType);
        if (control) {
            control.deactivate();
        }
    }
    
    clearAllFilters() {
        this.controls.forEach(control => {
            control.deactivate();
        });
    }
    
    destroy() {
        this.controls.forEach(control => {
            control.destroy();
        });
        this.controls.clear();
    }
}

// Example: How to initialize all filter controls
function initializeFilterControls() {
    const filterControlManager = new FilterControlManager();
    
    // Create flag filter
    const flagFilter = createFlagFilter();
    if (flagFilter) {
        filterControlManager.addControl('flagged', flagFilter);
    }
    
    // Set the filter manager reference
    if (window.filterManager) {
        filterControlManager.setFilterManager(window.filterManager);
    }
    
    // Store the manager globally for access
    window.filterControlManager = filterControlManager;
    
    console.log('Filter controls initialized:', filterControlManager);
    return filterControlManager;
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        FilterControl,
        IconFilter,
        FilterControlManager,
        createFlagFilter,
        initializeFilterControls
    };
}
