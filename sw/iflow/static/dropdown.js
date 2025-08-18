// Dropdown Management System
// This file contains all custom dropdown functionality for the iflow application

class CustomDropdownManager {
    // CSS Constants
    static CSS = {
        DROPDOWN_CONTAINER: `
            position: relative;
            display: inline-block;
            width: 100%;
            font-family: inherit;
        `,
        DROPDOWN_BUTTON: `
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 12px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            background-color: white;
            cursor: pointer;
            user-select: none;
            min-height: 38px;
        `,
        DROPDOWN_ARROW: `
            font-size: 12px;
            color: #6b7280;
            margin-left: 8px;
            transition: transform 0.2s;
        `,
        OPTIONS_CONTAINER: `
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background-color: white;
            border: 1px solid #d1d5db;
            border-top: none;
            border-radius: 0 0 6px 6px;
            max-height: 200px;
            overflow-y: auto;
            z-index: 1000;
            display: none;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        `,
        DROPDOWN_OPTION: `
            padding: 8px 12px;
            cursor: pointer;
            border-bottom: 1px solid #f3f4f6;
            line-height: 1.2;
        `
    };

    constructor() {
        this.workItemTypes = [];
        this.artifactStatuses = [];
        this.dropdowns = new Map(); // Store references to created dropdowns
        this.activeDropdown = null; // Track currently open dropdown
        this.isInitialized = false;
        
        // Bind methods to preserve 'this' context
        this.handleDocumentClick = this.handleDocumentClick.bind(this);
        this.handleDropdownToggle = this.handleDropdownToggle.bind(this);
        this.handleOptionSelect = this.handleOptionSelect.bind(this);
        
        // Initialize event listeners
        this.initEventListeners();
    }
    
    // Initialize event listeners
    initEventListeners() {
        // Add document click listener to close dropdowns when clicking outside
        document.addEventListener('click', this.handleDocumentClick);
    }
    
    // Handle document clicks to close dropdowns
    handleDocumentClick(event) {
        if (this.activeDropdown && !this.activeDropdown.contains(event.target)) {
            this.closeAllDropdowns();
        }
    }
    
    // Handle dropdown toggle (open/close)
    handleDropdownToggle(dropdownElement) {
        if (this.activeDropdown === dropdownElement) {
            // Close this dropdown
            this.closeAllDropdowns();
        } else {
            // Close any other open dropdown
            this.closeAllDropdowns();
            
            // Open this dropdown
            const optionsContainer = dropdownElement.querySelector('.custom-dropdown-options');
            if (optionsContainer) {
                optionsContainer.style.display = 'block';
                this.activeDropdown = dropdownElement;
            }
        }
    }
    
    // Handle option selection
    handleOptionSelect(dropdownElement, optionElement) {
        console.log('=== handleOptionSelect called ===');
        console.log('dropdownElement:', dropdownElement);
        console.log('optionElement:', optionElement);
        
        const value = optionElement.getAttribute('data-value');
        const originalSelect = dropdownElement._originalSelect;
        
        console.log('Selected value:', value);
        console.log('Original select element:', originalSelect);
        
        if (originalSelect) {
            originalSelect.value = value;
            console.log('Set originalSelect.value to:', value);
            // Trigger change event on the original select
            const event = new Event('change', { bubbles: true });
            originalSelect.dispatchEvent(event);
            console.log('Dispatched change event on originalSelect');
        } else {
            console.error('No original select element found!');
        }
        
        // Update the visual display
        const displayUpdated = this.setCustomDropdownValue(dropdownElement, value);
        console.log('Display update result:', displayUpdated);
        
        // Close the dropdown
        this.closeAllDropdowns();
        console.log('=== handleOptionSelect completed ===');
    }

    // Initialize dropdown data
    initializeData(workItemTypes, artifactStatuses) {
        // Validate input data
        if (!Array.isArray(workItemTypes) || !Array.isArray(artifactStatuses)) {
            console.error('Invalid data provided to initializeData');
            return false;
        }
        
        // Store the data
        this.workItemTypes = [...workItemTypes];
        this.artifactStatuses = [...artifactStatuses];
        
        // Mark as initialized
        this.isInitialized = true;
        
        // Log initialization
        console.log(`DropdownManager initialized with ${this.workItemTypes.length} work item types and ${this.artifactStatuses.length} artifact statuses`);
        
        return true;
    }

    // Create all custom dropdowns
    createCustomDropdowns() {
        if (!this.isInitialized) {
            console.error('DropdownManager not initialized. Call initializeData() first.');
            return false;
        }
        
        try {
            // Find all select elements that need custom dropdowns
            const typeFilter = document.getElementById('typeFilter');
            const statusFilter = document.getElementById('statusFilter');
            const artifactTypeSelect = document.getElementById('artifactType');
            const artifactStatusSelect = document.getElementById('artifactStatus');
            
            // Create custom dropdowns for filters
            if (typeFilter) {
                this.createCustomDropdown(typeFilter, 'type', this.workItemTypes);
            }
            
            if (statusFilter) {
                this.createCustomDropdown(statusFilter, 'status', this.artifactStatuses);
            }
            
            // Create custom dropdowns for forms
            if (artifactTypeSelect) {
                this.createCustomDropdown(artifactTypeSelect, 'form', this.workItemTypes);
            }
            
            if (artifactStatusSelect) {
                this.createCustomDropdown(artifactStatusSelect, 'status-form', this.artifactStatuses);
            }
            
            // Set up event handling for all created dropdowns
            this.dropdowns.forEach((customDropdown, selectId) => {
                this.handleDropdownEvents(customDropdown);
            });
            
            console.log(`Created ${this.dropdowns.size} custom dropdowns`);
            return true;
            
        } catch (error) {
            console.error('Error creating custom dropdowns:', error);
            return false;
        }
    }

    // Create a single custom dropdown
    createCustomDropdown(originalSelect, type, items) {
        // Validate inputs
        if (!originalSelect || !type || !Array.isArray(items)) {
            console.error('Invalid parameters for createCustomDropdown');
            return null;
        }
        
        // Create the custom dropdown container
        const customDropdown = document.createElement('div');
        customDropdown.className = 'custom-dropdown';
        
        // Set width based on dropdown type - filters should maintain original width
        let containerWidth = '100%';
        if (type === 'type' || type === 'status') {
            // Filter dropdowns - use original select width
            const originalWidth = originalSelect.offsetWidth;
            if (originalWidth > 0) {
                containerWidth = originalWidth + 'px';
            } else {
                // Fallback width for filter dropdowns
                containerWidth = '180px';
            }
        }
        
        customDropdown.style.cssText = CustomDropdownManager.CSS.DROPDOWN_CONTAINER.replace('width: 100%', `width: ${containerWidth}`);
        
        // Add additional styling for filter dropdowns
        if (type === 'type' || type === 'status') {
            customDropdown.style.minWidth = '150px';
            customDropdown.style.maxWidth = '250px';
        }
        
        // Create the dropdown button
        const dropdownButton = document.createElement('div');
        dropdownButton.className = 'custom-dropdown-button';
        dropdownButton.style.cssText = CustomDropdownManager.CSS.DROPDOWN_BUTTON;
        
        // Create the selected value display
        const selectedValue = document.createElement('span');
        selectedValue.className = 'custom-dropdown-selected';
        selectedValue.textContent = this.getDefaultText(type);
        
        // Create the dropdown arrow
        const arrow = document.createElement('span');
        arrow.textContent = '▼';
        arrow.style.cssText = CustomDropdownManager.CSS.DROPDOWN_ARROW;
        
        // Create the options container
        const optionsContainer = document.createElement('div');
        optionsContainer.className = 'custom-dropdown-options';
        optionsContainer.style.cssText = CustomDropdownManager.CSS.OPTIONS_CONTAINER;
        
        // Add default option
        const defaultOption = document.createElement('div');
        defaultOption.className = 'custom-dropdown-option';
        defaultOption.style.cssText = CustomDropdownManager.CSS.DROPDOWN_OPTION;
        defaultOption.textContent = this.getDefaultText(type);
        defaultOption.setAttribute('data-value', '');
        optionsContainer.appendChild(defaultOption);
        
        // Add item options
        items.forEach(item => {
            const option = document.createElement('div');
            option.className = 'custom-dropdown-option';
            option.style.cssText = CustomDropdownManager.CSS.DROPDOWN_OPTION;
            
            if (item.icon && item.icon.startsWith('ion-')) {
                // Ionic icon
                option.innerHTML = `
                    <ion-icon name="${item.icon.replace('ion-', '')}" style="color: ${item.color}; font-size: 16px; margin-right: 8px;"></ion-icon>
                    ${item.name}
                `;
            } else if (item.icon) {
                // Emoji or other icon
                option.innerHTML = `
                    <span style="font-size: 16px; margin-right: 8px;">${item.icon}</span>
                    ${item.name}
                `;
            } else {
                option.textContent = item.name;
            }
            
            option.setAttribute('data-value', item.id);
            optionsContainer.appendChild(option);
        });
        
        // Store references for external access
        customDropdown._originalSelect = originalSelect;
        customDropdown._selectedValue = selectedValue;
        customDropdown._items = items;
        customDropdown._type = type;
        
        // Assemble the dropdown
        dropdownButton.appendChild(selectedValue);
        dropdownButton.appendChild(arrow);
        customDropdown.appendChild(dropdownButton);
        customDropdown.appendChild(optionsContainer);
        
        // Replace the original select
        originalSelect.style.display = 'none';
        originalSelect.parentNode.insertBefore(customDropdown, originalSelect);
        
        // Store reference in the manager
        this.dropdowns.set(originalSelect.id, customDropdown);
        
        return customDropdown;
    }

    // Set value on a custom dropdown programmatically
    setCustomDropdownValue(dropdownElement, value) {
        // Validate inputs
        if (!dropdownElement || !dropdownElement._selectedValue || !dropdownElement._items) {
            console.error('Invalid dropdown element or missing required properties');
            return false;
        }
        
        const selectedValue = dropdownElement._selectedValue;
        const items = dropdownElement._items;
        const type = dropdownElement._type;
        
        // Update the original select element
        if (dropdownElement._originalSelect) {
            dropdownElement._originalSelect.value = value;
        }
        
        // Update the visual display
        if (value === '') {
            selectedValue.textContent = this.getDefaultText(type);
        } else {
            // Validate the selection before updating
            const validation = this.validateDropdownSelection(dropdownElement, value);
            if (!validation.isValid) {
                console.error('Invalid dropdown selection:', validation.error);
                return false;
            }
            
            const item = validation.item;
            selectedValue.innerHTML = '';
            
            if (item.icon && item.icon.startsWith('ion-')) {
                // Ionic icon - reuse the same icon creation logic
                const icon = document.createElement('ion-icon');
                icon.setAttribute('name', item.icon.replace('ion-', ''));
                icon.style.fontSize = '16px';
                icon.style.color = item.color;
                selectedValue.appendChild(icon);
            } else if (item.icon) {
                // Emoji or other icon - reuse the same icon creation logic
                const iconSpan = document.createElement('span');
                iconSpan.textContent = item.icon;
                iconSpan.style.fontSize = '16px';
                selectedValue.appendChild(iconSpan);
            }
            
            // Add the name text - reuse the same pattern
            const nameSpan = document.createElement('span');
            nameSpan.textContent = ` ${item.name}`;
            selectedValue.appendChild(nameSpan);
        }
        
        return true;
    }

    // Update dropdown options when data changes
    updateDropdownOptions() {
        // Check if data is initialized
        if (!this.isInitialized) {
            console.error('DropdownManager not initialized. Call initializeData() first.');
            return false;
        }
        
        try {
            // Update each existing dropdown with new data
            this.dropdowns.forEach((customDropdown, selectId) => {
                const originalSelect = customDropdown._originalSelect;
                const type = customDropdown._type;
                
                if (originalSelect && type) {
                    // Determine which data to use based on dropdown type
                    let items = [];
                    if (type === 'type' || type === 'form') {
                        items = this.workItemTypes;
                    } else if (type === 'status' || type === 'status-form') {
                        items = this.artifactStatuses;
                    }
                    
                    // Clear existing options container
                    const optionsContainer = customDropdown.querySelector('.custom-dropdown-options');
                    if (optionsContainer) {
                        optionsContainer.innerHTML = '';
                        
                        // Add default option
                        const defaultOption = document.createElement('div');
                        defaultOption.className = 'custom-dropdown-option';
                        defaultOption.style.cssText = CustomDropdownManager.CSS.DROPDOWN_OPTION;
                        defaultOption.textContent = this.getDefaultText(type);
                        defaultOption.setAttribute('data-value', '');
                        optionsContainer.appendChild(defaultOption);
                        
                        // Add updated item options
                        items.forEach(item => {
                            const option = document.createElement('div');
                            option.className = 'custom-dropdown-option';
                            option.style.cssText = CustomDropdownManager.CSS.DROPDOWN_OPTION;
                            
                            if (item.icon && item.icon.startsWith('ion-')) {
                                // Ionic icon - reuse existing icon creation logic
                                option.innerHTML = `
                                    <ion-icon name="${item.icon.replace('ion-', '')}" style="color: ${item.color}; font-size: 16px; margin-right: 8px;"></ion-icon>
                                    ${item.name}
                                `;
                            } else if (item.icon) {
                                // Emoji or other icon - reuse existing icon creation logic
                                option.innerHTML = `
                                    <span style="font-size: 16px; margin-right: 8px;">${item.icon}</span>
                                    ${item.name}
                                `;
                            } else {
                                option.textContent = item.name;
                            }
                            
                            option.setAttribute('data-value', item.id);
                            optionsContainer.appendChild(option);
                        });
                        
                        // Update the items reference
                        customDropdown._items = items;
                        
                        // Re-add hover effects
                        const options = optionsContainer.querySelectorAll('.custom-dropdown-option');
                        options.forEach(option => {
                            option.addEventListener('mouseenter', () => {
                                option.style.backgroundColor = '#f3f4f6';
                            });
                            option.addEventListener('mouseleave', () => {
                                option.style.backgroundColor = 'white';
                            });
                        });
                    }
                }
            });
            
            console.log('All dropdown options updated successfully');
            return true;
            
        } catch (error) {
            console.error('Error updating dropdown options:', error);
            return false;
        }
    }

    // Handle dropdown state changes
    handleDropdownStateChange() {
        // Check if any dropdowns exist
        if (this.dropdowns.size === 0) {
            return;
        }
        
        try {
            // Update dropdown states based on current data
            this.dropdowns.forEach((customDropdown, selectId) => {
                const type = customDropdown._type;
                const selectedValue = customDropdown._selectedValue;
                const originalSelect = customDropdown._originalSelect;
                
                if (type && selectedValue && originalSelect) {
                    const currentValue = originalSelect.value;
                    
                    // Update visual state based on current value
                    if (currentValue === '') {
                        // Reset to default state
                        selectedValue.textContent = this.getDefaultText(type);
                        selectedValue.innerHTML = this.getDefaultText(type);
                    } else {
                        // Find current item and update display
                        let items = [];
                        if (type === 'type' || type === 'form') {
                            items = this.workItemTypes;
                        } else if (type === 'status' || type === 'status-form') {
                            items = this.artifactStatuses;
                        }
                        
                        // Validate current selection
                        const validation = this.validateDropdownSelection(customDropdown, currentValue);
                        if (validation.isValid && validation.item) {
                            // Update with current item data
                            this.setDropdownValue(customDropdown, currentValue);
                        } else {
                            // Current value not found or invalid, reset to default
                            console.warn(`Current value '${currentValue}' validation failed: ${validation.error}, resetting to default`);
                            this.setDropdownValue(customDropdown, '');
                        }
                    }
                    
                    // Update disabled state based on data availability
                    const hasItems = (type === 'type' || type === 'form') ? 
                        this.workItemTypes.length > 0 : 
                        this.artifactStatuses.length > 0;
                    
                    const dropdownButton = customDropdown.querySelector('.custom-dropdown-button');
                    if (dropdownButton) {
                        dropdownButton.style.opacity = hasItems ? '1' : '0.5';
                        dropdownButton.style.cursor = hasItems ? 'pointer' : 'not-allowed';
                        dropdownButton.style.pointerEvents = hasItems ? 'auto' : 'none';
                    }
                }
            });
            
            console.log('Dropdown states updated successfully');
            
        } catch (error) {
            console.error('Error handling dropdown state changes:', error);
        }
    }

    // Close all open dropdowns
    closeAllDropdowns() {
        if (this.activeDropdown) {
            const optionsContainer = this.activeDropdown.querySelector('.custom-dropdown-options');
            if (optionsContainer) {
                optionsContainer.style.display = 'none';
            }
            this.activeDropdown = null;
        }
    }

    // JavaScript accessibility functions for testing (Ticket #00073)
    
    /**
     * Get the current selected value of a dropdown
     * @param {string} selectId - The ID of the original select element
     * @returns {string|null} The current selected value or null if not found
     */
    getDropdownValue(selectId) {
        const originalSelect = document.getElementById(selectId);
        if (!originalSelect) {
            console.warn(`Dropdown with ID '${selectId}' not found`);
            return null;
        }
        
        const value = originalSelect.value;
        console.log(`getDropdownValue('${selectId}') = '${value}'`);
        return value;
    }
    
    /**
     * Set the value of a dropdown programmatically
     * @param {string} selectId - The ID of the original select element
     * @param {string} value - The value to set
     * @returns {boolean} True if successful, false otherwise
     */
    setDropdownValue(selectId, value) {
        const originalSelect = document.getElementById(selectId);
        if (!originalSelect) {
            console.warn(`Dropdown with ID '${selectId}' not found`);
            return false;
        }
        
        // Check if the value is valid for this select
        const option = originalSelect.querySelector(`option[value="${value}"]`);
        if (!option) {
            console.warn(`Value '${value}' is not a valid option for dropdown '${selectId}'`);
            return false;
        }
        
        // Set the value on the original select
        originalSelect.value = value;
        
        // Trigger change event
        const event = new Event('change', { bubbles: true });
        originalSelect.dispatchEvent(event);
        
        // Update the custom dropdown visual display
        const customDropdown = this.dropdowns.get(selectId);
        if (customDropdown) {
            this.setCustomDropdownValue(customDropdown, value);
        }
        
        console.log(`setDropdownValue('${selectId}', '${value}') = true`);
        return true;
    }
    
    /**
     * Get all available options for a dropdown
     * @param {string} selectId - The ID of the original select element
     * @returns {Array} Array of option values
     */
    getDropdownOptions(selectId) {
        const originalSelect = document.getElementById(selectId);
        if (!originalSelect) {
            console.warn(`Dropdown with ID '${selectId}' not found`);
            return [];
        }
        
        const options = Array.from(originalSelect.options).map(option => option.value);
        console.log(`getDropdownOptions('${selectId}') = [${options.join(', ')}]`);
        return options;
    }
    
    /**
     * Check if a dropdown is open
     * @param {string} selectId - The ID of the original select element
     * @returns {boolean} True if dropdown is open, false otherwise
     */
    isDropdownOpen(selectId) {
        const customDropdown = this.dropdowns.get(selectId);
        if (!customDropdown) {
            return false;
        }
        
        const optionsContainer = customDropdown.querySelector('.custom-dropdown-options');
        return optionsContainer && optionsContainer.style.display === 'block';
    }
    
    /**
     * Open a dropdown programmatically
     * @param {string} selectId - The ID of the original select element
     * @returns {boolean} True if successful, false otherwise
     */
    openDropdown(selectId) {
        const customDropdown = this.dropdowns.get(selectId);
        if (!customDropdown) {
            console.warn(`Custom dropdown for '${selectId}' not found`);
            return false;
        }
        
        this.handleDropdownToggle(customDropdown);
        return true;
    }
    
    /**
     * Close a dropdown programmatically
     * @param {string} selectId - The ID of the original select element
     * @returns {boolean} True if successful, false otherwise
     */
    closeDropdown(selectId) {
        const customDropdown = this.dropdowns.get(selectId);
        if (!customDropdown) {
            return false;
        }
        
        if (this.activeDropdown === customDropdown) {
            this.closeAllDropdowns();
        }
        return true;
    }
    
    /**
     * Get the display text of the currently selected option
     * @param {string} selectId - The ID of the original select element
     * @returns {string|null} The display text or null if not found
     */
    getDropdownDisplayText(selectId) {
        const originalSelect = document.getElementById(selectId);
        if (!originalSelect) {
            return null;
        }
        
        const selectedOption = originalSelect.options[originalSelect.selectedIndex];
        return selectedOption ? selectedOption.textContent : null;
    }
    
    /**
     * Expose the dropdown manager globally for testing access
     */
    exposeForTesting() {
        // Make the dropdown manager available globally for testing
        window.dropdownManager = this;
        
        // Also expose individual functions for easier access
        window.getDropdownValue = (selectId) => this.getDropdownValue(selectId);
        window.setDropdownValue = (selectId, value) => this.setDropdownValue(selectId, value);
        window.getDropdownOptions = (selectId) => this.getDropdownOptions(selectId);
        window.isDropdownOpen = (selectId) => this.isDropdownOpen(selectId);
        window.openDropdown = (selectId) => this.openDropdown(selectId);
        window.closeDropdown = (selectId) => this.closeDropdown(selectId);
        window.getDropdownDisplayText = (selectId) => this.getDropdownDisplayText(selectId);
        
        console.log('Dropdown accessibility functions exposed globally for testing');
    }
    
    // Get all dropdown values as an object
    getAllDropdownValues() {
        const values = {};
        
        this.dropdowns.forEach((customDropdown, selectId) => {
            values[selectId] = this.getDropdownValue(selectId);
        });
        
        return values;
    }
    
    // Set multiple dropdown values at once
    setMultipleDropdownValues(valuesObject) {
        let success = true;
        
        Object.entries(valuesObject).forEach(([selectId, value]) => {
            const customDropdown = this.dropdowns.get(selectId);
            if (customDropdown) {
                if (!this.setDropdownValue(selectId, value)) {
                    success = false;
                }
            } else {
                console.warn(`Dropdown with id '${selectId}' not found`);
                success = false;
            }
        });
        
        return success;
    }

    // Validate dropdown selection
    validateDropdownSelection(dropdownElement, value) {
        // Validate dropdown element
        if (!dropdownElement || !dropdownElement._items || !dropdownElement._type) {
            console.error('Invalid dropdown element for validation');
            return { isValid: false, error: 'Invalid dropdown element' };
        }
        
        const items = dropdownElement._items;
        const type = dropdownElement._type;
        
        // Check if value is empty (default option)
        if (value === '') {
            return { isValid: true, error: null, item: null };
        }
        
        // Find the item with the given value
        const selectedItem = items.find(item => item.id === value);
        
        if (!selectedItem) {
            return { 
                isValid: false, 
                error: `Value '${value}' not found in ${type} dropdown items`,
                item: null 
            };
        }
        
        // Validate item properties
        const validationResult = this.validateItemProperties(selectedItem, type);
        
        return {
            isValid: validationResult.isValid,
            error: validationResult.error,
            item: selectedItem
        };
    }
    
    // Helper method to validate item properties
    validateItemProperties(item, type) {
        // Check required properties
        if (!item.id || !item.name) {
            return { isValid: false, error: 'Item missing required properties (id or name)' };
        }
        
        // Type-specific validation
        if (type === 'type' || type === 'form') {
            // Work item type validation
            if (!item.color) {
                return { isValid: false, error: 'Work item type missing color property' };
            }
        } else if (type === 'status' || type === 'status-form') {
            // Status validation
            if (!item.color) {
                return { isValid: false, error: 'Status missing color property' };
            }
        }
        
        return { isValid: true, error: null };
    }

    // Refresh dropdown display
    refreshDropdownDisplay(dropdownElement) {
        if (!dropdownElement || !dropdownElement._selectedValue || !dropdownElement._originalSelect) {
            console.error('Invalid dropdown element for refresh');
            return false;
        }
        
        const currentValue = dropdownElement._originalSelect.value;
        return this.setCustomDropdownValue(dropdownElement, currentValue);
    }

    // Handle dropdown events
    handleDropdownEvents(dropdownElement) {
        if (!dropdownElement) return;
        
        const dropdownButton = dropdownElement.querySelector('.custom-dropdown-button');
        const optionsContainer = dropdownElement.querySelector('.custom-dropdown-options');
        
        if (!dropdownButton || !optionsContainer) return;
        
        // Toggle dropdown on button click
        dropdownButton.addEventListener('click', (e) => {
            e.stopPropagation();
            this.handleDropdownToggle(dropdownElement);
        });
        
        // Use event delegation for option selection - this is more reliable
        optionsContainer.addEventListener('click', (e) => {
            e.stopPropagation();
            
            // Check if the clicked element is an option
            const option = e.target.closest('.custom-dropdown-option');
            if (option) {
                this.handleOptionSelect(dropdownElement, option);
            }
        });
        
        // Add hover effects using event delegation
        optionsContainer.addEventListener('mouseover', (e) => {
            const option = e.target.closest('.custom-dropdown-option');
            if (option) {
                option.style.backgroundColor = '#f3f4f6';
            }
        });
        
        optionsContainer.addEventListener('mouseout', (e) => {
            const option = e.target.closest('.custom-dropdown-option');
            if (option) {
                option.style.backgroundColor = 'white';
            }
        });
    }

    // Clean up dropdown resources
    cleanup() {
        // Remove event listeners
        this.dropdowns.forEach((customDropdown, selectId) => {
            const dropdownButton = customDropdown.querySelector('.custom-dropdown-button');
            const options = customDropdown.querySelectorAll('.custom-dropdown-option');
            
            if (dropdownButton) {
                dropdownButton.replaceWith(dropdownButton.cloneNode(true));
            }
            
            options.forEach(option => {
                option.replaceWith(option.cloneNode(true));
            });
        });
        
        // Remove document click listener
        document.removeEventListener('click', this.handleDocumentClick);
        
        // Clear dropdowns map
        this.dropdowns.clear();
        
        // Reset state
        this.activeDropdown = null;
        this.isInitialized = false;
        
        console.log('DropdownManager cleanup completed');
    }
    
    // Helper method to get default text for dropdowns
    getDefaultText(type) {
        if (type === 'type') {
            return 'All Types';
        } else if (type === 'status') {
            return 'All Statuses';
        } else if (type === 'form') {
            return 'Select Type';
        } else if (type === 'status-form') {
            return 'Select Status';
        }
        return '';
    }
}

// Export the class
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CustomDropdownManager;
}
