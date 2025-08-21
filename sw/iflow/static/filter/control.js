/**
 * Base Filter Control Class
 * Self-managing filter with auto-registration and state management
 */
class FilterControl {
    static registry = new Map();
    
    constructor(container, filterType, options = {}) {
        this.container = container;
        this.filterType = filterType;
        this.state = 'inactive';
        
        // Get DOM elements
        this.control = this.container.querySelector('.filter-control') || this.container;
        this.footer = this.container.querySelector('.filter-footer');
        
        // Auto-register this filter
        FilterControl.registry.set(this.filterType, this);
        
        this.initialize();
    }
    
    // Static methods for registry management
    static getFilter(filterType) {
        return FilterControl.registry.get(filterType);
    }
    
    static getAllFilters() {
        return Array.from(FilterControl.registry.values());
    }
    
    static setupAllFilters() {
        // Auto-discover and setup all filter controls in the DOM
        const filterWrappers = document.querySelectorAll('.filter-wrapper');
        
        filterWrappers.forEach(wrapper => {
            const footer = wrapper.querySelector('.filter-footer');
            if (!footer) {
                console.warn('No footer found in wrapper:', wrapper);
                return;
            }
            
            // Use data-filter-type attribute if available, otherwise fall back to footer text
            let filterType = wrapper.getAttribute('data-filter-type');
            if (!filterType) {
                filterType = footer.textContent.toLowerCase().trim();
                console.warn(`No data-filter-type attribute found, using footer text: "${filterType}"`);
            }
            
            console.log(`Setting up filter: "${filterType}" in wrapper:`, wrapper);
            
            // Log what elements are found in the wrapper
            const hasInput = wrapper.querySelector('input[type="text"]');
            const hasSelect = wrapper.querySelector('select');
            const hasButton = wrapper.querySelector('button');
            
            console.log(`  - Has input: ${!!hasInput}, Has select: ${!!hasSelect}, Has button: ${!!hasButton}`);
            
            // Determine filter type and create appropriate instance with proper config
            if (hasInput) {
                console.log(`Creating TextInputFilter for: ${filterType}`);
                new TextInputFilter(wrapper, filterType);
            } else if (hasSelect) {
                console.log(`Creating SelectFilter for: ${filterType}`);
                new SelectFilter(wrapper, filterType);
            } else if (hasButton && !hasInput && !hasSelect) {
                // Only create IconFilter for pure button-based filters (no inputs/selects)
                console.log(`Creating IconFilter for: ${filterType}`);
                const iconConfig = FilterControl.getDefaultIconConfig(filterType);
                console.log(`  - Icon config:`, iconConfig);
                new IconFilter(wrapper, filterType, iconConfig);
            } else {
                console.log(`Creating base FilterControl for: ${filterType}`);
                new FilterControl(wrapper, filterType);
            }
        });
        
        console.log(`Auto-discovered and set up ${FilterControl.registry.size} filters`);
    }
    
    static getDefaultIconConfig(filterType) {
        // Provide default icon configurations for different filter types
        const configs = {
            'flag': {
                inactiveIcon: 'flag-outline',
                activeIcon: 'flag',
                disabledIcon: 'flag-outline'
            },
            'refresh': {
                inactiveIcon: 'refresh-outline',
                activeIcon: 'refresh-outline',
                disabledIcon: 'refresh-outline'
            },
            'create': {
                inactiveIcon: 'create-outline',
                activeIcon: 'create-outline',
                disabledIcon: 'create-outline'
            },
            'clear': {
                inactiveIcon: 'close',
                activeIcon: 'close',
                disabledIcon: 'close'
            }
        };
        
        // Return config for the filter type, or default flag config
        const config = configs[filterType];
        if (!config) {
            console.warn(`No icon config found for filter type: ${filterType}, using default`);
        }
        return config || {
            inactiveIcon: 'flag-outline',
            activeIcon: 'flag',
            disabledIcon: 'flag-outline'
        };
    }
    
    static connectToFilterManager(filterManager) {
        // Connect all registered filters to the FilterManager
        FilterControl.getAllFilters().forEach(filter => {
            filter.setFilterManager(filterManager);
        });
        console.log(`Connected ${FilterControl.registry.size} filters to FilterManager`);
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
     * Toggle between active, inactive, and disabled states
     * This allows cycling through: active -> inactive -> disabled -> active
     */
    cycleState() {
        console.log(`cycleState() called for ${this.filterType}, current state: ${this.state}`);
        
        switch (this.state) {
            case 'active':
                console.log(`  Transitioning: active -> inactive`);
                this.deactivate();
                break;
            case 'inactive':
                console.log(`  Transitioning: inactive -> disabled`);
                this.disable();
                break;
            case 'disabled':
                console.log(`  Transitioning: disabled -> active`);
                this.activate();
                break;
        }
        
        console.log(`  New state: ${this.state}`);
    }

    /**
     * Check if filter is currently applying its value
     */
    isApplying() {
        return this.state === 'active';
    }

    /**
     * Check if filter is disabled (not applying but keeping settings)
     */
    isDisabled() {
        return this.state === 'disabled';
    }

    /**
     * Get filter value for current state
     * Returns null if filter is disabled, otherwise returns the actual value
     */
    getEffectiveValue() {
        if (this.state === 'disabled') {
            return null; // Disabled filters don't apply their values
        }
        return this.getValue(); // Subclasses should implement this
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
        
        // Get the effective value (null if disabled, actual value otherwise)
        const effectiveValue = this.getEffectiveValue();
        
        // Update the filter manager with the effective value
        if (effectiveValue !== null) {
            this.filterManager.updateFilter(this.filterType, effectiveValue);
        } else {
            // Disabled filters don't apply their values
            this.filterManager.updateFilter(this.filterType, this.getDefaultValue());
        }
        
    }

    /**
     * Get the default value for this filter type when disabled
     * Subclasses can override this to provide appropriate default values
     */
    getDefaultValue() {
        // Default implementation returns empty string/false
        // Subclasses can override for specific types
        return '';
    }
    
    /**
     * Bind event handlers
     */
    bindEvents() {
        // Auto-setup click handler for filter footer
        if (this.footer) {
            // Remove any existing href from parent anchor
            const link = this.footer.closest('a');
            if (link) {
                link.removeAttribute('href');
                link.style.textDecoration = 'none';
            }
            
            // Add click handler for state cycling
            this.footer.addEventListener('click', (e) => {
                console.log(`Footer clicked for ${this.filterType} filter`);
                e.preventDefault();
                e.stopPropagation();
                this.cycleState();
            });
            
            // Style as clickable
            this.footer.style.cursor = 'pointer';
            this.footer.title = 'Click to cycle filter state: Active → Inactive → Disabled → Active';
        }
        
        // Subclasses can override to add specific event handling
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
    

    

}
