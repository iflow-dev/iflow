@smoke
Feature: Test Artifact Creation
  As a user
  I want to create new artifacts from the search view
  So that I can add new items to the project

  @tid:0101
  Scenario: Create New Artifact from Search View
    Given I go to home
    When I create a new requirement
    When I set the type to "requirement"
    And I set the summary to "Test requirement for BDD testing"
    And I set the description to "This is a test requirement created during BDD test execution"
    And I set the status to "open"
    When I save the article
    # TODO: Then I see 2 artifacts
    # TODO: replace step below
    Then I see the new artifact in the list
    # Note: The artifact ID is saved in world for use in subsequent scenarios

  @tid:0102
  Scenario: Cancel Artifact Creation
    Given I go to home
    When I create a new requirement
    When I set the type to "requirement"
    And I set the summary to "This will be cancelled"
    And I set the description to "This description will not be saved"
    And I set the status to "in_progress"
    When I cancel the artifact creation
    Then I am on the main page
    When I search for artifacts with "This will be cancelled"
    Then I see 0 search results
