/**
 * Filter Control Color Configuration Demo
 * Shows how to use the new color configuration functions
 */

// Example 1: Basic color configuration
function configureBasicColors() {
    const filterControl = new FilterControl(document.querySelector('.filter-wrapper'), 'example');
    
    // Set all border colors at once
    filterControl.setBorderColors({
        border1: '#333',           // Dotted outline (black)
        border2: '#ff6b6b',        // Filter state border (red)
        border3: '#4ecdc4',        // Button border (teal)
        border4: '#45b7d1'         // Icon border (blue)
    });
    
    // Set all area colors at once
    filterControl.setAreaColors({
        areaA: 'rgba(255,0,0,0.1)',    // Border area (red)
        areaB: 'rgba(0,255,0,0.1)',    // Content area (green)
        areaC: 'rgba(255,255,0,0.1)',  // Button area (yellow)
        areaD: 'rgba(0,0,255,0.1)'     // Icon area (blue)
    });
}

// Example 2: Individual color configuration
function configureIndividualColors() {
    const filterControl = new FilterControl(document.querySelector('.filter-wrapper'), 'example');
    
    // Set individual border colors
    filterControl.setBorderColor('border1', '#000000');      // Black dotted outline
    filterControl.setBorderColor('border2', '#ff8c00');      // Orange filter state
    filterControl.setBorderColor('border3', '#28a745');      // Green button
    filterControl.setBorderColor('border4', '#007bff');      // Blue icon
    
    // Set individual area colors
    filterControl.setAreaColor('areaA', 'rgba(0,0,0,0.1)');     // Black border area
    filterControl.setAreaColor('areaB', 'rgba(255,140,0,0.1)'); // Orange content area
    filterControl.setAreaColor('areaC', 'rgba(40,167,69,0.1)'); // Green button area
    filterControl.setAreaColor('areaD', 'rgba(0,123,255,0.1)'); // Blue icon area
}

// Example 3: Dynamic color changes based on state
function configureDynamicColors() {
    const filterControl = new FilterControl(document.querySelector('.filter-wrapper'), 'example');
    
    // Configure colors for different states
    const stateColors = {
        active: {
            border2: '#28a745',    // Green for active
            areaB: 'rgba(40,167,69,0.15)'
        },
        inactive: {
            border2: '#ff8c00',    // Orange for inactive
            areaB: 'rgba(255,140,0,0.1)'
        },
        disabled: {
            border2: '#6c757d',    // Grey for disabled
            areaB: 'rgba(108,117,125,0.1)'
        }
    };
    
    // Apply colors based on current state
    function updateColorsForState(state) {
        if (stateColors[state]) {
            filterControl.setBorderColor('border2', stateColors[state].border2);
            filterControl.setAreaColor('areaB', stateColors[state].areaB);
        }
    }
    
    // Example usage
    updateColorsForState('inactive');  // Set orange colors
    updateColorsForState('active');    // Set green colors
    updateColorsForState('disabled');  // Set grey colors
}

// Example 4: Theme-based color configuration
function configureThemeColors(theme = 'default') {
    const filterControl = new FilterControl(document.querySelector('.filter-wrapper'), 'example');
    
    const themes = {
        default: {
            borderColors: {
                border1: '#333',
                border2: '#ff8c00',
                border3: '#4ecdc4',
                border4: '#45b7d1'
            },
            areaColors: {
                areaA: 'rgba(255,0,0,0.1)',
                areaB: 'rgba(0,255,0,0.1)',
                areaC: 'rgba(255,255,0,0.1)',
                areaD: 'rgba(0,0,255,0.1)'
            }
        },
        dark: {
            borderColors: {
                border1: '#666',
                border2: '#ff6b6b',
                border3: '#4ecdc4',
                border4: '#45b7d1'
            },
            areaColors: {
                areaA: 'rgba(255,107,107,0.2)',
                areaB: 'rgba(78,205,196,0.2)',
                areaC: 'rgba(69,183,209,0.2)',
                areaD: 'rgba(255,107,107,0.2)'
            }
        },
        pastel: {
            borderColors: {
                border1: '#999',
                border2: '#ffb3ba',
                border3: '#baffc9',
                border4: '#b3d9ff'
            },
            areaColors: {
                areaA: 'rgba(255,179,186,0.2)',
                areaB: 'rgba(186,255,201,0.2)',
                areaC: 'rgba(179,217,255,0.2)',
                areaD: 'rgba(255,179,186,0.2)'
            }
        }
    };
    
    if (themes[theme]) {
        filterControl.setBorderColors(themes[theme].borderColors);
        filterControl.setAreaColors(themes[theme].areaColors);
    }
}

// Example 5: Get current color configuration
function showCurrentColors() {
    const filterControl = new FilterControl(document.querySelector('.filter-wrapper'), 'example');
    
    console.log('Current Border Colors:', filterControl.getBorderColors());
    console.log('Current Area Colors:', filterControl.getAreaColors());
    console.log('Current Text Colors:', filterControl.getTextColors());
    
    // Example output:
    // Current Border Colors: {border1: "#333", border2: "#ff8c00", border3: "#4ecdc4", border4: "#45b7d1"}
    // Current Area Colors: {areaA: "rgba(255,0,0,0.1)", areaB: "rgba(0,255,0,0.1)", areaC: "rgba(255,255,0,0.1)", areaD: "rgba(0,0,255,0.1)"}
    // Current Text Colors: {active: "#ffffff", inactive: "#495057", disabled: "#6c757d"}
}

// Example 6: Text color configuration
function configureTextColors() {
    const filterControl = new FilterControl(document.querySelector('.filter-wrapper'), 'example');
    
    // Set all text colors at once
    filterControl.setTextColors({
        active: '#ffffff',       // White text for active
        inactive: '#6c757d',     // Medium grey text for inactive
        disabled: '#adb5bd'      // Light grey text for disabled
    });
}

// Example 7: Individual text color configuration
function configureIndividualTextColors() {
    const filterControl = new FilterControl(document.querySelector('.filter-wrapper'), 'example');
    
    // Set individual text colors
    filterControl.setTextColor('active', '#ffffff');      // White for active
    filterControl.setTextColor('inactive', '#495057');    // Dark grey for inactive
    filterControl.setTextColor('disabled', '#6c757d');    // Medium grey for disabled
}

// Example 8: Different text and border colors
function configureDifferentTextAndBorderColors() {
    const filterControl = new FilterControl(document.querySelector('.filter-wrapper'), 'example');
    
    // Set border colors
    filterControl.setBorderColors({
        border1: '#333',         // Black dotted outline
        border2: '#ff8c00',      // Orange filter state border
        border3: '#4ecdc4',      // Teal button border
        border4: '#45b7d1'       // Blue icon border
    });
    
    // Set different text colors (independent from borders)
    filterControl.setTextColors({
        active: '#ffffff',       // White text (contrasts with orange border)
        inactive: '#495057',     // Dark grey text (contrasts with grey border)
        disabled: '#adb5bd'      // Light grey text (contrasts with light grey border)
    });
    
    // Now you can have:
    // - Active: Orange border with white text
    // - Inactive: Grey border with dark grey text
    // - Disabled: Light grey border with light grey text
}

// Export functions for use in other files
window.FilterControlDemo = {
    configureBasicColors,
    configureIndividualColors,
    configureDynamicColors,
    configureThemeColors,
    showCurrentColors,
    configureTextColors,
    configureIndividualTextColors,
    configureDifferentTextAndBorderColors
};

console.log('FilterControl Color Demo loaded! Use FilterControlDemo.configureBasicColors() to start.');
