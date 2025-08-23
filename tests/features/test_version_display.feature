@smoke
Feature: Version Display Verification
  As a user
  I want to see version information in the header
  So that I can identify the current application version

  @tid:0104
  Scenario: Verify Version Information in Header
    Given I go to home
    Then I see version information in the header
    And I do not see version information in the statistics line

  @tid:0105
  Scenario: Verify Statistics Line Without Version
    Given I go to home
    Then I see the statistics line
    And the statistics line does not contain version information
