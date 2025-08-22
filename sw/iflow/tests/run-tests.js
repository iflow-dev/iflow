#!/usr/bin/env node

const puppeteer = require('puppeteer');
const path = require('path');

async function runTests() {
    console.log('🚀 Starting Test Case 5: Cross Visibility After Text Input');
    
    const browser = await puppeteer.launch({ 
        headless: false, // Set to true for headless mode
        slowMo: 100 // Slow down actions for visibility
    });
    
    try {
        const page = await browser.newPage();
        
        // Load the template
        const templatePath = path.join(__dirname, 'template.html');
        await page.goto(`file://${templatePath}`);
        
        console.log('📄 Template loaded, waiting for filter initialization...');
        
        // Wait for the filter to be initialized
        await page.waitForFunction(() => window.textFilter !== undefined, { timeout: 10000 });
        
        console.log('✅ Filter initialized, running Test Case 5...');
        
        // Run Test Case 5
        const testResult = await page.evaluate(async () => {
            if (!window.textFilter) {
                return { success: false, error: 'Filter not initialized' };
            }
            
            console.log('=== Running Test Case 5: Cross Visibility After Text Input ===');
            
            // Ensure input starts empty
            window.textFilter.setValue('');
            
            // Get initial clear button visibility
            const initialClearButtonVisible = window.textFilter.clearButton.style.display === 'block';
            console.log('Initial clear button visibility: ' + initialClearButtonVisible);
            console.log('Initial input value: "' + window.textFilter.getValue() + '"');
            
            // Simulate user typing text
            const testText = 'user input text';
            window.textFilter.setValue(testText);
            
            // Wait a moment for state updates
            await new Promise(resolve => setTimeout(resolve, 100));
            
            // Check if clear button is now visible
            const finalClearButtonVisible = window.textFilter.clearButton.style.display === 'block';
            const finalInputValue = window.textFilter.getValue();
            const finalState = window.textFilter.state;
            
            console.log('After text input:');
            console.log('  - Input value: "' + finalInputValue + '"');
            console.log('  - Clear button visible: ' + finalClearButtonVisible);
            console.log('  - Filter state: ' + finalState);
            
            // Check if test passed
            const textEntered = finalInputValue === testText;
            const clearButtonVisible = finalClearButtonVisible;
            const stateActive = finalState === 'active';
            
            const allPassed = textEntered && clearButtonVisible && stateActive;
            
            return {
                success: true,
                allPassed,
                details: {
                    textEntered,
                    clearButtonVisible,
                    stateActive,
                    initialValue: window.textFilter.getValue(),
                    finalValue: finalInputValue,
                    finalState: finalState,
                    clearButtonDisplay: window.textFilter.clearButton.style.display
                }
            };
        });
        
        if (testResult.success) {
            console.log('\n📊 Test Case 5 Results:');
            console.log('========================');
            console.log(`✅ Text entered: ${testResult.details.textEntered ? 'PASSED' : 'FAILED'}`);
            console.log(`✅ Clear button visible: ${testResult.details.clearButtonVisible ? 'PASSED' : 'FAILED'}`);
            console.log(`✅ State active: ${testResult.details.stateActive ? 'PASSED' : 'FAILED'}`);
            console.log(`\n🎯 Overall Result: ${testResult.allPassed ? 'PASSED' : 'FAILED'}`);
            
            if (testResult.allPassed) {
                console.log('\n🎉 Test Case 5 PASSED: Cross becomes visible after text input');
            } else {
                console.log('\n❌ Test Case 5 FAILED: Some conditions not met');
                console.log('\n📋 Detailed Results:');
                console.log(`   Initial Value: "${testResult.details.initialValue}"`);
                console.log(`   Final Value: "${testResult.details.finalValue}"`);
                console.log(`   Final State: ${testResult.details.finalState}`);
                console.log(`   Clear Button Display: ${testResult.details.clearButtonDisplay}`);
            }
        } else {
            console.error('❌ Test failed to run:', testResult.error);
        }
        
        // Keep browser open for manual inspection
        console.log('\n🔍 Browser will remain open for manual inspection...');
        console.log('   Close the browser window when done, or press Ctrl+C to exit');
        
        // Wait for user to close browser or Ctrl+C
        await new Promise(() => {});
        
    } catch (error) {
        console.error('❌ Error running tests:', error);
    } finally {
        await browser.close();
    }
}

// Check if Puppeteer is available
try {
    require('puppeteer');
    runTests();
} catch (error) {
    console.log('📦 Puppeteer not installed. Installing...');
    console.log('   Run: npm install puppeteer');
    console.log('   Then run: node run-tests.js');
}
