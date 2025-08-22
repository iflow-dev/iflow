#!/usr/bin/env node

const puppeteer = require('puppeteer');
const path = require('path');

async function runAllTests() {
    console.log('🚀 Starting All Test Cases');
    console.log('===========================');
    
    const browser = await puppeteer.launch({ 
        headless: true, // Headless mode for CI/CD
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    try {
        const page = await browser.newPage();
        
        // Capture console messages from the browser (all messages for debugging)
        page.on('console', (msg) => {
            if (msg.type() === 'error') {
                console.log(`Browser Error: ${msg.text()}`);
            } else if (msg.type() === 'log') {
                console.log(`Browser Log: ${msg.text()}`);
            }
        });
        
        // Load the template from the test server
        await page.goto('http://localhost:7001/static/test-template.html');
        
        console.log('📄 Template loaded, waiting for filter initialization...');
        
        // Wait for the filter to be initialized
        await page.waitForFunction(() => window.textFilter !== undefined, { timeout: 10000 });
        
        console.log('✅ Filter initialized, running all tests...\n');
        
        // Run all test cases (some in page.evaluate, Test Case 5 using real DOM interaction)
        const results = await page.evaluate(async () => {
            const testResults = [];
            
            // Test Case 1: Clear Button Visibility When Empty
            console.log('=== Running Test Case 1: Clear Button Visibility When Empty ===');
            if (window.textFilter) {
                // Ensure input is empty
                window.textFilter.setValue('');
                
                // Check if clear button is hidden
                const clearButton = window.textFilter.clearButton;
                const isHidden = clearButton.style.display === 'none';
                const stateInactive = window.textFilter.state === 'inactive';
                const valueEmpty = window.textFilter.getValue() === '';
                
                const allPassed = isHidden && stateInactive && valueEmpty;
                testResults.push({
                    testId: 1,
                    name: 'Clear Button Visibility When Empty',
                    passed: allPassed,
                    details: {
                        buttonHidden: isHidden,
                        stateInactive: stateInactive,
                        valueEmpty: valueEmpty,
                        buttonDisplay: clearButton.style.display,
                        filterState: window.textFilter.state,
                        inputValue: window.textFilter.getValue()
                    }
                });
            }
            
            // Test Case 3: Filter State Cycling
            console.log('=== Running Test Case 3: Filter State Cycling ===');
            if (window.textFilter) {
                // Set input to have content first
                window.textFilter.setValue('test');
                
                // Get initial state
                const initialState = window.textFilter.state;
                
                // Cycle through states
                const states = [];
                for (let i = 0; i < 3; i++) {
                    window.textFilter.cycleState();
                    states.push(window.textFilter.state);
                }
                
                // Check if states changed
                const stateChanged = states.length > 0 && states.some(state => state !== initialState);
                testResults.push({
                    testId: 3,
                    name: 'Filter State Cycling',
                    passed: stateChanged,
                    details: {
                        stateChanged: stateChanged,
                        states: states,
                        initialState: initialState
                    }
                });
            }
            
            // Test Case 4: Clear Button Functionality
            console.log('=== Running Test Case 4: Clear Button Functionality ===');
            if (window.textFilter) {
                // Set input to have content first
                window.textFilter.setValue('test content');
                
                // Get initial state and value
                const initialState = window.textFilter.state;
                const initialValue = window.textFilter.getValue();
                
                // Click clear button
                window.textFilter.clearInput();
                
                // Check results
                const finalState = window.textFilter.state;
                const finalValue = window.textFilter.getValue();
                const clearButtonVisible = window.textFilter.clearButton.style.display === 'block';
                
                // Check if clear worked properly
                const valueCleared = finalValue === '';
                const stateChanged = finalState === 'inactive';
                const buttonHidden = !clearButtonVisible;
                
                const allPassed = valueCleared && stateChanged && buttonHidden;
                testResults.push({
                    testId: 4,
                    name: 'Clear Button Functionality',
                    passed: allPassed,
                    details: {
                        valueCleared: valueCleared,
                        stateChanged: stateChanged,
                        buttonHidden: buttonHidden,
                        initialValue: initialValue,
                        finalValue: finalValue,
                        initialState: initialState,
                        finalState: finalState,
                        clearButtonDisplay: window.textFilter.clearButton.style.display
                    }
                });
            }
            
            // Test Case 5 will be run outside page.evaluate() to use real user interaction
            
            return testResults;
        });
        
        // Test Case 5: Cross Visibility After Text Input (using real user interaction)
        console.log('=== Running Test Case 5: Cross Visibility After Text Input (Real User Input) ===');
        
        // Clear the input field first
        await page.evaluate(() => {
            if (window.textFilter) {
                window.textFilter.setValue('');
            }
        });
        
        // Get initial state
        const initialState = await page.evaluate(() => {
            if (!window.textFilter) return null;
            return {
                clearButtonVisible: window.textFilter.clearButton.style.display === 'block',
                inputValue: window.textFilter.getValue(),
                filterState: window.textFilter.state,
                clearButtonDisplay: window.textFilter.clearButton.style.display
            };
        });
        
        // Simulate real user typing by focusing the input and typing text
        await page.focus('#search-input');
                const testText = 'user input text';
        await page.type('#search-input', testText, { delay: 50 }); // Delay to simulate human typing
        
        // Wait for state updates
        await page.waitForTimeout(200);
        
        // Get final state after real user interaction
        const finalState = await page.evaluate(() => {
            if (!window.textFilter) return null;
            return {
                clearButtonVisible: window.textFilter.clearButton.style.display === 'block',
                inputValue: window.textFilter.getValue(),
                filterState: window.textFilter.state,
                clearButtonDisplay: window.textFilter.clearButton.style.display
            };
        });
        
        // Evaluate test results
        const textEntered = finalState.inputValue === testText;
        const clearButtonVisible = finalState.clearButtonVisible;
        const stateActive = finalState.filterState === 'active';
        const testCase5Passed = textEntered && clearButtonVisible && stateActive;
        
        // Add Test Case 5 results to the results array
        const testCase5Result = {
                    testId: 5,
            name: 'Cross Visibility After Text Input (Real User Input)',
            passed: testCase5Passed,
                    details: {
                        textEntered: textEntered,
                        clearButtonVisible: clearButtonVisible,
                        stateActive: stateActive,
                initialValue: initialState.inputValue,
                finalValue: finalState.inputValue,
                initialState: initialState.filterState,
                finalState: finalState.filterState,
                initialClearButtonDisplay: initialState.clearButtonDisplay,
                finalClearButtonDisplay: finalState.clearButtonDisplay
            }
        };
        
        results.push(testCase5Result);
        
        // Test Case 6: Filter Name Click to Disabled State (using real user interaction)
        console.log('=== Running Test Case 6: Filter Name Click to Disabled State (Real User Click) ===');
        
        // First, ensure the filter is in a known state (active) by typing some text
        await page.evaluate(() => {
            if (window.textFilter) {
                window.textFilter.setValue('test text');
            }
        });
        
        // Wait for state to settle
        await page.waitForTimeout(100);
        
        // Get initial state before clicking
        const initialStateBeforeClick = await page.evaluate(() => {
            if (!window.textFilter) return null;
            return {
                filterState: window.textFilter.state,
                inputValue: window.textFilter.getValue(),
                clearButtonVisible: window.textFilter.clearButton.style.display === 'block'
            };
        });
        
        // Simulate real user clicking on the filter footer (filter name)
        // The filter footer is the clickable element that cycles through states
        console.log('About to click on .filter-footer element...');
        
        // Check if the element exists and is visible
        const footerElement = await page.$('.filter-footer');
        if (!footerElement) {
            console.error('ERROR: .filter-footer element not found!');
        } else {
            console.log('✓ .filter-footer element found');
            const isVisible = await footerElement.isVisible();
            console.log('  - Element visible:', isVisible);
            const text = await page.evaluate(el => el.textContent, footerElement);
            console.log('  - Element text:', text);
        }
        
        // Check if the event handler is properly bound before clicking
        const eventHandlerInfo = await page.evaluate(() => {
            const footer = document.querySelector('.filter-footer');
            if (!footer) return { found: false };
            
            return {
                found: true,
                footerStyle: footer.style.cursor,
                footerTitle: footer.title,
                filterExists: !!window.textFilter,
                filterState: window.textFilter ? window.textFilter.state : 'no filter',
                footerElement: !!window.textFilter?.footer
            };
        });
        
        console.log('Event handler info:', eventHandlerInfo);
        

        
        // Perform the click and get the immediate result
        console.log('About to click on .filter-footer...');
        
        // Add a click event listener to see if the click is being captured
        await page.evaluate(() => {
            const footer = document.querySelector('.filter-footer');
            if (footer) {
                footer.addEventListener('click', (e) => {
                    console.log('DEBUG: Click event captured on footer!');
                    console.log('DEBUG: Event target:', e.target);
                    console.log('DEBUG: Event type:', e.type);
                });
            }
        });
        
        // Click and wait for any console output
        await page.click('.filter-footer');
        
        // Wait for the state change to complete
        await page.waitForTimeout(200);
        
        // Get final state after clicking
        const finalStateAfterClick = await page.evaluate(() => {
            if (!window.textFilter) return null;
            return {
                filterState: window.textFilter.state,
                inputValue: window.textFilter.getValue(),
                clearButtonVisible: window.textFilter.clearButton.style.display === 'block'
            };
        });
        
        // Evaluate test results
        const wasInitiallyActive = initialStateBeforeClick.filterState === 'active';
        const becameDisabled = finalStateAfterClick.filterState === 'disabled';
        const stateChanged = initialStateBeforeClick.filterState !== finalStateAfterClick.filterState;
        const testCase6Passed = wasInitiallyActive && becameDisabled && stateChanged;
        
        // Add Test Case 6 results to the results array
        const testCase6Result = {
            testId: 6,
            name: 'Filter Name Click to Disabled State (Real User Click)',
            passed: testCase6Passed,
            details: {
                wasInitiallyActive: wasInitiallyActive,
                becameDisabled: becameDisabled,
                stateChanged: stateChanged,
                initialState: initialStateBeforeClick.filterState,
                finalState: finalStateAfterClick.filterState,
                inputValue: finalStateAfterClick.inputValue,
                clearButtonVisible: finalStateAfterClick.clearButtonVisible
            }
        };
        
        results.push(testCase6Result);
        
        // Test Case 7: Disabled Filter Click to Active State (using real user interaction)
        console.log('=== Running Test Case 7: Disabled Filter Click to Active State (Real User Click) ===');
        
        // First, ensure the filter is in active state by typing text
        await page.evaluate(() => {
            if (window.textFilter) {
                window.textFilter.setValue('test text');
                // Force the state to be active after setting value
                if (window.textFilter.inputElement && window.textFilter.inputElement.value.trim() !== '') {
                    window.textFilter.setState('active');
                }
            }
        });
        
        // Wait for state to settle
        await page.waitForTimeout(200);
        
        // Get initial state (should be active after typing)
        const testCase7InitialActiveState = await page.evaluate(() => {
            if (!window.textFilter) return null;
            return {
                filterState: window.textFilter.state,
                inputValue: window.textFilter.getValue(),
                clearButtonVisible: window.textFilter.clearButton.style.display === 'block'
            };
        });
        
        console.log('Initial active state:', testCase7InitialActiveState.filterState);
        
        // First click: active -> disabled
        await page.click('.filter-footer');
        await page.waitForTimeout(100);
        
        // Get state after first click (should be disabled)
        const testCase7DisabledState = await page.evaluate(() => {
            if (!window.textFilter) return null;
            return {
                filterState: window.textFilter.state,
                inputValue: window.textFilter.getValue(),
                clearButtonVisible: window.textFilter.clearButton.style.display === 'block'
            };
        });
        
        console.log('State after first click (should be disabled):', testCase7DisabledState.filterState);
        
        // Second click: disabled -> active
        await page.click('.filter-footer');
        await page.waitForTimeout(100);
        
        // Get final state after second click (should be active)
        const testCase7FinalActiveState = await page.evaluate(() => {
            if (!window.textFilter) return null;
            return {
                filterState: window.textFilter.state,
                inputValue: window.textFilter.getValue(),
                clearButtonVisible: window.textFilter.clearButton.style.display === 'block'
            };
        });
        
        console.log('Final state after second click (should be active):', testCase7FinalActiveState.filterState);
        
        // Evaluate test results
        const testCase7WasInitiallyActive = testCase7InitialActiveState.filterState === 'active';
        const testCase7BecameDisabled = testCase7DisabledState.filterState === 'disabled';
        const testCase7BecameActiveAgain = testCase7FinalActiveState.filterState === 'active';
        const testCase7CycleCompleted = testCase7WasInitiallyActive && testCase7BecameDisabled && testCase7BecameActiveAgain;
        
        // Add Test Case 7 results to the results array
        const testCase7Result = {
            testId: 7,
            name: 'Disabled Filter Click to Active State (Real User Click)',
            passed: testCase7CycleCompleted,
            details: {
                wasInitiallyActive: testCase7WasInitiallyActive,
                becameDisabled: testCase7BecameDisabled,
                becameActiveAgain: testCase7BecameActiveAgain,
                cycleCompleted: testCase7CycleCompleted,
                initialActiveState: testCase7InitialActiveState.filterState,
                disabledState: testCase7DisabledState.filterState,
                finalActiveState: testCase7FinalActiveState.filterState,
                inputValue: testCase7FinalActiveState.inputValue,
                clearButtonVisible: testCase7FinalActiveState.clearButtonVisible
            }
        };
        
        results.push(testCase7Result);
        
        // Display results
        console.log('📊 All Test Results:');
        console.log('====================\n');
        
        let passedCount = 0;
        let totalCount = results.length;
        
        results.forEach(result => {
            const status = result.passed ? '✅ PASSED' : '❌ FAILED';
            const color = result.passed ? '\x1b[32m' : '\x1b[31m';
            const reset = '\x1b[0m';
            
            console.log(`${color}${status}${reset} - Test Case ${result.testId}: ${result.name}`);
            
            if (result.passed) {
                passedCount++;
            } else {
                console.log(`   Details: ${JSON.stringify(result.details, null, 2)}`);
            }
        });
        
        console.log('\n🎯 Summary:');
        console.log('===========');
        console.log(`Total Tests: ${totalCount}`);
        console.log(`Passed: ${passedCount}`);
        console.log(`Failed: ${totalCount - passedCount}`);
        
        if (passedCount === totalCount) {
            console.log('\n🎉 All tests PASSED!');
            process.exit(0); // Success exit code
        } else {
            console.log('\n❌ Some tests FAILED');
            process.exit(1); // Failure exit code
        }
        
    } catch (error) {
        console.error('❌ Error running tests:', error);
        process.exit(1);
    } finally {
        await browser.close();
    }
}

// Check if Puppeteer is available
try {
    require('puppeteer');
    runAllTests();
} catch (error) {
    console.log('📦 Puppeteer not installed. Installing...');
    console.log('   Run: npm install puppeteer');
    console.log('   Then run: node run-all-tests-headless.js');
    process.exit(1);
}

