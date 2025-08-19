Feature: Artifact Activity Field - Basic Test
    As an iflow user
    I want to have a text field as a one-liner
    So that I can track the latest activity of a ticket

    Scenario: Create artifact with activity field
        Given I go to home
        When I click the create button
        Then I should see the edit dialog
        And I should see an activity field
        And the activity field should be empty by default
