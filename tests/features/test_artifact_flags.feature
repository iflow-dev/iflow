@smoke
Feature: Artifact Flags
    As a user
    I want to flag artifacts for easy identification
    So that I can filter and find important artifacts quickly

    Scenario: Flag and unflag an artifact
        Given I am on the main page
        And I see artifacts displayed
        When I click the flag button on the first artifact
        Then the artifact should be flagged
        And the flag icon should be red
        When I click the flag button on the same artifact again
        Then the artifact should be unflagged
        And the flag icon should be grey

    Scenario: Filter by flagged artifacts
        Given I am on the main page
        And I have at least one flagged artifact
        When I click the flag filter button in the toolbar
        Then I should see only flagged artifacts
        And the flag filter button should be red
        When I click the flag filter button again
        Then I should see all artifacts again
        And the flag filter button should be grey

    Scenario: Create artifact with flag
        Given I am on the main page
        When I click the "Create" button
        And I fill in the artifact details
        And I check the "Flag this artifact" checkbox
        And I submit the form
        Then I should see the new artifact created
        And the new artifact should be flagged
        And the flag icon should be red
