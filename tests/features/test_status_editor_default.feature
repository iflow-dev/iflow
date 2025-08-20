Feature: Status Field Default Values in Editor
  As a user
  I want the status field in the artifact editor to have proper default values
  So that I don't have to manually select the status every time

  Background:
    Given I am on the main page
    And the artifact editor is available

  @smoke
  Scenario: Status field shows first status as default when creating new artifact
    When I create a new requirement
    Then I see the artifact creation form
    And the status field should show the first status from the status list
    And I should be able to change the status to a different value

  @smoke
  Scenario: Status field shows actual status when editing existing artifact
    Given I have an existing artifact with status "in_progress"
    When I edit the existing artifact
    Then I see the artifact edit form
    And the status field should show "in_progress"
    And I should be able to change the status to a different value

  @smoke
  Scenario: Status field maintains selected value when saving artifact
    When I create a new requirement
    And I set the status to "done"
    And I set the summary to "Test artifact with custom status"
    And I set the description to "Testing status persistence"
    And I save the new artifact
    Then I should see a success message
    And the new artifact should have status "done"
