#!/bin/bash

echo "🧪 Running Test Case 5: Cross Visibility After Text Input"
echo "=========================================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "run-tests.js" ]; then
    echo "❌ Please run this script from the tests directory"
    exit 1
fi

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Run the test
echo "🚀 Starting test execution..."
node run-tests.js

echo ""
echo "✅ Test execution complete!"
