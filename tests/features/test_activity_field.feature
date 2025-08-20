Feature: Artifact Activity Field
    As an iflow user
    I want to have a text field as a one-liner
    So that I can track the latest activity of a ticket

    Scenario: Create artifact with activity field
        Given I go to home
        When I create a new requirement
        Then I should see the edit dialog
        And I should see an activity field
        And the activity field is empty

    Scenario: Edit artifact activity field
        Given I go to home
        And I see artifacts displayed
        When I edit an artifact
        Then I should see the edit dialog
        And I should see an activity field

    Scenario: Save artifact with activity information
        Given I go to home
        When I create a new requirement
        And I fill in the summary with "Test artifact with activity"
        And I fill in the description with "This artifact has activity tracking"
        And I set activity to "Initial development started"
        And I click the "Create" button
        Then I should see a success message
        And I open the artifact with title "Test artifact with activity"
        And I see the activity is "Initial development started"

    Scenario: Display activity field in artifact tile
        Given I go to home
        And I see artifacts displayed
        When I edit an artifact
        Then I should see the edit dialog
        And I should see an activity field

    Scenario: Update activity field on existing artifact
        Given I go to home
        And I see artifacts displayed
        When I edit an artifact
        And I set activity to "Testing in progress"
        And I click the "Save" button
        Then I should see a success message
        And I open the artifact with title "Test artifact with activity"
        And I see the activity is "Testing in progress"
