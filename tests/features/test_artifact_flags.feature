@smoke
Feature: Artifact Flags
    As a user
    I want to flag artifacts for easy identification
    So that I can filter and find important artifacts quickly

    Scenario: Flag and unflag an artifact
        Given I reset the database to master
        And I go to home
        And I see artifacts displayed
        When I flag artifact #00001
        Then the artifact should be flagged
        When I flag artifact #00001
        Then the artifact should be unflagged

    Scenario: Filter by flagged artifacts
        Given I reset the database to master
        And I go to home
        And I flag artifact #00001
        And I flag artifact #00002
        When I click the flag filter button in the toolbar
        Then I should see only flagged artifacts
        And the flag filter button should be red
        When I click the flag filter button again
        Then I should see all artifacts again
        And the flag filter button should be grey

    Scenario: Create artifact with flag
        Given I reset the database to master
        And I go to home
        When I click the "Create" button
        And I fill in the artifact details
            | Field        | Value                    |
            | Type         | requirement              |
            | Summary      | Test artifact with flag  |
            | Description  | Test artifact for flag functionality |
            | Category     | Test                     |
            | Status       | open                     |
        And I check the "Flag this artifact" checkbox
        And I submit the form
        Then I should see the new artifact created
        And the new artifact should be flagged
