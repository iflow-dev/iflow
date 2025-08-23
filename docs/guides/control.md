# Control Class Implementation Guide

## 🎯 **Overview**

Control classes implement the Page Object Model pattern, providing clean abstractions for web page interactions. This guide defines the standards for implementing maintainable and reusable control classes.

## 🏗️ **Architecture Principles**

### **Core Concepts**
- **Single Responsibility**: Each control handles one logical component
- **Encapsulation**: Hide Selenium complexity behind clean interfaces
- **Reusability**: Controls can be used across multiple test scenarios
- **Maintainability**: Centralized element management for UI changes

### **Inheritance Hierarchy**
```
ControlBase (Abstract Base)
├── Artifact (Individual artifact element)
├── Artifacts (Collection of artifacts)
├── Editor (Form/modal interactions)
├── Toolbar (Toolbar controls and filters)
├── Page (Page-level operations)
└── ...
```

## 🔧 **Base Class Implementation**

### **Standard ControlBase**
```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from radish import world

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
    
    def is_visible(self):
        """Check if element is visible."""
        try:
            element = self.locate()
            return element.is_displayed()
        except:
            return False
```

### **Key Methods**
- **`locate(timeout)`**: Find element with explicit wait
- **`exists()`**: Quick existence check
- **`is_visible()`**: Visibility verification
- **`click()`**: Safe element clicking
- **`text`**: Element text property

## 🎮 **Control Class Patterns**

### **Simple Element Control**
```python
class Button(ControlBase):
    """Control for button elements."""
    
    def __init__(self, xpath):
        super().__init__(xpath)
    
    def click(self):
        """Click the button safely."""
        element = self.locate()
        element.click()
    
    @property
    def text(self):
        """Get button text."""
        try:
            return self.locate().text.strip()
        except:
            return None
    
    @property
    def is_enabled(self):
        """Check if button is enabled."""
        try:
            return self.locate().is_enabled()
        except:
            return False
```

### **Form Field Control**
```python
class InputField(ControlBase):
    """Control for input field elements."""
    
    def __init__(self, xpath):
        super().__init__(xpath)
    
    def set_value(self, value):
        """Set the input field value."""
        element = self.locate()
        element.clear()
        element.send_keys(value)
    
    def get_value(self):
        """Get the current input field value."""
        try:
            return self.locate().get_attribute("value")
        except:
            return None
    
    def is_required(self):
        """Check if field is required."""
        try:
            return self.locate().get_attribute("required") is not None
        except:
            return False
```

### **Collection Control**
```python
class Artifacts(ControlBase):
    """Control for artifact collections."""
    
    def __init__(self):
        super().__init__("//div[contains(@class, 'artifact')]")
    
    def find(self, **filters):
        """Find artifacts matching criteria."""
        elements = self.locate_all()
        if not filters:
            return [Artifact.from_element(elem) for elem in elements]
        
        # Apply filters
        filtered = []
        for element in elements:
            artifact = Artifact.from_element(element)
            if self._matches_filters(artifact, filters):
                filtered.append(artifact)
        return filtered
    
    def find_one(self, **filters):
        """Find single artifact matching criteria."""
        results = self.find(**filters)
        return results[0] if results else None
    
    def count(self, **filters):
        """Count artifacts matching criteria."""
        return len(self.find(**filters))
    
    def _matches_filters(self, artifact, filters):
        """Check if artifact matches all filters."""
        for key, value in filters.items():
            if not hasattr(artifact, key) or getattr(artifact, key) != value:
                return False
        return True
```

## 🎨 **Design Patterns**

### **Property-Based Access**
```python
class StatusFilter(ControlBase):
    """Control for status filter dropdown."""
    
    def __init__(self):
        super().__init__("//select[@id='statusFilter']")
    
    @property
    def value(self):
        """Get current selected value."""
        try:
            select = Select(self.locate())
            return select.first_selected_option.text
        except:
            return None
    
    @property
    def options(self):
        """Get all available options."""
        try:
            select = Select(self.locate())
            return [option.text for option in select.options]
        except:
            return []
    
    def select(self, value):
        """Select option by value."""
        try:
            select = Select(self.locate())
            select.select_by_visible_text(value)
        except Exception as e:
            raise AssertionError(f"Failed to select '{value}': {e}")
```

### **Method Chaining**
```python
class Toolbar(ControlBase):
    """Control for toolbar operations."""
    
    def __init__(self):
        super().__init__("//div[@class='toolbar']")
    
    def filter_by_status(self, status):
        """Filter by status and return self for chaining."""
        self.status_filter.select(status)
        return self
    
    def filter_by_type(self, type_name):
        """Filter by type and return self for chaining."""
        self.type_filter.select(type_name)
        return self
    
    def refresh(self):
        """Refresh the view and return self for chaining."""
        self.refresh_button.click()
        return self
    
    # Usage: Toolbar().filter_by_status("open").filter_by_type("requirement").refresh()
```

## 🔍 **Error Handling**

### **Graceful Degradation**
```python
class Navigation(ControlBase):
    """Control for navigation elements."""
    
    def __init__(self):
        super().__init__("//nav")
    
    @property
    def current_page(self):
        """Get current page identifier."""
        try:
            # Try multiple strategies
            element = self.locate().find_element(By.CSS_SELECTOR, "[data-page]")
            return element.get_attribute("data-page")
        except:
            try:
                # Fallback to URL analysis
                url = world.driver.current_url
                if "/artifacts" in url:
                    return "artifacts"
                elif "/settings" in url:
                    return "settings"
                else:
                    return "unknown"
            except:
                return "unknown"
```

### **Assertion Integration**
```python
class VerificationFilter(ControlBase):
    """Control for verification filter."""
    
    def __init__(self):
        super().__init__("//select[@id='verificationFilter']")
    
    def assert_value(self, expected_value):
        """Assert current value matches expected."""
        actual_value = self.value
        assert actual_value == expected_value, \
            f"Verification filter expected '{expected_value}', got '{actual_value}'"
    
    def assert_contains_option(self, option):
        """Assert option is available."""
        options = self.options
        assert option in options, \
            f"Option '{option}' not found in {options}"
```

## 📏 **Code Quality Standards**

### **File Organization**
- **Maximum file size**: 100 lines
- **Maximum class size**: 50 lines
- **Maximum method size**: 15 lines
- **Maximum property size**: 10 lines

### **Naming Conventions**
- **Class names**: PascalCase (e.g., `StatusFilter`)
- **Method names**: snake_case (e.g., `select_value`)
- **Property names**: snake_case (e.g., `current_value`)
- **Private methods**: underscore prefix (e.g., `_matches_filters`)

### **Documentation Requirements**
- **Class docstring**: Purpose and usage
- **Method docstring**: Parameters, return values, exceptions
- **Property docstring**: What the property represents
- **Complex logic**: Inline comments for non-obvious code

## 🧪 **Testing Controls**

### **Unit Testing**
```python
def test_status_filter_select():
    """Test status filter selection."""
    # Mock setup
    mock_driver = Mock()
    mock_element = Mock()
    mock_select = Mock()
    
    with patch('radish.world.driver', mock_driver):
        mock_driver.find_element.return_value = mock_element
        with patch('selenium.webdriver.support.ui.Select', return_value=mock_select):
            filter_control = StatusFilter()
            filter_control.select("open")
            
            mock_select.select_by_visible_text.assert_called_once_with("open")
```

### **Integration Testing**
```python
def test_artifact_creation_flow():
    """Test complete artifact creation flow."""
    # Setup
    page = Page()
    editor = Editor()
    
    # Execute
    page.navigate_to_artifacts()
    editor.open()
    editor.set("summary", "Test artifact")
    editor.set("type", "requirement")
    editor.save()
    
    # Verify
    artifacts = Artifacts()
    assert artifacts.find_one(summary="Test artifact")
```

## 🚀 **Performance Considerations**

### **Lazy Loading**
```python
class LazyControl(ControlBase):
    """Control with lazy element loading."""
    
    def __init__(self, xpath):
        super().__init__(xpath)
        self._element = None
    
    def _get_element(self):
        """Get element, loading if necessary."""
        if self._element is None:
            self._element = self.locate()
        return self._element
    
    def click(self):
        """Click using cached element."""
        self._get_element().click()
```

### **Batch Operations**
```python
class BatchOperations(ControlBase):
    """Control for batch operations."""
    
    def select_all(self):
        """Select all visible items."""
        elements = self.locate_all()
        for element in elements:
            element.click()
    
    def get_all_texts(self):
        """Get text from all elements efficiently."""
        elements = self.locate_all()
        return [elem.text for elem in elements]
```

## 📚 **Best Practices**

### **Element Locators**
- **Prefer CSS selectors** over XPath for simple selections
- **Use data attributes** for test-specific elements
- **Avoid brittle selectors** that depend on text content
- **Keep selectors short** and readable

### **Wait Strategies**
- **Use explicit waits** for dynamic content
- **Avoid fixed delays** (time.sleep)
- **Implement custom wait conditions** for complex scenarios
- **Handle timeout gracefully** with meaningful errors

### **Control Composition**
- **Compose complex controls** from simpler ones
- **Use delegation** rather than inheritance for unrelated functionality
- **Keep controls focused** on single responsibility
- **Enable easy mocking** for testing

## 🎓 **Lessons Learned from Real Transformations**

### **Case Study: verification.py Control Classes**

#### **New Control Classes Created**
During the verification.py transformation, we created several new control classes that demonstrate best practices:

```python
class VerificationField(ControlBase):
    """Control for verification field elements."""
    
    def __init__(self):
        super().__init__("//select[@id='artifactVerification']")
    
    @property
    def value(self):
        """Get current verification field value."""
        try:
            element = self.locate()
            return element.get_attribute("value")
        except:
            return None
    
    def set_value(self, value):
        """Set verification field value."""
        element = self.locate()
        element.clear()
        element.send_keys(value)
```

#### **Key Design Decisions**
1. **Single Responsibility**: Each control handles one UI component
2. **Property-Based Access**: `value` property for getting current state
3. **Method-Based Actions**: `set_value()` for user interactions
4. **Graceful Error Handling**: Try-catch with sensible defaults
5. **Clean Interfaces**: Simple, intuitive method names

#### **Performance Optimizations Discovered**
- **Avoid Duplicate Control Calls**: Don't call `VerificationField().value` twice in same assertion
- **Reuse Control Instances**: Store control in variable when used multiple times
- **Eliminate Unnecessary Locating**: Cache elements when performing multiple operations

#### **Integration Patterns**
```python
# ✅ GOOD: Single control instance, multiple operations
verification = VerificationField()
assert verification.value == expected_value, \
    f"Expected '{expected_value}', got '{verification.value}'"

# ❌ BAD: Multiple control instantiations
assert VerificationField().value == expected_value, \
    f"Expected '{expected_value}', got '{VerificationField().value}'"
```

#### **Control Class Benefits**
- **Eliminated Direct Selenium**: 100% control-based implementation
- **Improved Maintainability**: Centralized element management
- **Enhanced Reusability**: Controls used across multiple step functions
- **Better Error Messages**: Context-aware assertions
- **Cleaner Step Functions**: One-liner implementations

---

*Following this guide ensures that control classes are maintainable, reusable, and provide clean abstractions for web page interactions.*
