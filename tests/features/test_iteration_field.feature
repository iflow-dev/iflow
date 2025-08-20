Feature: Artifact Iteration Field
    As an iflow user
    I want to specify the iteration in which an artifact is supposed to be resolved
    So that I can track project planning and delivery timelines

    Scenario: Create artifact with iteration field
        Given I go to home
        When I create a requirement
        Then I should see the edit dialog
        Then the field iteration is set to ""

    Scenario: Edit artifact iteration field
        Given I go to home
        And I see artifacts displayed
        When I edit the first artifact
        Then I should see the edit dialog
        And I fill the iteration field with "Sprint 1"

    Scenario: Save artifact with iteration information
        Given I go to home
        When I create a requirement
        And I fill in the summary with "Test artifact with iteration"
        And I fill in the description with "This artifact has iteration tracking"
        And I fill in the iteration field with "Sprint 3"
        And I click the Create button
        Then I should see a success message
        And the artifact should be saved with iteration "Sprint 3"

    Scenario: Display iteration field in artifact tile
        Given I go to home
        And there is an artifact with iteration "Sprint 2"
        When I open the artifact with title "Test artifact with iteration"
        Then I see the iteration is set to "Sprint 2"

    Scenario: Update iteration field on existing artifact
        Given I go to home
        And there is an existing artifact
        When I click the edit button on the artifact
        And I update the iteration field to "Sprint 4"
        And I click the Save button
        Then I should see a success message
        And the artifact should be updated with new iteration "Sprint 4"
