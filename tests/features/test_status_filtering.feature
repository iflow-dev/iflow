@smoke
Feature: Test Status Filtering
    As a user
    I want to filter artifacts by status
    So that I can view artifacts with specific status values

    Scenario: Filter Artifacts by Status
        Given I go to home
        When I filter by status "open"
        Then I see artifacts with status "open"
        When I clear the status filter
        Then I see all artifacts again
