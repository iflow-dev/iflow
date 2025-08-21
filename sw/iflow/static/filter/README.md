# Filter Module

This directory contains all filter-related JavaScript classes and utilities for the iflow application.

## File Structure

### Core Classes
- **`control.js`** - Base `FilterControl` class that provides common filter functionality
- **`manager.js`** - `FilterManager` singleton that coordinates all filters and search operations

### Filter Type Implementations
- **`icon.js`** - `IconFilter` class for icon-based filters (e.g., flag filter)
- **`select.js`** - `SelectFilter` class for dropdown/select filters
- **`text-input.js`** - `TextInputFilter` class for text input filters
- **`clear.js`** - `ClearFilter` class for clearing/resetting filters

### Demo and Examples
- **`demo.js`** - Example implementation showing how to use filter controls
- **`color-demo.js`** - Demo of color configuration capabilities

## Architecture

The filter system follows a hierarchical design:

```
FilterControl (base class)
├── IconFilter
├── SelectFilter
├── TextInputFilter
└── ClearFilter
```

### Key Features

- **State Management**: Each filter can be in `active`, `inactive`, or `disabled` state
- **Click to Cycle**: Click on filter footer (name) to cycle through states
- **Disabled State**: Disabled filters keep their settings but don't apply to search
- **Centralized Logic**: Base class handles all disabled state logic
- **Visual Feedback**: CSS classes provide clear visual state indication

### Usage

Filters are automatically initialized by the `Toolbar` class and integrated with the `FilterManager`. Users can:

1. **Click filter names** to cycle through states
2. **See visual feedback** for each state
3. **Maintain settings** even when filters are disabled
4. **Apply multiple filters** simultaneously

## CSS Classes

- `.filter-active` - Orange border, filter applies
- `.filter-inactive` - Transparent border, filter doesn't apply
- `.filter-disabled` - Grey border with strikethrough, filter doesn't apply but keeps settings
