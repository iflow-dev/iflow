# requirements

## template.html

1. run test button:
    - name: run
    - turns yellow when running and shows "running"
    - turns green with name "PASSED" when test passed
    - shows a "redo" icon to rerun the test
    - turns red with "FAILED" when test fails
    - the button shall be a reusable component
    - the button shall be placed on the top right of the test tile

2. button "run all" runs all tests

3. show only test results when test is failed

## test automation infrastructure

4. the test automation infrastracture shall be resusable. The template.html
   shall be a reusable component to run javascript based tests in an automated
   environment.

   Hint: The current tests for the search input can be considered as a test suite
   and runs in the test automation infrastructure. The template.html detects the test cases
   or offers a way to register them so that i can say something like:

        unit_test --suite search-filter

    or

        unit-test --suite icon-filter [dont implement yet]


