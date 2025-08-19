@smoke
Feature: Edit Dialog Button Text
    As a user
    I want to see the correct button text in the edit dialog
    So that I know whether I'm creating or editing an artifact

    Scenario: Create new artifact shows "Create" button
        Given I go to home
        When I create a new requirement
        Then I should see the edit dialog
        And the submit button should say "Create"
        And I cancel the artifact creation

    Scenario: Edit existing artifact shows "Save" button
        Given I go to home
        And I see artifacts displayed
        When I click the edit button on the first artifact
        Then I should see the edit dialog
        And the submit button should say "Save"
        And I cancel the artifact creation
