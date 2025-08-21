/**
 * Text Input Filter Control
 * Extends FilterControl to provide text input filter functionality
 */
class TextInputFilter extends FilterControl {
    constructor(container, filterType, options = {}) {
        super(container, filterType, options);
        
        // Get the input element
        this.inputElement = this.container.querySelector('input');
        
        // Get the clear button
        this.clearButton = this.container.querySelector('.clear-button');
        

        
        // Initialize with proper styling
        this.updateVisualState();
        
        // Bind events
        this.bindEvents();
    }
    
    /**
     * Override updateVisualState to include input-specific updates
     */
    updateVisualState() {
        super.updateVisualState();
        this.updateInputState();
        this.updateClearButtonVisibility();
    }
    
    /**
     * Update the input state based on current content
     */
    updateInputState() {
        if (!this.inputElement) return;
        
        // Don't auto-update state if filter is disabled
        if (this.state === 'disabled') return;
        
        const hasContent = this.inputElement.value.trim() !== '';
        
        // Only update state if it would be a meaningful change
        if (hasContent && this.state === 'inactive') {
            // Text entered and currently inactive - set to active
            this.setState('active');
        } else if (!hasContent && this.state === 'active') {
            // No text and currently active - set to inactive
            this.setState('inactive');
        }
        // If state is already correct, don't change it
    }
    
    /**
     * Update clear button visibility based on input content and filter state
     */
    updateClearButtonVisibility() {
        if (!this.clearButton) return;
        
        const hasContent = this.inputElement && this.inputElement.value.trim() !== '';
        
        if (hasContent) {
            // Show clear button when there's content (regardless of filter state)
            this.clearButton.style.display = 'block';
        } else {
            // Hide clear button when there's no content
            this.clearButton.style.display = 'none';
        }
    }
    
    /**
     * Override updateFilterManager to provide specific filter updates
     */
    updateFilterManager() {
        // Call the base class implementation which handles disabled state
        super.updateFilterManager();
    }
    
    /**
     * Override bindEvents to handle input-specific interactions
     */
    bindEvents() {
        // Call base class bindEvents to get footer click handler for state cycling
        super.bindEvents();
        
        if (this.inputElement) {
            // Listen for input changes
            this.inputElement.addEventListener('input', () => {
                this.updateInputState();
                this.updateFilterManager();
            });
            
            // Listen for keyup events
            this.inputElement.addEventListener('keyup', () => {
                this.updateInputState();
            });
        }
        
        if (this.clearButton) {
            // Handle clear button clicks
            this.clearButton.addEventListener('click', (e) => {
                e.preventDefault();
                this.clearInput();
            });
        }
    }
    
    /**
     * Clear the input and reset state
     */
    clearInput() {
        if (this.inputElement) {
            this.inputElement.value = '';
            this.setState('inactive');
            this.updateFilterManager();
            this.updateClearButtonVisibility();
        }
        console.log(`${this.filterType} filter cleared`);
    }
    
    /**
     * Get the current input value
     */
    getValue() {
        return this.inputElement ? this.inputElement.value.trim() : '';
    }
    
    /**
     * Set the input value
     */
    setValue(value) {
        if (this.inputElement) {
            this.inputElement.value = value;
            this.updateInputState();
            this.updateFilterManager();
            this.updateClearButtonVisibility();
        }
    }
    
    /**
     * Override destroy to clean up event listeners
     */
    destroy() {
        if (this.inputElement) {
            this.inputElement.removeEventListener('input', this.updateInputState);
            this.inputElement.removeEventListener('keyup', this.updateInputState);
        }
        
        if (this.clearButton) {
            this.clearButton.removeEventListener('click', this.clearInput);
        }
    }
}
