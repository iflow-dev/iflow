# Styleguide rules

## Python

-   All imports shall be done on module level
-   Step definitions itself must not use xpath and low-level selenium calls
-   Step definitions must use control-classes
-   driver handling:
    -   Whenever a Component needs access to driver, it should directly import world from radish
        and use this driver directly.
    -   driver shall never be passed through control functions
    -   no sanity checks on valid world.driver required, always expect it to be valid

## Creating steps

-   before creating new step definitions, always:
-   search all existing steps for similar steps that can do the job
-   unify steps by making them more flexible and reusing them
-   try to follow a natural language, but with formal elements
-   always distinguish between activity (when) and verification (then),
    but use only @step decorator
