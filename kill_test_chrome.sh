#!/bin/bash

# Simple script to kill leftover test Chrome processes
# Returns non-zero if processes were found and killed
# Excludes crash handler processes that get auto-restarted

found_processes=false

# Kill Chrome processes with test-type=webdriver (exclude crash handlers)
if pkill -f "test-type=webdriver" 2>/dev/null | grep -v "crashpad_handler" 2>/dev/null; then
    echo "test-type=webdriver processes killed"
    found_processes=true
fi

# Kill chromedriver processes
if pkill -f "chromedriver" 2>/dev/null; then
    echo "chromedriver processes killed"
    found_processes=true
fi

# Kill Chrome processes with --enable-automation (exclude crash handlers)
if pkill -f "enable-automation" 2>/dev/null | grep -v "crashpad_handler" 2>/dev/null; then
    echo "enable-automation processes killed"
    found_processes=true
fi

# Kill Chrome processes with --remote-debugging-port (exclude crash handlers)
if pkill -f "remote-debugging-port" 2>/dev/null | grep -v "crashpad_handler" 2>/dev/null; then
    echo "remote-debugging-port processes killed"
    found_processes=true
fi

if [ "$found_processes" = true ]; then
    exit 1
else
    exit 0
fi
