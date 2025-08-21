# Text Input Filter Test Infrastructure

This directory contains a simple test setup for testing the TextInputFilter functionality in isolation.

## Files

- **`template.html`** - A minimal HTML page containing only the text-input filter with built-in tests
- **`README.md`** - This file

## How to Test

### 1. Open the HTML Template in Browser

Open `sw/iflow/tests/template.html` in your web browser to see the filter rendered and test the functionality manually.

### 2. Test the Filter

The HTML page includes:
- A single text input filter
- Debug information showing current state
- Test buttons to trigger different actions
- Console logging for debugging

### 3. Manual Testing Steps

1. **Initial State**: Filter should start as "inactive" (transparent border)
2. **Type Text**: Enter some text in the input field
3. **State Change**: Filter should become "active" (orange border, clear button visible)
4. **Click Footer**: Click on the "search" text below the input
5. **State Cycling**: Should cycle through: active → inactive → disabled → active

### 4. Debug Information

The page shows real-time information about:
- Current filter state
- Input value
- Clear button visibility
- Applied CSS classes

### 5. Console Logging

Open browser console to see:
- Filter initialization
- State changes
- Method calls
- Any errors

## Test Controls

- **Test Cycle State**: Manually trigger state cycling
- **Set Value "test"**: Programmatically set input value
- **Clear Value**: Programmatically clear input
- **Test Clear Button Visibility**: Run automated test for clear button visibility when input is empty

## Expected Behavior

- **inactive**: Filter is empty, no clear button
- **active**: Filter has value, clear button visible
- **disabled**: Filter is disabled but has content, clear button visible

## Automated Test

The template includes a built-in test for clear button visibility:

**Test: Clear Button Not Visible When Empty**
- **Purpose**: Verify that the clearing cross is not visible when the search text field is empty
- **How to Run**: Click the "Test Clear Button Visibility" button
- **Expected Result**: Clear button should be hidden (display: none) when input is empty
- **Test Output**: Shows PASSED/FAILED result with visual feedback and console logging

## Troubleshooting

If the filter doesn't work:
1. Check browser console for JavaScript errors
2. Verify the JavaScript files are loading correctly
3. Check that the filter wrapper has the correct CSS classes
4. Ensure the data-filter-type attribute is set correctly

## Future Development

This infrastructure can be extended with:
- Automated browser testing using Selenium
- Unit tests for the JavaScript classes
- Integration tests with the full application
- Performance testing
- Cross-browser compatibility testing


## requirements to template.thml

1. run test button:
    - name: run
    - turns yellow when running and shows "running"
    - turns green with name "PASSED" when test passed
    - shows a "redo" icon to rerun the test
    - turns red with "FAILED" when test fails
    

