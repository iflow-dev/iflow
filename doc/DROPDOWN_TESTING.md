# Dropdown Testing Accessibility Functions

This document describes the JavaScript accessibility functions added to the custom dropdown implementation to improve testability, as requested in ticket #00073.

## Overview

The custom dropdown implementation now provides JavaScript functions that allow programmatic access to dropdown values and operations, making it easier to test dropdown functionality without relying on complex UI interactions.

## Available Functions

All functions are exposed globally on the `window` object and can be accessed from Selenium tests or browser console.

### Core Functions

#### `getDropdownValue(selectId)`
Get the current selected value of a dropdown.

**Parameters:**
- `selectId` (string): The ID of the original select element

**Returns:**
- `string|null`: The current selected value or null if not found

**Example:**
```javascript
const value = getDropdownValue('artifactType');
console.log(value); // 'requirement'
```

#### `setDropdownValue(selectId, value)`
Set the value of a dropdown programmatically.

**Parameters:**
- `selectId` (string): The ID of the original select element
- `value` (string): The value to set

**Returns:**
- `boolean`: True if successful, false otherwise

**Example:**
```javascript
const success = setDropdownValue('artifactType', 'requirement');
console.log(success); // true
```

### Utility Functions

#### `getDropdownOptions(selectId)`
Get all available options for a dropdown.

**Parameters:**
- `selectId` (string): The ID of the original select element

**Returns:**
- `Array`: Array of option values

**Example:**
```javascript
const options = getDropdownOptions('artifactType');
console.log(options); // ['requirement', 'task', 'test_case', ...]
```

#### `getDropdownDisplayText(selectId)`
Get the display text of the currently selected option.

**Parameters:**
- `selectId` (string): The ID of the original select element

**Returns:**
- `string|null`: The display text or null if not found

**Example:**
```javascript
const text = getDropdownDisplayText('artifactType');
console.log(text); // '📄 Requirement'
```

#### `isDropdownOpen(selectId)`
Check if a dropdown is currently open.

**Parameters:**
- `selectId` (string): The ID of the original select element

**Returns:**
- `boolean`: True if dropdown is open, false otherwise

**Example:**
```javascript
const isOpen = isDropdownOpen('artifactType');
console.log(isOpen); // false
```

#### `openDropdown(selectId)`
Open a dropdown programmatically.

**Parameters:**
- `selectId` (string): The ID of the original select element

**Returns:**
- `boolean`: True if successful, false otherwise

**Example:**
```javascript
const success = openDropdown('artifactType');
console.log(success); // true
```

#### `closeDropdown(selectId)`
Close a dropdown programmatically.

**Parameters:**
- `selectId` (string): The ID of the original select element

**Returns:**
- `boolean`: True if successful, false otherwise

**Example:**
```javascript
const success = closeDropdown('artifactType');
console.log(success); // true
```

## Global Access

The dropdown manager instance is also available globally:

```javascript
// Access the full dropdown manager
const manager = window.dropdownManager;

// Use manager methods directly
const value = manager.getDropdownValue('artifactType');
const success = manager.setDropdownValue('artifactType', 'requirement');
```

## Usage in Selenium Tests

These functions can be used directly in Selenium tests via `execute_script`:

```python
# Set dropdown value
result = driver.execute_script("""
    return setDropdownValue('artifactType', 'requirement');
""")

# Get dropdown value
value = driver.execute_script("""
    return getDropdownValue('artifactType');
""")

# Check if dropdown is open
is_open = driver.execute_script("""
    return isDropdownOpen('artifactType');
""")
```

## Implementation Details

### Automatic Exposure
The functions are automatically exposed when the dropdown manager is initialized:

```javascript
// In app_web.js
if (dropdownManager.initializeData(workItemTypes, artifactStatuses)) {
    dropdownManager.createCustomDropdowns();
    // Expose dropdown accessibility functions for testing (Ticket #00073)
    dropdownManager.exposeForTesting();
}
```

### Validation
The `setDropdownValue` function includes validation:
- Checks if the select element exists
- Validates that the value is a valid option
- Updates both the original select and custom dropdown display
- Triggers change events for proper form handling

### Error Handling
All functions include proper error handling and logging:
- Console warnings for missing elements
- Validation of input parameters
- Graceful fallbacks for edge cases

## Benefits

1. **Improved Testability**: Tests can interact with dropdowns without complex UI interactions
2. **Reliability**: No dependency on position-based clicks or timing issues
3. **Simplicity**: Direct programmatic access to dropdown state
4. **Validation**: Built-in validation ensures only valid values are set
5. **Debugging**: Comprehensive logging for troubleshooting

## Ticket #00073 Implementation

This implementation directly addresses the requirements in ticket #00073:

- ✅ **Check the current selected value**: `getDropdownValue(selectId)`
- ✅ **Set the current selected value**: `setDropdownValue(selectId, value)`

The functions provide clean, reliable access to dropdown functionality for testing purposes.
