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

### **Phase 4: Function Removal (NEW)**
- **Target**: Remove redundant functions that are just `pass` statements
- **Process**: Remove function + remove all usages + verify with dry-run
- **Scoring**: Track LOCs and Steps removed with point multipliers

### **Phase 5: Multi-File Cleanup (NEW)**
- **Target**: Apply cleanup patterns to ALL step files in the project
- **Priority**: Start with smallest files (1-2 steps) for quick wins
- **Process**: Systematic cleanup of all step files using established patterns

### **Phase 5: Multi-File Cleanup (NEW)**
- **Target**: Apply cleanup patterns to ALL step files in the project
- **Priority**: Start with smallest files (1-2 steps) for quick wins
- **Process**: Systematic cleanup of all step files using established patterns

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
4. **Function removal** (Phase 4) - Remove redundant pass functions
   - **VERIFY**: Check syntax and flake8 after each function removal
5. **Multi-file cleanup** (Phase 5) - Apply patterns to all step files
   - **VERIFY**: Check syntax and flake8 after each file cleanup
6. **Test and verify** - Ensure cleanup doesn't break functionality

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

## 🎯 **FUNCTION REMOVAL LESSONS LEARNED (NEW)**

### **Critical Discovery: Not All Functions Are "Just Pass"**
- **❌ MISTAKE**: Assumed `i_edit_an_artifact` was just `pass` - it had real implementation!
- **✅ CORRECT**: Only remove functions that are truly empty or just `pass` statements
- **🔍 VERIFICATION**: Always check function content before removal

### **Function Removal Process (Refined)**
1. **Identify target function** - Must be truly empty/pass
2. **Remove function from Python file** - Count LOCs removed
3. **Remove ALL usages from feature files** - Count usages removed
4. **Verify with dry-run test** - Use `--tid XXXX --dry-run`
5. **Update score table** - Track LOCs and Steps (25x multiplier)
6. **Repeat for next function**

### **Pitfalls in Function Removal**
- **False assumptions**: Don't assume function names indicate empty functions
- **Incomplete cleanup**: Must remove BOTH function AND all usages
- **Missing verification**: Always run dry-run to ensure steps still found
- **Score tracking**: Keep accurate counts for LOCs and Steps removed

### **Verification Process for Function Removal**
```bash
# After each function removal, verify with:
./bdd-test --tid XXXX --dry-run

# Expected result: No step definition errors
# Don't care about other errors (like DRY_RUN assertions)
```

### **Scoring System for Function Removal**
- **LOCs**: Count lines removed from Python files + feature files
- **Steps**: Count functions removed (25 points each)
- **Total**: LOCs + (Steps × 25)
- **Example**: 3 LOCs + 1 Step = 3 + (1 × 25) = 28 points

### **What NOT to Remove**
- **Functions with real implementation** (even if simple)
- **Functions that interact with WebDriver**
- **Functions that perform actual test logic**
- **Functions that are called by other functions**

### **Best Practices for Function Removal**
- **Read the function first**: Don't assume based on name
- **Check for WebDriver calls**: `world.driver.find_element`, `click()`, etc.
- **Look for actual logic**: Even simple logic means keep the function
- **When in doubt**: Ask user or skip the function
- **Document removals**: Keep list of what was removed and why

### **Common Function Types to Remove**
- **Empty functions**: Just `pass` statements
- **Placeholder functions**: Comments like "This would need to be implemented"
- **Duplicate functions**: Identical functionality to other functions
- **Unused functions**: No usages found in any feature files

### **Common Function Types to KEEP**
- **WebDriver interactions**: Any function that clicks, types, or finds elements
- **Assertions**: Functions that verify test conditions
- **Setup functions**: Functions that prepare test state
- **Complex logic**: Functions with multiple operations or conditions

## 🔄 **STEP REMOVAL PROCESS - COMPLETE WORKFLOW**

### **Phase: Function Removal & Step Cleanup**
This phase systematically removes redundant step functions and their corresponding usages from feature files.

### **Step-by-Step Process**

#### **1. Function Identification**
```bash
# Search for functions in Python step files
grep_search --query "function_name" --include_pattern "tests/**/*.py"

# Look for functions that are just "pass" or empty
grep_search --query "def.*:\s*\n\s*pass" --include_pattern "tests/**/*.py"
```

#### **2. Usage Discovery**
```bash
# Search for step usages in feature files
grep_search --query "Step text from function" --include_pattern "features/**/*.feature"

# Example: For function "i_am_logged_in_as_user"
grep_search --query "I am logged in as a user" --include_pattern "features/**/*.feature"
```

#### **3. Function Removal**
- **Remove the function definition** from the Python step file
- **Count LOCs removed** (Python file lines)
- **Remove all step usages** from feature files
- **Count LOCs removed** (feature file lines)

#### **4. Verification Process**
```bash
# Run a dry-run test with any random test ID
./bdd-test --tid XXXX --dry-run

# Where XXXX is any random test ID (e.g., 0108, 0109, 0110)
# Expected: No step definition errors (steps still found)
# Don't care about other errors (DRY_RUN assertions, etc.)
```

#### **5. Score Table Update**
After each function removal, update the tracking table:

| **Pool** | **LOCs** | **Steps** | **Total** |
|----------|----------|-----------|-----------|
| **AI** | +X | +Y (25×Y) | LOCs + (Steps × 25) |
| **Claudio** | 0 | 0 (0) | 0 |
| **Common** | 0 | 0 (0) | 0 |

#### **6. Documentation**
Maintain a list of removed functions:
| **Function** | **LOCs Removed** | **Usages Removed** | **Files Modified** |
|--------------|------------------|-------------------|-------------------|
| `function_name` | **X** (Y Python + Z feature) | **N** | `file1.py`, `file2.feature` |

### **Verification Commands (Keep Handy)**
```bash
# Check for BDD Chrome processes (clean before testing)
ps aux | grep -i chrome | grep -v grep

# Kill BDD Chrome processes if needed
pkill -f "chromedriver"
pkill -f "Google Chrome.*--test-type=webdriver"

# Run verification test
./bdd-test --tid XXXX --dry-run

# Check syntax and style
python -m py_compile artifact_steps.py
python -m flake8 artifact_steps.py
```

### **Critical Success Factors**
1. **One function at a time** - Don't remove multiple functions without verification
2. **Complete cleanup** - Remove function + ALL usages
3. **Immediate verification** - Run dry-run test after each removal
4. **Accurate counting** - Track both Python and feature file LOCs
5. **Document everything** - Keep score table and removal list updated

### **When to Stop and Review**
- **After each batch** (e.g., "make 5 more functions and stop then")
- **When verification fails** - Step definition errors
- **When user requests review** - "stop for review"
- **When score milestones reached** - Track progress

### **Common Verification Errors (Expected)**
```bash
# This is EXPECTED in dry-run mode:
AssertionError: DRY_RUN.. test aborted

# This means the dry-run mechanism is working correctly
# The important thing is NO step definition errors
```

### **Success Metrics**
- **All steps found**: No `StepDefinitionNotFound` errors
- **Clean verification**: Dry-run completes without step issues
- **Accurate scoring**: LOCs and Steps properly counted
- **Complete cleanup**: No orphaned step usages in feature files

## 📁 **COMPLETE STEP FILE ANALYSIS & CLEANUP PRIORITIES**

### **Project-Wide Step File Inventory**
After comprehensive analysis using `git grep "@step\|@given\|@when\|@then"`, we discovered **19 step files** in the project.

### **Step Files by Number of Steps (Smallest to Largest)**

| **File** | **Steps** | **Lines** | **Cleanup Status** | **Priority** | **Estimated Effort** |
|----------|-----------|-----------|-------------------|--------------|---------------------|
| **`dropdown_selection_steps.py`** | **1 step** | 17 lines | ❌ **NOT CLEANED** | 🥇 **HIGHEST** | **5 minutes** |
| **`toolbar.py`** | **1 step** | 18 lines | ❌ **NOT CLEANED** | 🥇 **HIGHEST** | **5 minutes** |
| **`artifacts.py`** | **2 steps** | 40 lines | ❌ **NOT CLEANED** | 🥈 **HIGH** | **10 minutes** |
| **`edit_button_steps.py`** | **4 steps** | 66 lines | ❌ **NOT CLEANED** | 🥉 **MEDIUM** | **15 minutes** |
| **`version_display_steps.py`** | **4 steps** | 85 lines | ❌ **NOT CLEANED** | 🥉 **MEDIUM** | **15 minutes** |
| **`activity_field_steps.py`** | **5 steps** | 68 lines | ❌ **NOT CLEANED** | 🥉 **MEDIUM** | **15 minutes** |
| **`database_verification_steps.py`** | **5 steps** | 98 lines | ❌ **NOT CLEANED** | 🥉 **MEDIUM** | **15 minutes** |
| **`simple_steps.py`** | **5 steps** | 73 lines | ❌ **NOT CLEANED** | 🥉 **MEDIUM** | **15 minutes** |
| **`status_filtering_steps.py`** | **6 steps** | 168 lines | ❌ **NOT CLEANED** | 🥉 **MEDIUM** | **20 minutes** |
| **`artifact_creation_steps.py`** | **7 steps** | 65 lines | ✅ **ALREADY CLEANED** | ✅ **DONE** | **N/A** |
| **`refresh_filter_steps.py`** | **7 steps** | 154 lines | ❌ **NOT CLEANED** | 🥉 **MEDIUM** | **20 minutes** |
| **`status_editor_default_steps.py`** | **7 steps** | 139 lines | ❌ **NOT CLEANED** | 🥉 **MEDIUM** | **20 minutes** |
| **`artifact_flags_steps.py`** | **11 steps** | 170 lines | ❌ **NOT CLEANED** | 🥉 **MEDIUM** | **25 minutes** |
| **`verification_field_steps.py`** | **12 steps** | 128 lines | ❌ **NOT CLEANED** | 🥉 **MEDIUM** | **25 minutes** |
| **`filter_clear_buttons_steps.py`** | **16 steps** | 189 lines | ❌ **NOT CLEANED** | 🥉 **MEDIUM** | **30 minutes** |
| **`iteration_field_steps.py`** | **16 steps** | 176 lines | ❌ **NOT CLEANED** | 🥉 **MEDIUM** | **30 minutes** |
| **`active_filter_borders_steps.py`** | **19 steps** | 219 lines | ❌ **NOT CLEANED** | 🥉 **MEDIUM** | **35 minutes** |
| **`artifact_steps.py`** | **31 steps** | 344 lines | ✅ **PARTIALLY CLEANED** | ✅ **IN PROGRESS** | **N/A** |

### **Cleanup Strategy & Priority Matrix**

#### **🥇 TIER 1: Quick Wins (1-2 steps, <50 lines)**
- **`dropdown_selection_steps.py`** (1 step, 17 lines) - **Perfect starter**
- **`toolbar.py`** (1 step, 18 lines) - **Quick cleanup**
- **`artifacts.py`** (2 steps, 40 lines) - **Easy win**

**Why start here:**
- **Lowest risk** - small files, easy to understand
- **Highest impact** - quick wins build momentum
- **Good practice** - perfect for refining cleanup patterns
- **Fast results** - can complete 3 files in ~20 minutes

#### **🥈 TIER 2: Medium Effort (4-6 steps, 50-170 lines)**
- **`edit_button_steps.py`** (4 steps, 66 lines)
- **`version_display_steps.py`** (4 steps, 85 lines)
- **`activity_field_steps.py`** (5 steps, 68 lines)
- **`simple_steps.py`** (5 steps, 73 lines)

**Why tackle next:**
- **Moderate complexity** - manageable but not trivial
- **Good learning** - more complex patterns to practice
- **Steady progress** - consistent improvement

#### **🥉 TIER 3: Larger Files (7+ steps, 150+ lines)**
- **`status_filtering_steps.py`** (6 steps, 168 lines)
- **`refresh_filter_steps.py`** (7 steps, 154 lines)
- **`status_editor_default_steps.py`** (7 steps, 139 lines)

**Why save for later:**
- **Higher complexity** - need more experience
- **More risk** - larger files = more potential issues
- **Better preparation** - practice on smaller files first

### **Expected Cleanup Results by Tier**

#### **TIER 1 (3 files):**
- **Total lines:** 75 → ~45 (**40% reduction**)
- **Total steps:** 4 → 4 (**No reduction, just cleanup**)
- **Time investment:** ~20 minutes
- **Risk level:** **Very Low**

#### **TIER 2 (4 files):**
- **Total lines:** 292 → ~200 (**30% reduction**)
- **Total steps:** 19 → 19 (**No reduction, just cleanup**)
- **Time investment:** ~60 minutes
- **Risk level:** **Low**

#### **TIER 3 (3 files):**
- **Total lines:** 461 → ~300 (**35% reduction**)
- **Total steps:** 20 → 20 (**No reduction, just cleanup**)
- **Time investment:** ~75 minutes
- **Risk level:** **Medium**

### **Overall Project Impact**
- **Total step files:** 19
- **Files already cleaned:** 1 (5%)
- **Files to clean:** 18 (95%)
- **Total estimated time:** ~155 minutes (~2.5 hours)
- **Expected total LOC reduction:** ~25-30%
- **Expected quality improvement:** **Significant**

### **Next Steps Recommendation**
1. **Start with TIER 1** - Build confidence and momentum
2. **Move to TIER 2** - Apply learned patterns
3. **Finish with TIER 3** - Master complex scenarios
4. **Continuous verification** - Check syntax and flake8 after each file
5. **Regular commits** - Save progress frequently

**This systematic approach ensures steady progress with minimal risk!** 🚀

## 📁 **COMPLETE STEP FILE ANALYSIS & CLEANUP PRIORITIES**

### **Project-Wide Step File Inventory**
After comprehensive analysis using `git grep "@step\|@given\|@when\|@then"`, we discovered **19 step files** in the project.

### **Step Files by Number of Steps (Smallest to Largest)**

| **File** | **Steps** | **Lines** | **Cleanup Status** | **Priority** |
|----------|-----------|-----------|-------------------|--------------|
| **`dropdown_selection_steps.py`** | **1 step** | 17 lines | ❌ **NOT CLEANED** | 🥇 **HIGHEST** |
| **`toolbar.py`** | **1 step** | 18 lines | ❌ **NOT CLEANED** | 🥇 **HIGHEST** |
| **`artifacts.py`** | **2 steps** | 40 lines | ❌ **NOT CLEANED** | 🥈 **HIGH** |
| **`edit_button_steps.py`** | **4 steps** | 66 lines | ❌ **NOT CLEANED** | 🥉 **MEDIUM** |
| **`version_display_steps.py`** | **4 steps** | 85 lines | ❌ **NOT CLEANED** | 🥉 **MEDIUM** |
| **`artifact_creation_steps.py`** | **7 steps** | 65 lines | ✅ **ALREADY CLEANED** | ✅ **DONE** |
| **`artifact_steps.py`** | **31 steps** | 344 lines | ✅ **PARTIALLY CLEANED** | ✅ **IN PROGRESS** |

### **Cleanup Strategy & Priority Matrix**

#### **🥇 TIER 1: Quick Wins (1-2 steps, <50 lines)**
- **`dropdown_selection_steps.py`** (1 step, 17 lines) - **Perfect starter**
- **`toolbar.py`** (1 step, 18 lines) - **Quick cleanup**
- **`artifacts.py`** (2 steps, 40 lines) - **Easy win**

**Why start here:**
- **Lowest risk** - small files, easy to understand
- **Highest impact** - quick wins build momentum
- **Good practice** - perfect for refining cleanup patterns
- **Fast results** - can complete 3 files in ~20 minutes

### **Next Steps Recommendation**
1. **Start with TIER 1** - Build confidence and momentum
2. **Move to TIER 2** - Apply learned patterns
3. **Finish with TIER 3** - Master complex scenarios
4. **Continuous verification** - Check syntax and flake8 after each file
5. **Regular commits** - Save progress frequently
