# TODO:
# - use 4 space indents
#
Feature: Status Field Default Values in Editor
  As a user
  I want the status field in the artifact editor to have proper default values
  So that I don't have to manually select the status every time

  Background:
    Given I go to home

  @smoke @tid:0111
  Scenario: Status field shows first status as default when creating new artifact
    When I create a new requirement
    Then I see the editor is open
    Then I see the status is "open"

    When I set the status to "done"
    Then I see the status is "done"

  @smoke @tid:0112
  Scenario: Status field shows actual status when editing existing artifact

    When I open the artifact 00001
    Then I see the editor is open
    When I set the status to "open"
    Then I see the status is "open"

    When I save the artifact
    Then I see artifact 00001 has status "open"

    When I open the artifact 00001
    Then I see the status is "open"

    When I set the status to "done"
    When I save the artifact
    Then I see artifact 00001 has status "done"

    When I open the artifact 00001
    Then I see the status is "done"

  @smoke @tid:0113
  Scenario: Status field maintains selected value when saving artifact

    When I create a new requirement "test requirement"
    And I set the status to "in_progress"
    And I set the summary to "Test artifact with custom status"
    And I set the description to "Testing status persistence"
    And I save the artifact
 
    When I open the artifact "test requirement"
    Then I see the status is "in_progress"
