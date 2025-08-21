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
        
        const hasValue = this.selectElement.value && this.selectElement.value !== '';
        if (hasValue) {
            this.setState('active');
        } else {
            this.setState('inactive');
        }
    }
    
    updateFilterManager() {
        if (!this.filterManager) return;
        
        const currentValue = this.selectElement ? this.selectElement.value : '';
        if (this.state === 'active' && currentValue !== '') {
            this.filterManager.updateFilter(this.filterType, currentValue);
        } else {
            this.filterManager.updateFilter(this.filterType, '');
        }
        console.log(`SelectFilter ${this.filterType} updated FilterManager: ${currentValue}`);
    }
    
    bindEvents() {
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
