Feature: Status Field Default Values in Editor
  As a user
  I want the status field in the artifact editor to have proper default values
  So that I don't have to manually select the status every time

  Background:
    Given I am on the main page

  @smoke
  Scenario: Status field shows first status as default when creating new artifact
    When I create a new requirement
    Then I see the editor is open
    Then I see the status is "open"

    When I set the status to "done"
    Then I see the status is "done"

  @smoke
  Scenario: Status field shows actual status when editing existing artifact
    When I open the artifact with "00001"
    Then I see the editor is open
            And I see the status is "open"
    And I set the status to "done"
    And I see the status is "done"

  @smoke
  Scenario: Status field maintains selected value when saving artifact
    When I create a new requirement "test requirement"
    And I set the status to "in_progress"
    And I set the summary to "Test artifact with custom status"
    And I set the description to "Testing status persistence"
    And I save the article
    Then I see artifact with "test requirement" has status "in_progress"
