/**
 * Icon Filter Control
 * Extends FilterControl to provide icon-based filter functionality
 */
class IconFilter extends FilterControl {
    constructor(container, filterType, iconConfig, options = {}) {
        super(container, filterType, options);
        
        this.iconConfig = {
            inactiveIcon: iconConfig.inactiveIcon || 'flag-outline',
            activeIcon: iconConfig.activeIcon || 'flag',
            disabledIcon: iconConfig.disabledIcon || 'flag-outline',
            ...iconConfig
        };
        
        // Ensure container has proper class and id attributes
        this.container.classList.add('filter-control');
        
        // Get the footer text to use as ID
        const footer = this.container.querySelector('.filter-footer');
        if (footer && footer.textContent) {
            const idText = footer.textContent.trim().toLowerCase();
            this.container.id = idText;
        }
        
        // Get the icon element
        this.iconElement = this.container.querySelector('.icon-svg');
        
        // Initialize with proper icon
        this.updateIcon();
    }
    
    /**
     * Override updateVisualState to include icon updates
     */
    updateVisualState() {
        super.updateVisualState();
        this.updateIcon();
    }
    
    /**
     * Update the icon based on current state
     */
    updateIcon() {
        if (!this.iconElement) return;
        
        // Always use the same icon file (flag.svg) but apply different colors
        const iconPath = `/static/icons/${this.iconConfig.activeIcon}.svg`;
        this.iconElement.src = iconPath;
        
        // Apply CSS classes based on state
        this.updateIconColors();
    }
    
    /**
     * Update icon colors using CSS classes
     */
    updateIconColors() {
        if (!this.iconElement) return;
        
        // Remove all state classes
        this.container.classList.remove('filter-active', 'filter-inactive', 'filter-disabled');
        
        // Add the current state class
        this.container.classList.add(`filter-${this.state}`);
        
        console.log(`IconFilter: Applied CSS class filter-${this.state}`);
    }
    
    /**
     * Override updateFilterManager to provide specific filter updates
     */
    updateFilterManager() {
        if (!this.filterManager) return;
        
        if (this.state === 'active') {
            // Activate the filter in FilterManager
            this.filterManager.updateFilter(this.filterType, true);
        } else {
            // Deactivate the filter in FilterManager
            this.filterManager.updateFilter(this.filterType, false);
        }
        
        console.log(`IconFilter ${this.filterType} updated FilterManager: ${this.state}`);
    }
    
    /**
     * Override bindEvents to handle icon-specific interactions
     */
    bindEvents() {
        if (this.control && this.control.tagName === 'BUTTON') {
            this.control.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggle();
            });
        }
    }
    
    /**
     * Override destroy to clean up event listeners
     */
    destroy() {
        if (this.control && this.control.tagName === 'BUTTON') {
            this.control.removeEventListener('click', this.toggle);
        }
    }
    
    /**
     * Set custom icon configuration
     */
    setIconConfig(newConfig) {
        this.iconConfig = { ...this.iconConfig, ...newConfig };
        this.updateIcon();
    }
    
    /**
     * Get current icon configuration
     */
    getIconConfig() {
        return { ...this.iconConfig };
    }
    
    /**
     * Get current state for debugging
     */
    getCurrentState() {
        return this.state;
    }
}
