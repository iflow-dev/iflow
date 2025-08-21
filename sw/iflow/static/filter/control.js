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
        this.controlId = `${filterType}-${Date.now()}`; // Unique identifier
        
        // Get DOM elements
        this.control = this.container.querySelector('.filter-control') || this.container;
        this.footer = this.container.querySelector('.filter-footer');
        
        // Debug update callback for real-time UI updates
        this.debugUpdateCallback = null;
        
        // Auto-register this filter
        FilterControl.registry.set(this.filterType, this);
        
        // Register with EventManager
        if (window.eventManager) {
            window.eventManager.registerControl(this.controlId, this);
            
            // Subscribe to EventManager updates
            window.eventManager.subscribe('filterFooterClick', this.handleEventManagerUpdate.bind(this), this.controlId);
            window.eventManager.subscribe('filterInputChange', this.handleEventManagerUpdate.bind(this), this.controlId);
            window.eventManager.subscribe('filterKeyUp', this.handleEventManagerUpdate.bind(this), this.controlId);
        }
        
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
     * Check if events are already bound to prevent duplicate binding
     */
    areEventsBound() {
        return this._eventsBound === true;
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
        
        // Call debug update callback if set
        if (this.debugUpdateCallback && typeof this.debugUpdateCallback === 'function') {
            this.debugUpdateCallback();
        }
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
     * Toggle between active and disabled states
     * This allows cycling through: active -> disabled -> active
     * (inactive state can only be reached by clearing text or programmatically)
     */
    cycleState() {
        // Mark this as a manual state change to prevent automatic overrides
        if (this.isAutoStateChange !== undefined) {
            this.isAutoStateChange = false;
        }
        
        switch (this.state) {
            case 'active':
                this.disable();
                break;
            case 'inactive':
                this.activate();
                break;
            case 'disabled':
                this.activate();
                break;
        }
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
     * Set debug update callback for real-time UI updates
     */
    setDebugUpdateCallback(callback) {
        if (typeof callback === 'function') {
            this.debugUpdateCallback = callback;
        }
    }
    
    /**
     * Get updates from EventManager
     * @param {Object} event - Event object from EventManager
     */
    handleEventManagerUpdate(event) {
        console.log(`${this.filterType} filter received event:`, event);
        
        // Handle different event types
        switch (event.type) {
            case 'filterFooterClick':
                // Check if this is our own click event
                if (event.data.sourceId === this.controlId) {
                    console.log(`${this.filterType} filter processing own click event`);
                    // This is our own click, so cycle the state
                    this.cycleState();
                } else {
                    // Another filter was clicked - could trigger coordinated behavior
                    console.log(`${this.filterType} filter responding to other filter click`);
                }
                break;
            case 'filterInputChange':
                // Check if this is our own input change
                if (event.data.sourceId === this.controlId) {
                    console.log(`${this.filterType} filter processing own input change`);
                    // This is our own input change, so update the input state
                    if (this.updateInputState) {
                        this.updateInputState();
                    }
                    // Also update clear button visibility and filter manager if methods exist
                    if (this.updateClearButtonVisibility) {
                        this.updateClearButtonVisibility();
                    }
                    if (this.updateFilterManager) {
                        this.updateFilterManager();
                    }
                } else {
                    // Another filter's input changed - could trigger coordinated behavior
                    console.log(`${this.filterType} filter responding to other filter input change`);
                }
                break;
            case 'filterKeyUp':
                // Check if this is our own keyup event
                if (event.data.sourceId === this.controlId) {
                    console.log(`${this.filterType} filter processing own keyup event`);
                    // This is our own keyup, so update the input state
                    if (this.updateInputState) {
                        this.updateInputState();
                    }
                    // Also update clear button visibility if method exists
                    if (this.updateClearButtonVisibility) {
                        this.updateClearButtonVisibility();
                    }
                } else {
                    // Another filter's keyup - could trigger coordinated behavior
                    console.log(`${this.filterType} filter responding to other filter keyup event`);
                }
                break;
            default:
                console.log(`${this.filterType} filter received unknown event type:`, event.type);
        }
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
     * Get the current filter value
     * Subclasses should override this to provide actual values
     */
    getValue() {
        // Default implementation returns empty string
        // Subclasses should override for specific types
        return '';
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
        // Prevent duplicate event binding
        if (this.areEventsBound()) {
            console.log(`FilterControl: Events already bound for ${this.filterType}, skipping duplicate binding`);
            return;
        }
        
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
                console.log(`FilterControl: footer click event triggered for ${this.filterType}`);
                e.preventDefault();
                e.stopPropagation();
                
                // Queue user click event through EventManager
                if (window.eventManager) {
                    console.log(`FilterControl: queueing filterFooterClick event`);
                    window.eventManager.queueUserEvent('filterFooterClick', {
                        sourceId: this.controlId,
                        filterType: this.filterType,
                        currentState: this.state,
                        action: 'cycleState'
                    });
                } else {
                    console.error(`FilterControl: EventManager not available!`);
                    // Fallback: call cycleState directly if EventManager is not available
                    this.cycleState();
                }
            });
            
            // Style as clickable
            this.footer.style.cursor = 'pointer';
            this.footer.title = 'Click to cycle filter state: Active → Inactive → Disabled → Active';
        }
        
        // Mark events as bound to prevent duplicate binding
        this._eventsBound = true;
        
        // Subclasses can override to add specific event handling
    }
    
    /**
     * Clean up event listeners and EventManager subscriptions
     */
    destroy() {
        // Unsubscribe from EventManager
        if (window.eventManager) {
            window.eventManager.unsubscribe('filterFooterClick', this.controlId);
            window.eventManager.unsubscribe('filterInputChange', this.controlId);
            window.eventManager.unsubscribe('filterKeyUp', this.controlId);
            window.eventManager.unregisterControl(this.controlId);
        }
        
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
