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
        
        // Track if state changes are automatic (from text input) or manual (from user interaction)
        this.isAutoStateChange = false;
        
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
        
        // Don't auto-update state if it was manually set to disabled
        // Allow automatic updates for inactive state and when it's an auto state change
        if (this.state === 'disabled' && !this.isAutoStateChange) {
            return; // Preserve manually set disabled state
        }
        
        // Don't auto-update state if it was manually set to inactive (unless it's an auto change)
        if (this.state === 'inactive' && !this.isAutoStateChange) {
            return; // Preserve manually set inactive state
        }
        
        const hasContent = this.inputElement.value.trim() !== '';
        
        if (hasContent) {
            // Text entered - set to active (but respect manually disabled state)
            if (this.state !== 'disabled') {
                this.isAutoStateChange = true;
                this.setState('active');
                this.isAutoStateChange = false;
            }
        } else {
            // No text - set to inactive
            this.isAutoStateChange = true;
            this.setState('inactive');
            this.isAutoStateChange = false;
        }
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
            // Listen for input changes (real user typing)
            this.inputElement.addEventListener('input', (e) => {
                console.log(`TextInputFilter: input event triggered, value: "${e.target.value}"`);
                this.isAutoStateChange = true; // Mark as automatic state change for user input
                
                // Report user input event through EventManager
                if (window.eventManager) {
                    console.log(`TextInputFilter: queueing filterInputChange event`);
                    window.eventManager.queueUserEvent('filterInputChange', {
                        sourceId: this.controlId,
                        filterType: this.filterType,
                        inputValue: e.target.value,
                        eventType: 'input',
                        currentState: this.state
                    });
                } else {
                    console.error(`TextInputFilter: EventManager not available!`);
                    // Fallback: update directly if EventManager is not available
                    this.updateInputState();
                    this.updateClearButtonVisibility();
                    this.updateFilterManager();
                }
                this.isAutoStateChange = false;
            });
            
            // Listen for keyup events (real user typing)
            this.inputElement.addEventListener('keyup', (e) => {
                this.isAutoStateChange = true; // Mark as automatic state change for user input
                
                // Report user keyup event through EventManager
                if (window.eventManager) {
                    window.eventManager.queueUserEvent('filterKeyUp', {
                        sourceId: this.controlId,
                        filterType: this.filterType,
                        inputValue: e.target.value,
                        key: e.key,
                        currentState: this.state
                    });
                } else {
                    // Fallback: update directly if EventManager is not available
                    this.updateInputState();
                    this.updateClearButtonVisibility();
                }
                this.isAutoStateChange = false;
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
            // Mark this as an automatic state change to allow proper state updates
            this.isAutoStateChange = true;
            this.updateInputState();
            this.updateFilterManager();
            this.updateClearButtonVisibility();
            this.isAutoStateChange = false;
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
