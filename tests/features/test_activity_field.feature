Feature: Artifact Activity Field
    As an iflow user
    I want to have a text field as a one-liner
    So that I can track the latest activity of a ticket

    Scenario: Create artifact with activity field
        Given I go to home
        When I click the create button
        Then I should see the edit dialog
        And I should see an activity field
        And the activity field should be empty by default

    Scenario: Edit artifact activity field
        Given I go to home
        And I see artifacts displayed
        When I click the edit button on the first artifact
        Then I should see the edit dialog
        And I should see an activity field
        And I can edit the activity field

    Scenario: Save artifact with activity information
        Given I go to home
        When I click the create button
        And I fill in the summary with "Test artifact with activity"
        And I fill in the description with "This artifact has activity tracking"
        And I fill in the activity field with "Initial development started"
        And I click the Create button
        Then I should see a success message
        And the artifact should be saved with activity "Initial development started"

    Scenario: Display activity field in artifact tile
        Given I go to home
        And there is an artifact with activity "Code review completed"
        When I view the artifact tile
        Then I should see the activity information displayed
        And it should show "Code review completed"

    Scenario: Update activity field on existing artifact
        Given I go to home
        And there is an existing artifact
        When I click the edit button on the artifact
        And I update the activity field to "Testing in progress"
        And I click the Save button
        Then I should see a success message
        And the artifact should be updated with new activity "Testing in progress"
