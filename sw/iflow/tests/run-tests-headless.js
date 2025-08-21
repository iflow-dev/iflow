#!/usr/bin/env node

const puppeteer = require('puppeteer');
const path = require('path');

async function runTestsHeadless() {
    console.log('🚀 Starting Test Case 5: Cross Visibility After Text Input (Headless)');
    
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
        
        console.log('✅ Filter initialized, running Test Case 5...');
        
        // Run Test Case 5
        const testResult = await page.evaluate(async () => {
            if (!window.textFilter) {
                return { success: false, error: 'Filter not initialized' };
            }
            
            // Ensure input starts empty
            window.textFilter.setValue('');
            
            // Get initial clear button visibility
            const initialClearButtonVisible = window.textFilter.clearButton.style.display === 'block';
            
            // Simulate user typing text
            const testText = 'user input text';
            window.textFilter.setValue(testText);
            
            // Wait a moment for state updates
            await new Promise(resolve => setTimeout(resolve, 100));
            
            // Check if clear button is now visible
            const finalClearButtonVisible = window.textFilter.clearButton.style.display === 'block';
            const finalInputValue = window.textFilter.getValue();
            const finalState = window.textFilter.state;
            
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
                process.exit(0); // Success exit code
            } else {
                console.log('\n❌ Test Case 5 FAILED: Some conditions not met');
                console.log('\n📋 Detailed Results:');
                console.log(`   Initial Value: "${testResult.details.initialValue}"`);
                console.log(`   Final Value: "${testResult.details.finalValue}"`);
                console.log(`   Final State: ${testResult.details.finalState}`);
                console.log(`   Clear Button Display: ${testResult.details.clearButtonDisplay}`);
                process.exit(1); // Failure exit code
            }
        } else {
            console.error('❌ Test failed to run:', testResult.error);
            process.exit(1);
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
    runTestsHeadless();
} catch (error) {
    console.log('📦 Puppeteer not installed. Installing...');
    console.log('   Run: npm install puppeteer');
    console.log('   Then run: node run-tests-headless.js');
    process.exit(1);
}
