# Cleanup Plan for `artifact_steps.py`

## 🎯 Objective
Apply the same cleanup patterns we used in `artifact_creation_steps.py` to eliminate boilerplate, improve code quality, and fix the step definition conflict.

## 🧹 Cleanup Patterns We Used Before

### 1. **Remove Unused Imports** (F401)
- Remove: `given`, `when`, `then`, `webdriver`, `time`, etc.
- Keep only what's actually used in the code
- Consolidate all imports to top-level

### 2. **Remove Redundant Docstrings** (F401)
- Remove all verbose docstrings that just repeat function names
- Keep code self-documenting through clear function names
- No maintenance overhead for documentation

### 3. **Remove Verbose Step Entry Logging**
- Remove all "Starting:", "Verifying:", "Searching:" log statements
- These add no value and create noise
- If needed later, implement centrally in hooks

### 4. **Remove Try-Catch Boilerplate** (E722)
- Remove all verbose try-catch blocks with logging and re-raising
- Replace with clean, direct code execution
- Better stack traces, cleaner code

### 5. **Consolidate Scattered Imports**
- Move all imports from within functions to top-level
- Organize by importance: standard library → third-party → local
- Use proper import sorting

### 6. **Use Centralized Logging**
- Replace `logging.getLogger(__name__)` with `logging_config.logger`
- Consistent with project's logging architecture
- No local logger creation

### 7. **Fix Spacing Issues** (E302, E303, W293)
- Add proper 2 blank lines between function definitions
- Remove trailing whitespace
- Fix inconsistent blank line spacing

## 📋 Phase-by-Phase Cleanup Plan

### **Phase 1: Fix Step Definition Conflict (Priority 1)**
- **Problem**: Duplicate step `i_set_field_to_value` conflicts with `artifact_creation_steps.py`
- **Solution**: Remove the duplicate step from `artifact_steps.py`
- **Reason**: Keep the cleaner, consolidated version in `artifact_creation_steps.py`
- **⚠️ CRITICAL**: This step MUST be done FIRST before any other cleanup
- **Why**: Without this, tests cannot run due to step registration conflicts

### **Phase 2: Apply Core Cleanup Patterns**
- **Remove unused imports**: Clean up import statements
- **Remove redundant docstrings**: Eliminate verbose documentation
- **Remove step entry logging**: Clean up verbose logging
- **Remove try-catch boilerplate**: Simplify exception handling
- **Consolidate imports**: Move all imports to top-level
- **Use centralized logging**: Replace with `logging_config.logger`

### **Phase 3: Optimize Functions**
- **Remove duplicate functions**: Two search box functions do the same thing
- **Simplify complex functions**: Remove unnecessary complexity
- **Remove empty functions**: Several functions just have `pass` statements
- **Consolidate similar functionality**: Group related steps

## 🔍 Specific Issues Identified

### **Duplicate Step Definition**
```python
# CONFLICT: This step exists in both files with same regex
@step("I set the {field} to {value:QuotedString}")
def i_set_field_to_value(step, field, value):
```

### **Unused Imports**
- `from radish import given, when, then` (only `step` is used)
- `from selenium import webdriver` (not used)
- `import time` (minimal usage, can be optimized)

### **Redundant Functions**
- `i_enter_text_in_search_box` and `i_type_text_in_search_box` (identical)
- Multiple filter functions with similar patterns

### **Empty/Pass Functions**
- `i_am_logged_in_as_user` (just `pass`)
- `changes_should_be_reflected_immediately` (just `pass`)
- Several other verification functions with `pass`

## 📊 Expected Results

### **Before vs After Metrics**
| **Metric** | **Before** | **After** | **Improvement** |
|------------|------------|-----------|-----------------|
| **Total Lines** | ~519 | ~200-250 | **~50-60% reduction** |
| **Functions** | ~40+ | ~25-30 | **~25-35% reduction** |
| **Try-catch blocks** | ~15+ | ~2-3 | **~80% reduction** |
| **Docstrings** | ~40+ | 0 | **100% reduction** |
| **Step entry logs** | ~20+ | 0 | **100% reduction** |
| **Import statements** | 20+ scattered | 8-10 organized | **~50% reduction** |

### **Quality Improvements**
- **Flake8 compliant**: Follows Python style guidelines
- **No step conflicts**: Eliminates duplicate definitions
- **Cleaner code**: No boilerplate, focused functionality
- **Better maintainability**: Easier to read, debug, and modify
- **Consistent with project**: Uses same patterns as other files

## 🚀 Implementation Order

1. **Fix conflict first** (Phase 1) - Critical for tests to run
   - **REMOVE DUPLICATE STEP**: Delete `i_set_field_to_value` from `artifact_steps.py`
   - This step conflicts with `artifact_creation_steps.py` and prevents tests from running
   - **VERIFY**: Check syntax and flake8 after this step
2. **Apply core cleanup** (Phase 2) - Major quality improvements
   - **VERIFY**: Check syntax and flake8 after each cleanup step
3. **Optimize functions** (Phase 3) - Polish and consolidation
   - **VERIFY**: Check syntax and flake8 after each cleanup step
4. **Test and verify** - Ensure cleanup doesn't break functionality

## ⚠️ Notes
- **Preserve functionality**: Don't change what the steps actually do
- **Maintain compatibility**: Keep the same step regex patterns (except duplicates)
- **Test thoroughly**: Run tests after each phase to catch issues early
- **Document changes**: Commit each phase separately for easy rollback

## 🔍 **VERIFICATION PROCESS (CRITICAL)**
- **After EACH cleanup step**: Check for syntax errors with `python -m py_compile`
- **After EACH cleanup step**: Check for flake8 violations with `python -m flake8`
- **Why**: Prevents introducing multiple formatting/syntax issues at once
- **Goal**: Catch and fix problems immediately, not accumulate them

## 💡 **LESSONS LEARNED FROM THIS CLEANUP**

### **What Worked Well:**
- **Systematic approach**: One function at a time with verification
- **Immediate feedback**: Catching issues before they compound
- **Clear patterns**: Following established cleanup rules consistently

### **Common Pitfalls to Avoid:**
- **Don't rush**: Multiple changes without verification = formatting mess
- **Check imports**: Scattered imports are everywhere in legacy code
- **Watch for duplicates**: Step conflicts are the #1 blocker for tests
- **Empty functions**: Many functions just have `pass` - can be removed

### **Quick Wins (Low Risk, High Impact):**
- **Remove docstrings**: Most just repeat function names
- **Remove try-catch**: Usually just log and re-raise (boilerplate)
- **Consolidate imports**: Move scattered imports to top
- **Remove unused imports**: F401 errors are easy to fix

### **Tricky Areas:**
- **Step conflicts**: Check for duplicate step definitions across files
- **Complex functions**: Some have nested logic that needs careful cleanup
- **Import dependencies**: Make sure you don't break import chains

### **Verification Commands (Keep Handy):**
```bash
# Syntax check
python -m py_compile artifact_steps.py

# Style check (first 20 errors)
python -m flake8 artifact_steps.py | head -20

# Full style check
python -m flake8 artifact_steps.py
```

### **When to Stop and Ask:**
- **Step conflicts**: If you see `SameStepError` - stop immediately
- **Import errors**: If imports can't be resolved - check the project structure
- **Complex logic**: If a function has deep nesting - might need user input
