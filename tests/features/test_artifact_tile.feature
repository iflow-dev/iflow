@smoke
Feature: Test Artifact Tile
  As a user
  I want to verify that specific artifacts are visible
  So that I can confirm the page is working correctly

  Scenario: Verify Artifact Tile Exists
    Given I go to home
    Then I see the artifact #00004

  Scenario: Verify Artifact Tile does not Exist
    Given I go to home
    Then I do not see the artifact #99999