# BDD Architecture Guide

## 🎯 **Overview**

This guide documents the Behavior-Driven Development (BDD) architecture used in our project. The architecture follows a clean separation of concerns with three main components:

1. **Feature Files** - Human-readable test specifications
2. **Step Files** - Python implementations of test steps
3. **Control Classes** - Page Object Model abstractions

## 📁 **Directory Structure**

```
tests/
├── features/                    # Gherkin feature files
│   ├── test_artifact_creation.feature
│   ├── test_status_filtering.feature
│   └── ...
├── radish/steps/               # Step definition files
│   ├── artifact_creation_steps.py
│   ├── statusfilter.py
│   ├── version.py
│   └── ...
└── support/bdd/controls/       # Control class implementations
    ├── __init__.py
    ├── base.py
    ├── artifact.py
    ├── toolbar.py
    ├── editor.py
    └── ...
```

## 🥒 **Feature Files (Gherkin)**

### **Purpose**
Feature files define test scenarios in human-readable Gherkin syntax. They serve as:
- **Living documentation** of system behavior
- **Acceptance criteria** for features
- **Test specifications** for developers

### **Structure**
```gherkin
@smoke
Feature: Test Artifact Creation

    As a user
    I want to create new artifacts from the search view
    So that I can add new items to the project

    @tid:0101
    Scenario: Create New Artifact from Search View
        Given I go to home
        When I create a new requirement
        And I set the type to "requirement"
        And I set the summary to "Test requirement for BDD testing"
        And I set the description to "This is a test requirement created during BDD test execution"
        And I set the status to "open"
        When I save the article
        Then I see the new artifact in the list
```

### **Best Practices**
- **Use descriptive names** that explain the business value
- **Include @smoke tag** for critical path tests
- **Add @tid:XXXX tags** for unique test identification
- **Write scenarios** from the user's perspective
- **Keep steps focused** on single actions or verifications

## 🐍 **Step Files (Python)**

### **Purpose**
Step files contain the Python implementations of Gherkin steps. They:
- **Bridge** Gherkin syntax to executable code
- **Orchestrate** control class interactions
- **Handle** test data and assertions

### **Structure**
```python
from radish import step
from bdd.controls.artifact import Artifacts
from bdd.controls.editor import Editor

@step("I create a new requirement")
def i_create_a_new_requirement(step):
    editor = Editor()
    editor.open()

@step("I see the new artifact in the list")
def i_see_new_artifact_in_list(step):
    artifacts = Artifacts()
    assert artifacts.find_one(summary="Test requirement for BDD testing")
```

### **Key Principles**
- **Use control classes** for all page interactions
- **Keep implementations simple** (ideally one-liners)
- **Avoid direct Selenium** or JavaScript usage
- **Use descriptive function names** that match Gherkin steps
- **Handle assertions** with clear error messages

## 🎮 **Control Classes**

### **Purpose**
Control classes implement the Page Object Model pattern. They:
- **Abstract** web page elements and interactions
- **Provide** clean, reusable interfaces
- **Encapsulate** Selenium WebDriver complexity
- **Enable** maintainable test code

### **Architecture**
```
ControlBase (Abstract Base)
├── Artifact (Individual artifact element)
├── Artifacts (Collection of artifacts)
├── Editor (Form/modal interactions)
├── Toolbar (Toolbar controls and filters)
├── Page (Page-level operations)
└── ...
```

### **Base Class Structure**
```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ControlBase:
    """Base class for all control objects."""
    
    def __init__(self, xpath):
        self.xpath = xpath
    
    def locate(self, timeout=5):
        """Locate the element with explicit wait."""
        wait = WebDriverWait(world.driver, timeout)
        return wait.until(EC.presence_of_element_located((By.XPATH, self.xpath)))
    
    def exists(self):
        """Check if element exists."""
        try:
            self.locate(timeout=1)
            return True
        except:
            return False
```

## 🔄 **Data Flow**

### **Test Execution Flow**
1. **Radish** reads Gherkin feature files
2. **Step definitions** are matched to Gherkin steps
3. **Step functions** execute and use control classes
4. **Control classes** interact with web elements via Selenium
5. **Assertions** verify expected behavior

### **Control Class Usage Pattern**
```python
# ✅ GOOD: Clean control usage
@step("I verify the status filter is set to {status:QuotedString}")
def i_verify_status_filter_is_set_to(step, status):
    actual_value = Toolbar().filter.status.value
    assert actual_value == status, f"Expected '{status}', got '{actual_value}'"

# ❌ BAD: Direct Selenium usage
@step("I verify the status filter is set to {status:QuotedString}")
def i_verify_status_filter_is_set_to(step, status):
    element = world.driver.find_element(By.ID, "statusFilter")
    actual_value = element.text
    assert actual_value == status
```

## 🧪 **Testing Framework**

### **Radish Integration**
- **Tag filtering**: `--tags="(tid:0101) and (not fixme)"`
- **Dry-run mode**: `--dry-run` for validation without execution
- **Headless mode**: Chrome runs headless by default
- **Port management**: Automatic port 7000 allocation

### **Test Execution**
```bash
# Run specific test by ID
./bdd-test --tid 0101

# Run all smoke tests
./bdd-test --smoke

# Run with dry-run validation
./bdd-test --tid 0101 --dry-run

# Run with foreground Chrome (for debugging)
./bdd-test --tid 0101 --foreground
```

## 📚 **Related Documentation**

- **[Step Implementation Guide](steps.md)** - How to write proper step definitions
- **[Control Class Guide](control.md)** - How to implement control classes
- **[Cleanup Guide](cleanup.md)** - How to refactor existing code

## 🎓 **Real-World Transformation Example**

### **Case Study: verification.py Module**

The verification.py module demonstrates the complete BDD architecture transformation:

#### **Before Transformation (verification_field_steps.py)**
- **Lines**: 128 LOCs
- **Architecture**: Direct Selenium usage, mixed patterns
- **Issues**: Code duplication, intermediate variables, poor maintainability

#### **After Transformation (verification.py)**
- **Lines**: 58 LOCs (55% reduction)
- **Architecture**: 100% control-based, clean abstractions
- **Benefits**: Maintainable, reusable, performant

#### **New Control Classes Created**
```python
# VerificationField - handles verification field interactions
# ArtifactForm - manages form field operations  
# ArtifactVerification - handles verification display logic
# SuccessIndicator - manages success message verification
```

#### **Architecture Benefits Demonstrated**
- **Separation of Concerns**: Each control handles one UI component
- **Reusability**: Controls used across multiple step functions
- **Maintainability**: Centralized element management
- **Performance**: Optimized control usage patterns
- **Cleanliness**: Step functions are mostly one-liners

#### **Transformation Journey**
1. **Architectural**: Direct Selenium → Control classes
2. **Structural**: 128 lines → 58 lines
3. **Quality**: Mixed patterns → Consistent architecture
4. **Performance**: Unoptimized → Optimized control usage
5. **Maintainability**: Poor → Excellent

## 🎯 **Architecture Benefits**

### **Maintainability**
- **Separation of concerns** between test logic and page interactions
- **Reusable controls** across multiple test scenarios
- **Centralized element management** for UI changes

### **Readability**
- **Human-readable** test specifications
- **Self-documenting** step implementations
- **Clear intent** in control class methods

### **Reliability**
- **Explicit waits** for element availability
- **Consistent interaction patterns** across tests
- **Robust error handling** with meaningful messages

### **Scalability**
- **Modular design** allows easy addition of new features
- **Control class inheritance** promotes code reuse
- **Standardized patterns** reduce learning curve

---

*This architecture ensures that BDD tests are maintainable, readable, and reliable while providing a solid foundation for test automation.*
