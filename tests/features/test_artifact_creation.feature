@smoke
Feature: Test Artifact Creation
  As a user
  I want to create new artifacts from the search view
  So that I can add new items to the project

  Scenario: Create New Artifact from Search View
    Given I go to home
    When I create a new requirement
    Then I see the artifact creation form
    When I set the type to "requirement"
    When I set the summary to "Test requirement for BDD testing"
    When I set the description to "This is a test requirement created during BDD test execution"
    When I set the status to "open"
    When I save the new artifact
    Then I see the new artifact in the list
    Then I do not see the artifact creation form
    # Note: The artifact ID is saved in world for use in subsequent scenarios

  Scenario: Cancel Artifact Creation
    Given I go to home
    When I create a new requirement
    Then I see the artifact creation form
    When I set the type to "requirement"
    When I set the summary to "This will be cancelled"
    When I set the description to "This description will not be saved"
    When I set the status to "in_progress"
    When I cancel the artifact creation
    Then I do not see the artifact creation form
    Then I remain on the search view
    When I search for artifacts with "This will be cancelled"
    Then I see 0 search results
