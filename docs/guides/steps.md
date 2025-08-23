# Step Definition Style Guide

## 🎯 **Overview**

This guide defines the standards for implementing BDD step definitions. Following these guidelines ensures:
- **Consistent code quality** across all step files
- **Maintainable test implementations** that are easy to understand
- **Efficient execution** with minimal boilerplate
- **Proper integration** with control classes

## 📋 **Core Principles**

### **✅ DO:**
- Use control classes for all page interactions
- Keep step implementations simple and focused
- Use descriptive function names that match Gherkin steps
- Handle assertions with clear error messages
- Follow the single responsibility principle

### **❌ DON'T:**
- Use direct Selenium WebDriver calls
- Execute JavaScript with `execute_script`
- Create unnecessary intermediate variables
- Use local imports within functions
- Implement complex logic in step functions

## 🏗️ **File Structure**

### **Standard Layout**
```python
# 1. Imports (standard library, third-party, local)
from radish import step, given, when, then
from bdd.controls.artifact import Artifacts
from bdd.controls.toolbar import Toolbar

# 2. Step definitions
@step("step description")
def step_function_name(step):
    # Implementation here
```

### **Import Organization**
```python
# ✅ GOOD: Clean, organized imports
from radish import step
from bdd.controls.artifact import Artifacts
from bdd.controls.toolbar import Toolbar

# ❌ BAD: Scattered, unused imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from radish import step, world
from bdd.logging_config import logger
```

## 🎭 **Step Decorators**

### **Step Types**
```python
@step("universal step")           # Generic step for any context
@given("precondition")            # Setup/background steps
@when("action")                   # Action/behavior steps
@then("verification")             # Assertion/verification steps
```

## 🔧 **Implementation Patterns**

### **Simple Action Steps**
```python
# ✅ GOOD: Direct control usage
@step("I click the create button")
def i_click_create_button(step):
    Toolbar().create_button.click()

# ❌ BAD: Unnecessary variable assignment
@step("I click the create button")
def i_click_create_button(step):
    button = Toolbar().create_button
    button.click()
```

### **Verification Steps**
```python
# ✅ GOOD: Direct assertion with control
@step("I see {count:d} artifacts")
def i_see_artifacts_count(step, count):
    actual_count = len(Artifacts().find())
    assert actual_count == count, f"Expected {count}, got {actual_count}"
```

## 🎨 **Naming Conventions**

### **Function Names**
```python
# ✅ GOOD: Descriptive, follows Gherkin
@step("I create a new requirement")
def i_create_a_new_requirement(step):
    pass

# ❌ BAD: Unclear or abbreviated names
@step("I create a new requirement")
def create_req(step):
    pass
```

## 🔍 **Error Handling**

### **Assertion Patterns**
```python
# ✅ GOOD: Clear error messages
@step("I see the statistics line")
def i_see_statistics_line(step):
    assert StatisticsLine().is_visible, "Statistics line is not visible"

# ✅ GOOD: Descriptive error with context
@step("I see {count:d} search results")
def i_see_search_results(step, count):
    actual_count = len(Artifacts().find())
    assert actual_count == count, f"Expected {count} results, but got {actual_count}"
```

## 📏 **Code Quality Standards**

### **Line Length**
- **Maximum**: 120 characters per line
- **Target**: Under 100 characters for readability

### **Function Length**
- **Target**: 1-3 lines per step function
- **Maximum**: 5 lines for complex steps

### **Import Count**
- **Target**: 2-5 imports per file
- **Maximum**: 8 imports before considering refactoring

## 🧪 **Testing Best Practices**

### **Step Independence**
```python
# ✅ GOOD: Each step is independent
@step("I go to home")
def i_go_to_home(step):
    Page().navigate_to_home()

@step("I create a new artifact")
def i_create_new_artifact(step):
    Toolbar().create_button.click()
```

## 📊 **Quality Metrics**

### **Target Metrics**
- **Lines per file**: Under 50 lines
- **Functions per file**: Under 15 functions
- **Imports per file**: Under 8 imports
- **Control usage**: 100% control-based (no direct Selenium)

### **Health Indicators**
- ✅ **No `world.driver` direct usage**
- ✅ **No `execute_script` calls**
- ✅ **Clean control class usage**
- ✅ **Mostly one-liner implementations**
- ✅ **No unused imports**
- ✅ **No verbose boilerplate**

---

*Following this style guide ensures that step definitions are maintainable, readable, and efficient while providing a solid foundation for BDD test automation.*
