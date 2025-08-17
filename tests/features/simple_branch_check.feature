Feature: Simple Branch Display Check
  As a user
  I want to see the current branch in the status line
  So that I know which branch I'm working on

  Scenario: Check Master Branch Display
    Given I am on the artifacts page
    Then the status line should show "Branch: master"
