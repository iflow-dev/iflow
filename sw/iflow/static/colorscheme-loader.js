/**
 * Color Scheme Loader for FilterControl
 * Loads and applies color schemes from colorscheme.yaml
 */

class ColorSchemeLoader {
    constructor() {
        this.colorScheme = null;
        this.currentTheme = 'default';
    }
    
    /**
     * Load color scheme from YAML file
     * @param {string} yamlPath - Path to colorscheme.yaml
     * @returns {Promise<Object>} - Parsed color scheme
     */
    async loadColorScheme(yamlPath = '/static/colorscheme.yaml') {
        try {
            const response = await fetch(yamlPath);
            if (!response.ok) {
                throw new Error(`Failed to load color scheme: ${response.status}`);
            }
            
            const yamlText = await response.text();
            this.colorScheme = this.parseYAML(yamlText);
            console.log('Color scheme loaded successfully:', this.colorScheme);
            return this.colorScheme;
            
        } catch (error) {
            console.error('Error loading color scheme:', error);
            // Fallback to default colors
            this.colorScheme = this.getDefaultColorScheme();
            return this.colorScheme;
        }
    }
    
    /**
     * Simple YAML parser for basic key-value pairs
     * @param {string} yamlText - Raw YAML text
     * @returns {Object} - Parsed YAML object
     */
    parseYAML(yamlText) {
        const result = {};
        const lines = yamlText.split('\n');
        let currentSection = null;
        let currentSubsection = null;
        
        for (const line of lines) {
            const trimmedLine = line.trim();
            
            // Skip empty lines and comments
            if (!trimmedLine || trimmedLine.startsWith('#')) {
                continue;
            }
            
            // Check for section headers
            if (trimmedLine.endsWith(':')) {
                const sectionName = trimmedLine.slice(0, -1);
                if (!trimmedLine.startsWith(' ')) {
                    // Main section
                    currentSection = sectionName;
                    currentSubsection = null;
                    result[currentSection] = {};
                } else {
                    // Subsection
                    currentSubsection = sectionName;
                    if (currentSection) {
                        if (!result[currentSection][currentSubsection]) {
                            result[currentSection][currentSubsection] = {};
                        }
                    }
                }
                continue;
            }
            
            // Parse key-value pairs
            if (trimmedLine.includes(':')) {
                const [key, ...valueParts] = trimmedLine.split(':');
                const value = valueParts.join(':').trim();
                
                if (currentSubsection && currentSection) {
                    result[currentSection][currentSubsection][key.trim()] = value;
                } else if (currentSection) {
                    result[currentSection][key.trim()] = value;
                } else {
                    result[key.trim()] = value;
                }
            }
        }
        
        return result;
    }
    
    /**
     * Get default color scheme if YAML loading fails
     * @returns {Object} - Default color scheme
     */
    getDefaultColorScheme() {
        return {
            colors: {
                orange: "#ff8c00",
                grey: "#6c757d",
                light_grey: "#dee2e6",
                dark_grey: "#495057",
                white: "#ffffff",
                black: "#333333"
            },
            states: {
                active: {
                    border2: "#ff8c00",
                    text: "#ffffff"
                },
                inactive: {
                    border2: "transparent",
                    text: "#495057"
                },
                disabled: {
                    border2: "#dee2e6",
                    text: "#6c757d"
                }
            },
            styling: {
                border_width: "2px",
                border_radius: "8px",
                padding: "0.25rem"
            }
        };
    }
    
    /**
     * Apply color scheme to a FilterControl instance
     * @param {FilterControl} filterControl - FilterControl instance to style
     * @param {string} theme - Theme name to apply
     */
    applyColorScheme(filterControl, theme = 'default') {
        if (!this.colorScheme) {
            console.warn('No color scheme loaded, using defaults');
            return;
        }
        
        try {
            // Apply state templates if available (most comprehensive)
            if (this.colorScheme.state_templates) {
                this.applyStateTemplates(filterControl);
            }
            
            // Apply theme-based colors if available
            if (this.colorScheme.themes && this.colorScheme.themes[theme]) {
                const themeColors = this.colorScheme.themes[theme];
                this.applyThemeColors(filterControl, themeColors);
            }
            
            // Apply global colors
            if (this.colorScheme.colors) {
                this.applyGlobalColors(filterControl);
            }
            
            // Apply styling
            if (this.colorScheme.styling) {
                this.applyStyling(filterControl);
            }
            
            // Apply icon colors
            if (this.colorScheme.icon_colors) {
                this.applyIconColors(filterControl);
            }
            
            // Apply border templates
            if (this.colorScheme.border_templates) {
                this.applyBorderTemplates(filterControl);
            }
            
            // Apply area templates
            if (this.colorScheme.area_templates) {
                this.applyAreaTemplates(filterControl);
            }
            
            console.log(`Applied color scheme theme: ${theme}`);
            
        } catch (error) {
            console.error('Error applying color scheme:', error);
        }
    }
    
    /**
     * Apply theme colors to FilterControl
     * @param {FilterControl} filterControl - FilterControl instance
     * @param {Object} themeColors - Theme color configuration
     */
    applyThemeColors(filterControl, themeColors) {
        if (themeColors.states) {
            // Apply state-specific colors
            Object.keys(themeColors.states).forEach(state => {
                const stateColors = themeColors.states[state];
                
                if (stateColors.border2) {
                    filterControl.setBorderColor('border2', stateColors.border2);
                }
                
                if (stateColors.text) {
                    filterControl.setTextColor(state, stateColors.text);
                }
            });
        }
    }
    
    /**
     * Apply global colors to FilterControl
     * @param {FilterControl} filterControl - FilterControl instance
     */
    applyGlobalColors(filterControl) {
        const colors = this.colorScheme.colors;
        
        // Apply border colors
        if (colors.active_border) {
            filterControl.setBorderColor('border2', colors.active_border);
        }
        
        // Apply text colors
        if (colors.active_text) {
            filterControl.setTextColor('active', colors.active_text);
        }
        if (colors.inactive_text) {
            filterControl.setTextColor('inactive', colors.inactive_text);
        }
        if (colors.disabled_text) {
            filterControl.setTextColor('disabled', colors.disabled_text);
        }
    }
    
    /**
     * Apply styling configuration to FilterControl
     * @param {FilterControl} filterControl - FilterControl instance
     */
    applyStyling(filterControl) {
        const styling = this.colorScheme.styling;
        
        if (styling.border_width) {
            filterControl.options.borderWidth = styling.border_width;
        }
        
        if (styling.border_radius) {
            filterControl.container.style.borderRadius = styling.border_radius;
        }
        
        if (styling.padding) {
            filterControl.container.style.padding = styling.padding;
        }
    }
    
    /**
     * Apply icon colors to FilterControl
     * @param {FilterControl} filterControl - FilterControl instance
     */
    applyIconColors(filterControl) {
        const iconColors = this.colorScheme.icon_colors;
        const currentState = filterControl.getState();
        
        if (iconColors && iconColors[currentState]) {
            const stateColors = iconColors[currentState];
            const iconElement = filterControl.container.querySelector('.icon-svg');
            
            if (iconElement) {
                // Apply icon colors
                if (stateColors.fill) {
                    iconElement.style.fill = stateColors.fill;
                }
                if (stateColors.stroke) {
                    iconElement.style.stroke = stateColors.stroke;
                }
                if (stateColors.background) {
                    iconElement.style.backgroundColor = stateColors.background;
                }
                if (stateColors.filter) {
                    iconElement.style.filter = stateColors.filter;
                }
                
                console.log(`Applied icon colors for ${currentState} state:`, stateColors);
            }
        }
    }
    
    /**
     * Apply border templates to FilterControl
     * @param {FilterControl} filterControl - FilterControl instance
     */
    applyBorderTemplates(filterControl) {
        const borderTemplates = this.colorScheme.border_templates;
        const currentState = filterControl.getState();
        
        if (borderTemplates) {
            Object.keys(borderTemplates).forEach(borderKey => {
                const borderTemplate = borderTemplates[borderKey];
                
                // Get state-specific or default values
                let borderConfig = borderTemplate.default || {};
                if (borderTemplate.states && borderTemplate.states[currentState]) {
                    borderConfig = { ...borderConfig, ...borderTemplate.states[currentState] };
                }
                
                // Apply border styling based on border type
                switch (borderKey) {
                    case 'border1':
                        // Apply dotted outline
                        if (borderConfig.color && borderConfig.width && borderConfig.style) {
                            filterControl.container.style.outline = `${borderConfig.width} ${borderConfig.style} ${borderConfig.color}`;
                            if (borderConfig.offset) {
                                filterControl.container.style.outlineOffset = borderConfig.offset;
                            }
                        }
                        break;
                        
                    case 'border2':
                        // Apply filter state border
                        if (borderConfig.color && borderConfig.width && borderConfig.style) {
                            filterControl.container.style.border = `${borderConfig.width} ${borderConfig.style} ${borderConfig.color}`;
                            if (borderConfig.radius) {
                                filterControl.container.style.borderRadius = borderConfig.radius;
                            }
                        }
                        break;
                        
                    case 'border3':
                        // Apply button border (if button exists)
                        if (filterControl.control && filterControl.control.tagName === 'BUTTON') {
                            if (borderConfig.color && borderConfig.width && borderConfig.style) {
                                filterControl.control.style.border = `${borderConfig.width} ${borderConfig.style} ${borderConfig.color}`;
                                if (borderConfig.radius) {
                                    filterControl.control.style.borderRadius = borderConfig.radius;
                                }
                            }
                        }
                        break;
                        
                    case 'border4':
                        // Apply icon border
                        const iconElement = filterControl.container.querySelector('.icon-svg');
                        if (iconElement) {
                            if (borderConfig.color && borderConfig.width && borderConfig.style) {
                                iconElement.style.border = `${borderConfig.width} ${borderConfig.style} ${borderConfig.color}`;
                                if (borderConfig.radius) {
                                    iconElement.style.borderRadius = borderConfig.radius;
                                }
                            }
                        }
                        break;
                }
            });
        }
    }
    
    /**
     * Apply area templates to FilterControl
     * @param {FilterControl} filterControl - FilterControl instance
     */
    applyAreaTemplates(filterControl) {
        const areaTemplates = this.colorScheme.area_templates;
        const currentState = filterControl.getState();
        
        if (areaTemplates) {
            Object.keys(areaTemplates).forEach(areaKey => {
                const areaTemplate = areaTemplates[areaKey];
                
                // Get state-specific or default values
                let areaConfig = areaTemplate.default || {};
                if (areaTemplate.states && areaTemplate.states[currentState]) {
                    areaConfig = { ...areaConfig, ...areaTemplate.states[currentState] };
                }
                
                // Apply area styling based on area type
                switch (areaKey) {
                    case 'areaA':
                        // Border area - apply to container
                        if (areaConfig.background) {
                            filterControl.container.style.backgroundColor = areaConfig.background;
                        }
                        if (areaConfig.padding) {
                            filterControl.container.style.padding = areaConfig.padding;
                        }
                        if (areaConfig.margin) {
                            filterControl.container.style.margin = areaConfig.margin;
                        }
                        break;
                        
                    case 'areaB':
                        // Content area - apply to container content
                        if (areaConfig.background) {
                            filterControl.container.style.backgroundColor = areaConfig.background;
                        }
                        if (areaConfig.padding) {
                            filterControl.container.style.padding = areaConfig.padding;
                        }
                        if (areaConfig.margin) {
                            filterControl.container.style.margin = areaConfig.margin;
                        }
                        break;
                        
                    case 'areaC':
                        // Button area - apply to button element
                        if (filterControl.control && filterControl.control.tagName === 'BUTTON') {
                            if (areaConfig.background) {
                                filterControl.control.style.backgroundColor = areaConfig.background;
                            }
                            if (areaConfig.padding) {
                                filterControl.control.style.padding = areaConfig.padding;
                            }
                            if (areaConfig.margin) {
                                filterControl.control.style.margin = areaConfig.margin;
                            }
                            if (areaConfig.border_radius) {
                                filterControl.control.style.borderRadius = areaConfig.border_radius;
                            }
                        }
                        break;
                        
                    case 'areaD':
                        // Icon area - apply to icon element
                        const iconElement = filterControl.container.querySelector('.icon-svg');
                        if (iconElement) {
                            if (areaConfig.background) {
                                iconElement.style.backgroundColor = areaConfig.background;
                            }
                            if (areaConfig.padding) {
                                iconElement.style.padding = areaConfig.padding;
                            }
                            if (areaConfig.margin) {
                                iconElement.style.margin = areaConfig.margin;
                            }
                            if (areaConfig.border_radius) {
                                iconElement.style.borderRadius = areaConfig.border_radius;
                            }
                        }
                        break;
                }
            });
        }
    }
    
    /**
     * Apply state templates to FilterControl (most comprehensive)
     * @param {FilterControl} filterControl - FilterControl instance
     */
    applyStateTemplates(filterControl) {
        const stateTemplates = this.colorScheme.state_templates;
        const currentState = filterControl.getState();
        
        if (stateTemplates && stateTemplates[currentState]) {
            const stateTemplate = stateTemplates[currentState];
            
            // Apply borders
            if (stateTemplate.borders) {
                Object.keys(stateTemplate.borders).forEach(borderKey => {
                    const borderColor = stateTemplate.borders[borderKey];
                    filterControl.setBorderColor(borderKey, borderColor);
                });
            }
            
            // Apply areas
            if (stateTemplate.areas) {
                Object.keys(stateTemplate.areas).forEach(areaKey => {
                    const areaColor = stateTemplate.areas[areaKey];
                    filterControl.setAreaColor(areaKey, areaColor);
                });
            }
            
            // Apply text color
            if (stateTemplate.text) {
                filterControl.setTextColor(currentState, stateTemplate.text);
            }
            
            // Apply icon styling
            if (stateTemplate.icon) {
                const iconElement = filterControl.container.querySelector('.icon-svg');
                if (iconElement) {
                    const iconConfig = stateTemplate.icon;
                    
                    if (iconConfig.fill) {
                        iconElement.style.fill = iconConfig.fill;
                    }
                    if (iconConfig.stroke) {
                        iconElement.style.stroke = iconConfig.stroke;
                    }
                    if (iconConfig.background) {
                        iconElement.style.backgroundColor = iconConfig.background;
                    }
                    if (iconConfig.filter) {
                        iconElement.style.filter = iconConfig.filter;
                    }
                }
            }
            
            console.log(`Applied state template for ${currentState}:`, stateTemplate);
        }
    }
    
    /**
     * Switch to a different theme
     * @param {string} themeName - Name of the theme to switch to
     * @param {Array<FilterControl>} filterControls - Array of FilterControl instances to update
     */
    switchTheme(themeName, filterControls = []) {
        if (!this.colorScheme || !this.colorScheme.themes || !this.colorScheme.themes[themeName]) {
            console.warn(`Theme '${themeName}' not found`);
            return;
        }
        
        this.currentTheme = themeName;
        
        // Apply theme to all filter controls
        filterControls.forEach(filterControl => {
            this.applyColorScheme(filterControl, themeName);
        });
        
        console.log(`Switched to theme: ${themeName}`);
    }
    
    /**
     * Get available themes
     * @returns {Array<string>} - Array of available theme names
     */
    getAvailableThemes() {
        if (!this.colorScheme || !this.colorScheme.themes) {
            return ['default'];
        }
        return Object.keys(this.colorScheme.themes);
    }
    
    /**
     * Get current theme
     * @returns {string} - Current theme name
     */
    getCurrentTheme() {
        return this.currentTheme;
    }
}

// Export for use in other files
window.ColorSchemeLoader = ColorSchemeLoader;

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', async () => {
    window.colorSchemeLoader = new ColorSchemeLoader();
    await window.colorSchemeLoader.loadColorScheme();
    console.log('ColorSchemeLoader initialized and ready!');
});
