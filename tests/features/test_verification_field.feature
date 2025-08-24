Feature: Artifact Verification Field
    As an iflow user
    I want to specify the verification method for each ticket individually in a custom field
    So that I can give precise instructions how to test it

    @tid:0152
    Scenario: Create artifact with verification field
        Given I go to home
        When I click the create button
        Then I should see the edit dialog
        And I should see a verification field
        And the verification field should have default value "BDD"

    @tid:0153
    Scenario: Edit artifact verification field
        Given I go to home
        And I see artifacts displayed
        When I click the edit button on the first artifact
        Then I should see the edit dialog
        And I should see a verification field
        And I can edit the verification field

    @tid:0154
    Scenario: Save artifact with custom verification method
        Given I go to home
        When I click the create button
        And I set the summary to "Test artifact with custom verification"
        And I set the description to "This artifact has a custom verification method"
        And I set the verification field to "Manual Testing"
                        And I save the artifact
        Then I should see a success message
        And the artifact should be saved with verification method "Manual Testing"

    @tid:0155
    Scenario: Display verification field in artifact tile
        Given I go to home
        Then I should see the verification method displayed
        And it should show "Unit Tests"
