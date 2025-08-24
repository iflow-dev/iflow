@smoke
Feature: Test Status Filtering
    As a user
    I want to filter artifacts by status
    So that I can view artifacts with specific status values

    @tid:0103
    Scenario: Filter Artifacts by Status
        Given I go to home
        When I set the status filter to "open"
        Then I see the status filter is set to "open"
        Then I see only artifacts with status "open"
        When I clear the status filter
        Then I verify the status filter is cleared
        Then I see all artifacts again
