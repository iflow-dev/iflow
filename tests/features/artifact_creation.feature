@smoke
@feature:0001
Feature: Test Artifact Creation
  As a user
  I want to create new artifacts from the search view
  So that I can add new items to the project

  @tid:0101
  Scenario: Create New Artifact from Search View
    Given I go to home
    When I create a requirement
    And I set the summary to "Test requirement for BDD testing"
    And I set the description to "This is a test requirement created during BDD test execution"
    And I set the status to "in_progress"
    When I save the artifact
    Then I see the artifact "Test requirement for BDD testing"

  @tid:0102
  Scenario: Cancel Artifact Creation
    Given I go to home
    When I create a requirement
    And I set the summary to "This will be cancelled"
    And I set the description to "This description will not be saved"
    And I set the status to "in_progress"
    When I cancel the artifact creation
    Then I am on the main page
    Then I do not see the artifact "This will be cancelled"
