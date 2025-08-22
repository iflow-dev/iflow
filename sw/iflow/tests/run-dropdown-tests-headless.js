#!/usr/bin/env node

const puppeteer = require('puppeteer');
const path = require('path');

async function runDropdownTestsHeadless() {
    console.log('🚀 Starting SelectFilter Dropdown Tests (Headless)');
    
    const browser = await puppeteer.launch({ 
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    try {
        const page = await browser.newPage();
        
        // Capture console messages from the browser
        page.on('console', (msg) => {
            if (msg.type() === 'error') {
                console.log(`Browser Error: ${msg.text()}`);
            } else if (msg.type() === 'log') {
                console.log(`Browser Log: ${msg.text()}`);
            }
        });
        
        // Load the dropdown test template from the test server
        await page.goto('http://localhost:7001/static/test-dropdown-template.html');
        
        console.log('📄 Dropdown test template loaded, waiting for SelectFilter initialization...');
        
        // Wait for the SelectFilter to be initialized
        await page.waitForFunction(() => window.statusFilter !== undefined, { timeout: 10000 });
        
        console.log('✅ SelectFilter initialized, running all tests...\n');
        
        // Run all test cases
        const results = await page.evaluate(async () => {
            const testResults = [];
            
            // Test Case 1: Initial State
            console.log('=== Running Test Case 1: Initial State ===');
            if (window.statusFilter) {
                const initialState = window.statusFilter.state;
                const initialValue = window.statusFilter.getValue();
                const expectedState = 'inactive';
                const expectedValue = '';
                
                const stateCorrect = initialState === expectedState;
                const valueCorrect = initialValue === expectedValue;
                const testPassed = stateCorrect && valueCorrect;
                
                testResults.push({
                    testId: 1,
                    name: 'Initial State',
                    passed: testPassed,
                    details: {
                        stateCorrect: stateCorrect,
                        valueCorrect: valueCorrect,
                        expectedState: expectedState,
                        actualState: initialState,
                        expectedValue: expectedValue,
                        actualValue: initialValue
                    }
                });
            }
            
            // Test Case 2: Value Selection
            console.log('=== Running Test Case 2: Value Selection ===');
            if (window.statusFilter) {
                // Set a value
                window.statusFilter.setValue('active');
                
                // Wait a moment for state updates
                await new Promise(resolve => setTimeout(resolve, 100));
                
                const newState = window.statusFilter.state;
                const newValue = window.statusFilter.getValue();
                const expectedState = 'active';
                const expectedValue = 'active';
                
                const stateCorrect = newState === expectedState;
                const valueCorrect = newValue === expectedValue;
                const testPassed = stateCorrect && valueCorrect;
                
                testResults.push({
                    testId: 2,
                    name: 'Value Selection',
                    passed: testPassed,
                    details: {
                        stateCorrect: stateCorrect,
                        valueCorrect: valueCorrect,
                        expectedState: expectedState,
                        actualState: newState,
                        expectedValue: expectedValue,
                        actualValue: newValue
                    }
                });
            }
            
            // Test Case 3: State Cycling
            console.log('=== Running Test Case 3: State Cycling ===');
            if (window.statusFilter) {
                // Ensure filter is active first
                window.statusFilter.setValue('pending');
                await new Promise(resolve => setTimeout(resolve, 100));
                
                const initialState = window.statusFilter.state;
                console.log('Initial state before cycling:', initialState);
                
                // Click footer to cycle state
                const footer = window.statusFilter.footer;
                if (footer) {
                    footer.click();
                    await new Promise(resolve => setTimeout(resolve, 100));
                    
                    const afterClickState = window.statusFilter.state;
                    console.log('State after click:', afterClickState);
                    
                    const stateChanged = afterClickState !== initialState;
                    const isDisabled = afterClickState === 'disabled';
                    const testPassed = stateChanged && isDisabled;
                    
                    testResults.push({
                        testId: 3,
                        name: 'State Cycling',
                        passed: testPassed,
                        details: {
                            stateChanged: stateChanged,
                            isDisabled: isDisabled,
                            initialState: initialState,
                            afterClickState: afterClickState
                        }
                    });
                }
            }
            
            // Test Case 4: Clear Functionality
            console.log('=== Running Test Case 4: Clear Functionality ===');
            if (window.statusFilter) {
                // Set a value first
                window.statusFilter.setValue('completed');
                await new Promise(resolve => setTimeout(resolve, 100));
                
                // Clear the filter
                window.statusFilter.clearFilter();
                await new Promise(resolve => setTimeout(resolve, 100));
                
                const clearedState = window.statusFilter.state;
                const clearedValue = window.statusFilter.getValue();
                const expectedState = 'inactive';
                const expectedValue = '';
                
                const stateCorrect = clearedState === expectedState;
                const valueCorrect = clearedValue === expectedValue;
                const testPassed = stateCorrect && valueCorrect;
                
                testResults.push({
                    testId: 4,
                    name: 'Clear Functionality',
                    passed: testPassed,
                    details: {
                        stateCorrect: stateCorrect,
                        valueCorrect: valueCorrect,
                        expectedState: expectedState,
                        actualState: clearedState,
                        expectedValue: expectedValue,
                        actualValue: clearedValue
                    }
                });
            }
            
            // Test Case 5: EventManager Integration
            console.log('=== Running Test Case 5: EventManager Integration ===');
            if (window.statusFilter && window.eventManager) {
                const initialEventCount = window.eventManager.getStatus().totalEventsProcessed;
                
                // Trigger some events
                window.statusFilter.setValue('cancelled');
                await new Promise(resolve => setTimeout(resolve, 100));
                
                const footer = window.statusFilter.footer;
                if (footer) {
                    footer.click();
                    await new Promise(resolve => setTimeout(resolve, 100));
                    
                    const finalEventCount = window.eventManager.getStatus().totalEventsProcessed;
                    const eventsProcessed = finalEventCount > initialEventCount;
                    
                    testResults.push({
                        testId: 5,
                        name: 'EventManager Integration',
                        passed: eventsProcessed,
                        details: {
                            eventsProcessed: eventsProcessed,
                            initialEventCount: initialEventCount,
                            finalEventCount: finalEventCount
                        }
                    });
                }
            }
            
            return testResults;
        });
        
        // Display results
        console.log('📊 SelectFilter Test Results:');
        console.log('============================\n');
        
        let passedCount = 0;
        let totalCount = results.length;
        
        results.forEach(result => {
            const status = result.passed ? '✅ PASSED' : '❌ FAILED';
            console.log(`${status} - Test Case ${result.testId}: ${result.name}`);
            
            if (result.details) {
                console.log('   Details:', result.details);
            }
            
            if (result.passed) {
                passedCount++;
            }
        });
        
        console.log('\n🎯 Summary:');
        console.log('===========');
        console.log(`Total Tests: ${totalCount}`);
        console.log(`Passed: ${passedCount}`);
        console.log(`Failed: ${totalCount - passedCount}`);
        
        if (passedCount === totalCount) {
            console.log('\n🎉 All SelectFilter tests PASSED!');
            process.exit(0);
        } else {
            console.log('\n❌ Some SelectFilter tests FAILED');
            process.exit(1);
        }
        
    } catch (error) {
        console.error('❌ Error running SelectFilter tests:', error);
        process.exit(1);
    } finally {
        await browser.close();
    }
}

// Check if Puppeteer is available
try {
    require('puppeteer');
    runDropdownTestsHeadless();
} catch (error) {
    console.log('📦 Puppeteer not installed. Installing...');
    console.log('   Run: npm install puppeteer');
    console.log('   Then run: node run-dropdown-tests-headless.js');
    process.exit(1);
}

