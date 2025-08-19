@smoke
Feature: Toolbar Refresh Functionality
    As a user
    I want to refresh the artifacts in the search view
    So that I can see the latest data without reloading the page

    Scenario: Refresh artifacts using toolbar refresh button
        Given I go to home
        And I see artifacts displayed
        When I click the refresh button in the toolbar
        Then the artifacts should be refreshed
        And I should see the latest data
