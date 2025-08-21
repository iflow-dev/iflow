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
        
        // Load the template
        const templatePath = path.join(__dirname, 'template.html');
        await page.goto(`file://${templatePath}`);
        
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
        const allPassed = textEntered && clearButtonVisible && stateActive;
        
        // Add Test Case 5 results to the results array
        const testCase5Result = {
            testId: 5,
            name: 'Cross Visibility After Text Input (Real User Input)',
            passed: allPassed,
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

