Feature: Status Onliner Display
  As a iflow user
  I want to have a text file status as a onliner
  In order to track the latest status of a ticket

  Background:
    Given I am on the artifacts view
    And I have artifacts with different statuses

  Scenario: Status is displayed as a one-liner text
    When I view an artifact tile
    Then I should see the status displayed as a one-liner text
    And the status text should be clearly visible in the tile content

  Scenario: Status onliner shows current status
    Given I have an artifact with status "in progress"
    When I view the artifact tile
    Then I should see "in progress" displayed as a one-liner text
    And the status onliner should be separate from the status header

  Scenario: Status onliner updates when status changes
    Given I have an artifact with status "open"
    When I change the artifact status to "done"
    Then the status onliner should display "done"
    And the change should be immediately visible
