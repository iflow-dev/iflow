# Cleanup Guide v2.0 - BDD Step Module Optimization

## 🎯 **Core Principles**

### **A step module should NEVER:**
- Use Selenium directly (`world.driver.find_element`, `By.XPATH`, etc.)
- Use JavaScript (`execute_script`)
- Have verbose boilerplate (try-catch, excessive logging, redundant comments)

### **A step module SHOULD:**
- Use control classes for all page interactions (`Toolbar().filter.status.select()`)
- Have step implementations that are mostly one-liners
- Be clean, focused, and maintainable

## 🧹 **Cleanup Patterns**

### **1. Import Cleanup**
```python
# ❌ BAD: Scattered, unused imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from radish import world, step, given, when, then

# ✅ GOOD: Clean, focused imports
from radish import step
from bdd.controls import Artifacts, Toolbar
```

### **2. Control Class Usage**
```python
# ❌ BAD: Direct Selenium usage
status_filter = world.driver.find_element(By.ID, "statusFilter")
select = Select(status_filter)
select.select_by_visible_text(status)

# ✅ GOOD: Control class abstraction
toolbar = Toolbar()
toolbar.filter.status.select(status)
```

### **3. Assert Optimization**
```python
# ❌ BAD: Verbose if-statement
if not status_artifacts:
    raise AssertionError(f"No artifacts found with status '{status}'")

# ✅ GOOD: Clean assert
assert status_artifacts, f"No artifacts found with status '{status}'"
```

### **4. Variable Optimization**
```python
# ❌ BAD: Unnecessary intermediate variables
artifacts = Artifacts()
status_artifacts = [a for a in artifacts.find() if a.status == status]

# ✅ GOOD: Direct usage
status_artifacts = [a for a in Artifacts().find() if a.status == status]
```

### **5. Remove Boilerplate**
```python
# ❌ BAD: Try-catch boilerplate
try:
    result = world.driver.execute_script(f"return setDropdownValue('statusFilter', '{status}');")
    if not result:
        raise AssertionError(f"Failed to set status filter to '{status}'")
except Exception as e:
    logger.debug(f"Fallback failed: {e}")
    raise AssertionError(f"Failed to set status filter to '{status}': {e}")

# ✅ GOOD: Direct control usage
toolbar = Toolbar()
toolbar.filter.status.select(status)
```

## 📋 **Step-by-Step Cleanup Process**

### **Phase 1: Import Cleanup**
1. **Remove unused imports** (F401 flake8 violations)
2. **Consolidate scattered imports** to top-level
3. **Remove local imports** within functions
4. **Use proper import sorting** (standard → third-party → local)

### **Phase 2: Control Class Migration**
1. **Identify direct Selenium usage** (`world.driver.find_element`, `By.XPATH`)
2. **Replace with appropriate control classes** (`Toolbar()`, `Artifacts()`, etc.)
3. **Remove JavaScript dependencies** (`execute_script` calls)
4. **Use control properties** (`.value`, `.text`, etc.)

### **Phase 3: Code Optimization**
1. **Convert if-statements to asserts** where appropriate
2. **Remove unnecessary variables** and intermediate assignments
3. **Remove redundant comments** and docstrings
4. **Optimize function implementations** to one-liners where possible

### **Phase 4: Verification**
1. **Check syntax** with `python -m py_compile`
2. **Check style** with `flake8 --max-line-length=120`
3. **Verify functionality** with dry-run test
4. **Commit changes** with descriptive messages

## 🔍 **Health Indicators**

### **Quick Health Check (File should be under 50 lines)**
- **Excellent**: Under 40 lines
- **Good**: Under 50 lines  
- **Needs work**: 50-100 lines
- **Critical**: Over 100 lines

### **Code Quality Signs**
- ✅ **No `world.driver` direct usage**
- ✅ **No `execute_script` calls**
- ✅ **Clean control class usage**
- ✅ **Mostly one-liner implementations**
- ✅ **No unused imports**
- ✅ **No verbose boilerplate**

### **Red Flags**
- ❌ **Multiple `world.driver.find_element` calls**
- ❌ **JavaScript dependencies**
- ❌ **Verbose try-catch blocks**
- ❌ **Scattered imports**
- ❌ **Unnecessary intermediate variables**

## 🚀 **Implementation Examples**

### **Before (Bad)**
```python
from radish import step, world
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from bdd.logging_config import logger

@step(r"I set the status filter to {status:QuotedString}")
def i_set_status_filter_to(step, status):
    try:
        # Use JavaScript accessibility function to set the status filter
        logger.debug(f"Using JavaScript accessibility function to set status filter to '{status}'...")
        
        # Call the JavaScript function to set the dropdown value
        result = world.driver.execute_script(
            f"return setDropdownValue('statusFilter', '{status}');"
        )
        
        if result:
            logger.debug(f"Successfully set status filter to '{status}' using JavaScript accessibility function")
        else:
            # Fallback to traditional Select method
            status_filter = world.driver.find_element(By.ID, "statusFilter")
            select = Select(status_filter)
            select.select_by_visible_text(status)
            logger.debug(f"Fallback: Successfully selected status '{status}' using Select")
        
        # Wait for the filter to take effect
        time.sleep(2)
        logger.debug("Waited 2 seconds for filter to take effect")
        
    except Exception as e:
        logger.debug(f"Fallback failed: {e}")
        raise AssertionError(f"Failed to set status filter to '{status}': {e}")
```

### **After (Good)**
```python
from radish import step
from bdd.controls import Toolbar

@step(r"I set the status filter to {status:QuotedString}")
def i_set_status_filter_to(step, status):
    Toolbar().filter.status.select(status)
```

## 📊 **Expected Results**

### **Typical Improvements**
- **LOCs**: 50-80% reduction
- **Imports**: 70-90% reduction
- **JavaScript dependency**: 100% elimination
- **Direct Selenium usage**: 100% elimination
- **Code quality**: Significant improvement

### **File Transformation Example**
- **Before**: 85 lines with JavaScript, manual WebDriver, boilerplate
- **After**: 39 lines with clean control classes, optimized assertions
- **Improvement**: 54% reduction, 100% control class usage

## ⚠️ **Common Pitfalls**

### **1. Over-optimization**
- **Don't sacrifice readability** for line count
- **Keep meaningful variable names** when they add clarity
- **Maintain logical flow** in complex steps

### **2. Control Class Assumptions**
- **Verify control classes exist** before using them
- **Check method signatures** for proper usage
- **Test control interactions** to ensure they work

### **3. Import Dependencies**
- **Update all references** when renaming files
- **Check import chains** for broken dependencies
- **Verify imports work** after cleanup

## 🔧 **Verification Commands**

### **Essential Checks**
```bash
# Syntax verification
python -m py_compile filename.py

# Style verification  
flake8 filename.py --max-line-length=120

# Functionality verification
./bdd-test --tid XXXX --dry-run
```

### **Health Metrics**
```bash
# Line count
wc -l filename.py

# Import count
grep -c "^from\|^import" filename.py

# Control class usage
grep -c "Toolbar()\|Artifacts()\|Button(" filename.py

# Direct Selenium usage (should be 0)
grep -c "world.driver\|By.XPATH\|execute_script" filename.py
```

## 📝 **Commit Guidelines**

### **Commit Message Format**
```
cleanup: filename.py - Brief description of changes

KEY IMPROVEMENTS:
1. Specific change 1
2. Specific change 2
3. Specific change 3

BEFORE: X lines with problems
AFTER: Y lines with improvements
RESULT: Z% reduction, specific benefits
```

### **When to Commit**
- **After each phase** (import cleanup, control migration, etc.)
- **After verification** (syntax, style, functionality)
- **Before major changes** (save progress)
- **After completion** (final state)

## 🎯 **Success Criteria**

### **Module is "Clean" when:**
- ✅ **Under 50 lines** (ideally under 40)
- ✅ **No direct Selenium usage**
- ✅ **No JavaScript dependencies**
- ✅ **Clean control class usage**
- ✅ **Mostly one-liner implementations**
- ✅ **No flake8 violations**
- ✅ **All tests pass**

### **Module is "Optimized" when:**
- ✅ **Under 40 lines**
- ✅ **100% control class usage**
- ✅ **Clean, readable code**
- ✅ **Efficient implementations**
- ✅ **No unnecessary variables**
- ✅ **Proper error handling**

---

*This guide focuses on practical, actionable steps for transforming BDD step modules from verbose, JavaScript-dependent code to clean, maintainable control class abstractions.*
