/**
 * Color Scheme Demo
 * Shows how to use the ColorSchemeLoader with colorscheme.yaml
 */

// Example 1: Basic usage with ColorSchemeLoader
async function demoBasicUsage() {
    console.log('=== Basic Color Scheme Usage ===');
    
    // Wait for ColorSchemeLoader to be ready
    if (!window.colorSchemeLoader) {
        console.log('Waiting for ColorSchemeLoader...');
        await new Promise(resolve => {
            const checkLoader = () => {
                if (window.colorSchemeLoader) {
                    resolve();
                } else {
                    setTimeout(checkLoader, 100);
                }
            };
            checkLoader();
        });
    }
    
    const loader = window.colorSchemeLoader;
    
    // Show available themes
    const themes = loader.getAvailableThemes();
    console.log('Available themes:', themes);
    
    // Show current theme
    const currentTheme = loader.getCurrentTheme();
    console.log('Current theme:', currentTheme);
    
    // Get color scheme data
    const colorScheme = loader.colorScheme;
    console.log('Loaded color scheme:', colorScheme);
    
    return { loader, themes, currentTheme, colorScheme };
}

// Example 2: Apply color scheme to FilterControl
function demoApplyColorScheme() {
    console.log('=== Applying Color Scheme to FilterControl ===');
    
    const filterControl = new FilterControl(document.querySelector('.filter-wrapper'), 'demo');
    
    // Apply default theme
    window.colorSchemeLoader.applyColorScheme(filterControl, 'default');
    
    // Show the styled filter control
    console.log('FilterControl styled with default theme');
    
    return filterControl;
}

// Example 3: Theme switching
async function demoThemeSwitching() {
    console.log('=== Theme Switching Demo ===');
    
    const { loader } = await demoBasicUsage();
    const filterControl = demoApplyColorScheme();
    
    // Switch to different themes
    const themes = ['default', 'dark', 'pastel', 'high_contrast'];
    
    for (const theme of themes) {
        console.log(`Switching to theme: ${theme}`);
        loader.switchTheme(theme, [filterControl]);
        
        // Wait a bit to see the change
        await new Promise(resolve => setTimeout(resolve, 2000));
    }
    
    // Return to default theme
    loader.switchTheme('default', [filterControl]);
    console.log('Returned to default theme');
}

// Example 4: Custom color scheme application
function demoCustomColors() {
    console.log('=== Custom Color Application ===');
    
    const filterControl = new FilterControl(document.querySelector('.filter-wrapper'), 'custom');
    
    // Apply specific colors from the YAML
    if (window.colorSchemeLoader && window.colorSchemeLoader.colorScheme) {
        const scheme = window.colorSchemeLoader.colorScheme;
        
        // Apply specific border colors
        if (scheme.borders) {
            filterControl.setBorderColors(scheme.borders);
        }
        
        // Apply specific area colors
        if (scheme.areas) {
            filterControl.setAreaColors(scheme.areas);
        }
        
        // Apply specific text colors
        if (scheme.colors) {
            filterControl.setTextColors({
                active: scheme.colors.active_text || '#ffffff',
                inactive: scheme.colors.inactive_text || '#495057',
                disabled: scheme.colors.disabled_text || '#6c757d'
            });
        }
        
        console.log('Applied custom colors from YAML');
    }
    
    return filterControl;
}

// Example 5: Dynamic theme switching with UI
function createThemeSwitcher() {
    console.log('=== Creating Theme Switcher UI ===');
    
    // Create theme switcher dropdown
    const switcher = document.createElement('div');
    switcher.innerHTML = `
        <div style="position: fixed; top: 20px; right: 20px; z-index: 1000; background: white; padding: 10px; border: 1px solid #ccc; border-radius: 5px;">
            <label for="theme-select">Theme: </label>
            <select id="theme-select" style="margin-left: 10px;">
                <option value="default">Default</option>
                <option value="dark">Dark</option>
                <option value="pastel">Pastel</option>
                <option value="high_contrast">High Contrast</option>
            </select>
            <button id="apply-theme" style="margin-left: 10px;">Apply</button>
        </div>
    `;
    
    document.body.appendChild(switcher);
    
    // Add event listeners
    const themeSelect = document.getElementById('theme-select');
    const applyButton = document.getElementById('apply-theme');
    
    applyButton.addEventListener('click', () => {
        const selectedTheme = themeSelect.value;
        console.log(`Applying theme: ${selectedTheme}`);
        
        // Get all filter controls on the page
        const filterControls = Array.from(document.querySelectorAll('.filter-wrapper'))
            .map(wrapper => wrapper.filterControl)
            .filter(Boolean);
        
        if (window.colorSchemeLoader) {
            window.colorSchemeLoader.switchTheme(selectedTheme, filterControls);
        }
    });
    
    console.log('Theme switcher created in top-right corner');
    return switcher;
}

// Example 6: Export current color scheme
function exportCurrentColorScheme() {
    console.log('=== Exporting Current Color Scheme ===');
    
    if (!window.colorSchemeLoader || !window.colorSchemeLoader.colorScheme) {
        console.log('No color scheme loaded');
        return null;
    }
    
    const scheme = window.colorSchemeLoader.colorScheme;
    const currentTheme = window.colorSchemeLoader.getCurrentTheme();
    
    const exportData = {
        timestamp: new Date().toISOString(),
        currentTheme: currentTheme,
        colorScheme: scheme
    };
    
    // Create downloadable file
    const dataStr = JSON.stringify(exportData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = `colorscheme-${currentTheme}-${Date.now()}.json`;
    link.click();
    
    console.log('Color scheme exported as JSON file');
    return exportData;
}

// Export all demo functions
window.ColorSchemeDemo = {
    demoBasicUsage,
    demoApplyColorScheme,
    demoThemeSwitching,
    demoCustomColors,
    createThemeSwitcher,
    exportCurrentColorScheme
};

// Auto-run basic demo when page loads
document.addEventListener('DOMContentLoaded', async () => {
    console.log('ColorSchemeDemo loaded!');
    console.log('Available functions:', Object.keys(window.ColorSchemeDemo));
    
    // Wait a bit for ColorSchemeLoader to initialize
    setTimeout(async () => {
        try {
            await demoBasicUsage();
            console.log('Basic demo completed successfully!');
        } catch (error) {
            console.error('Demo error:', error);
        }
    }, 1000);
});
