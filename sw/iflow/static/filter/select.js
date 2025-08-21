/**
 * Select Filter Control
 * Extends FilterControl to provide select dropdown filter functionality
 */
class SelectFilter extends FilterControl {
    constructor(container, filterType, options = {}) {
        super(container, filterType, options);
        this.selectElement = this.container.querySelector('select');
        this.updateVisualState();
        this.bindEvents();
    }
    
    updateVisualState() {
        super.updateVisualState();
        this.updateSelectState();
    }
    
    updateSelectState() {
        if (!this.selectElement) return;
        
        // Don't auto-update state if filter is disabled
        if (this.state === 'disabled') return;
        
        // Don't auto-update state if filter is manually set to inactive
        if (this.state === 'inactive') return;
        
        const hasValue = this.selectElement.value && this.selectElement.value !== '';
        if (hasValue) {
            this.setState('active');
        } else {
            this.setState('inactive');
        }
    }
    
    updateFilterManager() {
        // Call the base class implementation which handles disabled state
        super.updateFilterManager();
    }
    
    bindEvents() {
        // Call base class bindEvents to get footer click handler for state cycling
        super.bindEvents();
        
        if (this.selectElement) {
            this.selectElement.addEventListener('change', (e) => {
                // Report user selection event through EventManager
                if (window.eventManager) {
                    console.log(`SelectFilter: queueing filterSelectChange event`);
                    window.eventManager.queueUserEvent('filterSelectChange', {
                        sourceId: this.controlId,
                        filterType: this.filterType,
                        selectedValue: e.target.value,
                        previousValue: this.getValue(),
                        currentState: this.state,
                        eventType: 'change'
                    });
                } else {
                    console.error(`SelectFilter: EventManager not available!`);
                }
                
                this.updateSelectState();
                this.updateFilterManager();
            });
        }
    }
    
    getValue() {
        return this.selectElement ? this.selectElement.value : '';
    }
    
    setValue(value) {
        if (this.selectElement) {
            this.selectElement.value = value;
            this.updateSelectState();
            this.updateFilterManager();
        }
    }
    
    clearFilter() {
        if (this.selectElement) {
            this.selectElement.value = '';
            this.setState('inactive');
            this.updateFilterManager();
        }
        console.log(`${this.filterType} filter cleared`);
    }
    
    destroy() {
        if (this.selectElement) {
            this.selectElement.removeEventListener('change', this.updateSelectState);
        }
        
        // Call base class destroy to clean up EventManager subscriptions
        super.destroy();
    }
    
    /**
     * Handle EventManager updates for SelectFilter-specific events
     */
    handleEventManagerUpdate(event) {
        // Call base class handler first
        super.handleEventManagerUpdate(event);
        
        // Handle SelectFilter-specific events
        switch (event.type) {
            case 'filterSelectChange':
                // Another filter's selection changed - could trigger coordinated behavior
                if (event.data.sourceId !== this.controlId) {
                    console.log(`${this.filterType} filter responding to other filter selection change`);
                    // Could implement coordinated behavior here
                }
                break;
            default:
                // Base class handles other event types
                break;
        }
    }
}
