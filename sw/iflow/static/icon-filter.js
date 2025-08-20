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
        
        // Apply color filters based on state
        this.updateIconColors();
    }
    
    /**
     * Update icon colors using CSS filters
     */
    updateIconColors() {
        if (!this.iconElement) return;
        
        let filterValue = '';
        switch (this.state) {
            case 'active':
                // Simple orange filter - much more reliable
                filterValue = 'hue-rotate(14deg) saturate(200%) brightness(1.2)';
                break;
            case 'inactive':
                // Simple grey filter - much more reliable
                filterValue = 'grayscale(100%) brightness(0.6)';
                break;
            case 'disabled':
                // Simple light grey filter - much more reliable
                filterValue = 'grayscale(100%) brightness(0.8) opacity(0.6)';
                break;
            default:
                // Default grey
                filterValue = 'grayscale(100%) brightness(0.6)';
        }
        
        this.iconElement.style.filter = filterValue;
        console.log(`IconFilter: Applied filter "${filterValue}" for state "${this.state}"`);
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
}
