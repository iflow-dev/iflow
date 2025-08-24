Feature: Database Initialization
    As a developer
    I want to ensure the database starts with exactly one artifact
    So that tests have a clean, predictable starting state

    @tid:0138
    Scenario: Verify database has exactly one artifact after initialization
        Given I go to home
        When I check the database state
        Then I see 1 search results
        And the artifact should have ID "00001"
        And the artifact should have summary "Initial artifact"
        And the artifact should have type "requirement"
        And the artifact should have status "open"
        And the artifact should not be flagged

    @tid:0139
    Scenario: Verify database repository tags
        Given I go to home
        When I check the database repository
        Then the repository should have tag "base"
        And the repository should have tag "v0.0.0"
        And the repository should have exactly 1 commit
