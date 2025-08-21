# Command Line Test Execution

This directory contains automated tests that can be run from the command line to test the filter functionality without manual browser interaction.

## 🚀 Quick Start

### Option 1: Shell Script (Easiest)
```bash
cd sw/iflow/tests
./run-test5.sh
```

### Option 2: Direct Node.js Execution
```bash
cd sw/iflow/tests
npm install
node run-tests.js
```

### Option 3: Headless Mode (CI/CD)
```bash
cd sw/iflow/tests
npm install
node run-tests-headless.js
```

## 📋 Prerequisites

- **Node.js** (version 14 or higher)
- **npm** (comes with Node.js)

## 🔧 Installation

1. Navigate to the tests directory:
   ```bash
   cd sw/iflow/tests
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## 🧪 Available Tests

### Test Case 5: Cross Visibility After Text Input
- **Purpose**: Verify that the cross (clear button) becomes visible after user inputs text
- **Expected**: Clear button should become visible (display: block) when user types text

## 📊 Test Output

The test will provide detailed output including:

```
📊 Test Case 5 Results:
========================
✅ Text entered: PASSED
✅ Clear button visible: PASSED
✅ State active: PASSED

🎯 Overall Result: PASSED

🎉 Test Case 5 PASSED: Cross becomes visible after text input
```

## 🎯 Exit Codes

- **0**: Test PASSED
- **1**: Test FAILED or error occurred

## 🔍 Debugging

### Interactive Mode
- Use `node run-tests.js` for interactive testing with browser visible
- Browser stays open for manual inspection
- Press Ctrl+C to exit

### Headless Mode
- Use `node run-tests-headless.js` for CI/CD environments
- No browser window visible
- Automatic exit with appropriate exit code

## 📁 Files

- `run-tests.js` - Interactive test runner (browser visible)
- `run-tests-headless.js` - Headless test runner (CI/CD)
- `run-test5.sh` - Shell script wrapper
- `package.json` - Node.js dependencies
- `template.html` - Test HTML template

## 🚀 Integration Examples

### GitHub Actions
```yaml
- name: Run Filter Tests
  run: |
    cd sw/iflow/tests
    npm install
    node run-tests-headless.js
```

### Local Development
```bash
# Run test and keep browser open for debugging
npm test

# Run test in headless mode
npm run test:headless
```

### Continuous Integration
```bash
# Exit with proper exit code for CI systems
node run-tests-headless.js
echo $?  # Will show 0 for PASS, 1 for FAIL
```

## 🐛 Troubleshooting

### Puppeteer Installation Issues
If you encounter Puppeteer installation problems:
```bash
npm install puppeteer --unsafe-perm=true
```

### Permission Issues
Make sure the shell script is executable:
```bash
chmod +x run-test5.sh
```

### Browser Issues
For headless environments, the headless script includes necessary flags:
```javascript
args: ['--no-sandbox', '--disable-setuid-sandbox']
```
