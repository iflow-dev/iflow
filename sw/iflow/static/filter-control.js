/**
 * Base Filter Control Class
 * Manages filter state, styling, and coordination with FilterManager
 */
class FilterControl {
    constructor(container, filterType, options = {}) {
        this.container = container;
        this.filterType = filterType;
        this.options = {
            activeColor: '#ff8c00',      // Orange for active state
            inactiveColor: 'transparent', // Transparent for inactive state (changed from grey)
            disabledColor: '#dee2e6',    // Light grey for disabled state
            borderWidth: '2px',
            // New color configuration options
            borderColors: {
                border1: '#333',         // Dotted outline (always black)
                border2: 'transparent',  // Filter state border (transparent for inactive)
                border3: '#4ecdc4',      // Button border (teal)
                border4: '#45b7d1'       // Icon border (blue)
            },
            areaColors: {
                areaA: 'transparent',    // Border area (transparent for inactive)
                areaB: 'transparent',    // Content area (transparent for inactive)
                areaC: 'rgba(255,0,0,0.1)',  // Button area (red for inactive)
                areaD: 'rgba(255,0,0,0.1)'     // Icon area (red for inactive)
            },
            textColors: {
                active: '#ffffff',       // White text for active state
                inactive: '#495057',     // Dark grey text for inactive state
                disabled: '#6c757d'      // Medium grey text for disabled state
            },
            ...options
        };
        
        this.state = 'inactive'; // inactive, active, disabled
        this.filterManager = null;
        
        // Get DOM elements
        this.control = this.container.querySelector('.filter-control') || this.container;
        this.footer = this.container.querySelector('.filter-footer');
        
        this.initialize();
    }
    
    /**
     * Initialize the filter control
     */
    initialize() {
        this.updateVisualState();
        this.bindEvents();
    }
    
    /**
     * Set the filter manager reference
     */
    setFilterManager(filterManager) {
        this.filterManager = filterManager;
    }
    
    /**
     * Get current filter state
     */
    getState() {
        return this.state;
    }
    
    /**
     * Set filter state
     */
    setState(newState) {
        if (this.state === newState) return;
        
        this.state = newState;
        this.updateVisualState();
        this.updateFilterManager();
    }
    
    /**
     * Activate the filter
     */
    activate() {
        this.setState('active');
    }
    
    /**
     * Deactivate the filter
     */
    deactivate() {
        this.setState('inactive');
    }
    
    /**
     * Disable the filter
     */
    disable() {
        this.setState('disabled');
    }
    
    /**
     * Enable the filter
     */
    enable() {
        this.setState('inactive');
    }
    
    /**
     * Toggle between active and inactive
     */
    toggle() {
        if (this.state === 'active') {
            this.deactivate();
        } else if (this.state === 'inactive') {
            this.activate();
        }
    }
    
    /**
     * Update visual appearance based on state
     */
    updateVisualState() {
        if (!this.control || !this.footer) return;
        
        // Remove all state classes
        this.container.classList.remove('filter-active', 'filter-inactive', 'filter-disabled');
        
        // Add current state class
        this.container.classList.add(`filter-${this.state}`);
        
        // Update control styling
        this.updateControlStyling();
        
        // Update footer styling
        this.updateFooterStyling();

        // Apply border and area colors
        this.applyBorderColors();
        this.applyAreaColors();
    }
    
    /**
     * Update control element styling
     */
    updateControlStyling() {
        if (!this.control) return;
        
        const colors = this.getStateColors();
        
        // Update border color
        this.control.style.borderColor = colors.border;
        
        // Update background color if it's a button
        if (this.control.tagName === 'BUTTON') {
            this.control.style.backgroundColor = colors.background;
            this.control.style.color = colors.text;
        }
    }
    
    /**
     * Update footer element styling
     */
    updateFooterStyling() {
        if (!this.footer) return;
        
        // Use the specific text color for the current state
        const textColor = this.options.textColors[this.state] || this.options.textColors.inactive;
        this.footer.style.color = textColor;
    }
    
    /**
     * Get colors for current state
     */
    getStateColors() {
        switch (this.state) {
            case 'active':
                return {
                    border: this.options.activeColor,
                    background: this.options.activeColor,
                    text: this.options.textColors.active,
                    footer: this.options.activeColor
                };
            case 'inactive':
                return {
                    border: this.options.inactiveColor,
                    background: 'transparent',
                    text: this.options.textColors.inactive,
                    footer: this.options.inactiveColor
                };
            case 'disabled':
                return {
                    border: this.options.disabledColor,
                    background: 'transparent',
                    text: this.options.textColors.disabled,
                    footer: this.options.disabledColor
                };
            default:
                return {
                    border: this.options.inactiveColor,
                    background: 'transparent',
                    text: this.options.inactiveColor,
                    footer: this.options.inactiveColor
                };
        }
    }
    
    /**
     * Update FilterManager with current state
     */
    updateFilterManager() {
        if (!this.filterManager) return;
        
        // This method should be overridden by subclasses
        // to provide specific filter value updates
        console.log(`FilterControl ${this.filterType} state changed to: ${this.state}`);
    }
    
    /**
     * Bind event handlers
     */
    bindEvents() {
        // This method should be overridden by subclasses
        // to provide specific event handling
    }
    
    /**
     * Clean up event listeners
     */
    destroy() {
        // This method should be overridden by subclasses
        // to clean up specific event listeners
    }

    /**
     * Set border colors for different border levels
     * @param {Object} colors - Object with border1, border2, border3, border4 properties
     */
    setBorderColors(colors) {
        this.options.borderColors = { ...this.options.borderColors, ...colors };
        this.updateVisualState();
    }
    
    /**
     * Set area colors for different functional areas
     * @param {Object} colors - Object with areaA, areaB, areaC, areaD properties
     */
    setAreaColors(colors) {
        this.options.areaColors = { ...this.options.areaColors, ...colors };
        this.updateVisualState();
    }
    
    /**
     * Get current border colors configuration
     */
    getBorderColors() {
        return { ...this.options.borderColors };
    }
    
    /**
     * Get current area colors configuration
     */
    getAreaColors() {
        return { ...this.options.areaColors };
    }
    
    /**
     * Set specific border color by level
     * @param {string} level - 'border1', 'border2', 'border3', or 'border4'
     * @param {string} color - CSS color value
     */
    setBorderColor(level, color) {
        if (this.options.borderColors.hasOwnProperty(level)) {
            this.options.borderColors[level] = color;
            this.updateVisualState();
        } else {
            console.warn(`Invalid border level: ${level}. Use 'border1', 'border2', 'border3', or 'border4'`);
        }
    }
    
    /**
     * Set specific area color by area
     * @param {string} area - 'areaA', 'areaB', 'areaC', or 'areaD'
     * @param {string} color - CSS color value
     */
    setAreaColor(area, color) {
        if (this.options.areaColors.hasOwnProperty(area)) {
            this.options.areaColors[area] = color;
            this.updateVisualState();
        } else {
            console.warn(`Invalid area: ${area}. Use 'areaA', 'areaB', 'areaC', or 'areaD'`);
        }
    }
    
    /**
     * Set text color for a specific state
     * @param {string} state - 'active', 'inactive', or 'disabled'
     * @param {string} color - CSS color value
     */
    setTextColor(state, color) {
        if (this.options.textColors.hasOwnProperty(state)) {
            this.options.textColors[state] = color;
            this.updateVisualState();
        } else {
            console.warn(`Invalid state: ${state}. Use 'active', 'inactive', or 'disabled'`);
        }
    }
    
    /**
     * Set all text colors at once
     * @param {Object} colors - Object with active, inactive, disabled properties
     */
    setTextColors(colors) {
        this.options.textColors = { ...this.options.textColors, ...colors };
        this.updateVisualState();
    }
    
    /**
     * Get current text colors configuration
     */
    getTextColors() {
        return { ...this.options.textColors };
    }
    
    /**
     * Apply border colors to the container based on current state
     */
    applyBorderColors() {
        if (!this.container) return;
        
        const colors = this.options.borderColors;
        
        // Apply Border 1 (dotted outline) - always visible
        this.container.style.outline = `3px dotted ${colors.border1}`;
        this.container.style.outlineOffset = '6px';
        
        // Apply Border 2 (filter state border) - based on current state
        const stateColor = this.getStateColors().border;
        this.container.style.border = `${this.options.borderWidth} solid ${stateColor}`;
        
        // Note: Border 3 and 4 are typically handled by child elements
        // and would need specific implementation in subclasses
    }
    
    /**
     * Apply area colors to the container
     */
    applyAreaColors() {
        if (!this.container) return;
        
        const colors = this.options.areaColors;
        
        // Apply area A (border area) to the container background
        this.container.style.backgroundColor = colors.areaA;
        
        // Apply area C (button area) to the button element if it exists
        if (this.control && this.control.tagName === 'BUTTON') {
            if (this.state === 'inactive') {
                this.control.style.backgroundColor = colors.areaC; // Red background for inactive button
            } else {
                this.control.style.backgroundColor = 'transparent'; // Transparent for other states
            }
        }
        
        // Apply area D (icon area) to the icon element if it exists
        const iconElement = this.container.querySelector('.icon-svg');
        if (iconElement) {
            if (this.state === 'inactive') {
                iconElement.style.backgroundColor = colors.areaD; // Red background for inactive icon
            } else {
                iconElement.style.backgroundColor = 'transparent'; // Transparent for other states
            }
        }
        
        // Apply area B (content area) based on current state
        switch (this.state) {
            case 'active':
                // Keep area A background, content area handled by CSS
                break;
            case 'inactive':
                // Keep area A background, content area handled by CSS
                break;
            case 'disabled':
                // Keep area A background, content area handled by CSS
                break;
        }
    }
}
