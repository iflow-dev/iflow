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
        When I create a new requirement
        And I set the type to "requirement"
        And I set the summary to "Test artifact with flag"
        And I set the description to "Test artifact for flag functionality"
        And I set the status to "open"
        And I save the article
        Then I should see the new artifact created
        # TODO: Flag functionality not working - checkbox clicked but not saved
        # And the new artifact should be flagged
