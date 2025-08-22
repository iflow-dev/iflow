@smoke
Feature: Version Display Verification
  As a user
  I want to see version information in the header
  So that I can identify the current application version

  Scenario: Verify Version Information in Header
    Given I am on the main page
    Then I see version information in the header
    And I do not see version information in the statistics line

  Scenario: Verify Statistics Line Without Version
    Given I am on the main page
    Then I see the statistics line
    And the statistics line does not contain version information
