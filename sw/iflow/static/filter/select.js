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
            this.selectElement.addEventListener('change', () => {
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
    }
}
