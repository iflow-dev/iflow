@smoke
Feature: Dropdown Selection in Artifact Editor
    As a user
    I want to be able to select values from dropdowns in the artifact editor
    So that I can create and edit artifacts properly

    Background:
        Given I go to home
        And I am on the main page
        And I click the "Create" button

    Scenario: Select artifact type from dropdown
        Given the artifact creation modal is open
        When I click on the "Type" dropdown
        And I click on "📄 Requirement" option
        Then the dropdown should close
        And the selected value should be "📄 Requirement"
        And the original select element should have value "requirement"

    Scenario: Select artifact status from dropdown
        Given the artifact creation modal is open
        When I click on the "Status" dropdown
        And I click on "🟢 Open" option
        Then the dropdown should close
        And the selected value should be "🟢 Open"
        And the original select element should have value "open"

    Scenario: Select different artifact type
        Given the artifact creation modal is open
        When I click on the "Type" dropdown
        And I click on "✅ Task" option
        Then the dropdown should close
        And the selected value should be "✅ Task"
        And the original select element should have value "task"

    Scenario: Cancel dropdown selection by clicking outside
        Given the artifact creation modal is open
        When I click on the "Type" dropdown
        And I click outside the dropdown
        Then the dropdown should close
        And no value should be selected
