Feature: Artifact Management
  As a project manager
  I want to create, edit, and manage artifacts
  So that project requirements are properly tracked

  Background:
    Given I go to home
    And I am on the artifacts page
    

  Scenario: Create New Artifact
    Given I click the "+ New Artifact" button
    When I fill in the artifact details
      | Field      | Value           |
      | Type       | requirement     |
      | Summary    | Test requirement |
      | Description| This is a test  |
      | Category   | Testing         |
      | Status     | open            |
    When I click "Save Artifact"
    Then a new artifact should be created
    Then it should appear in the artifacts list
    Then the modal should close

  Scenario: Edit Existing Artifact
    Given I am viewing an artifact
    When I click the "Edit" button
    When I modify the artifact description
    When I save the changes
    Then the artifact should be updated
    
    

  Scenario: Delete Artifact
    Given I am viewing an artifact
    When I click the "Delete" button
    When I confirm the deletion

  Scenario: Filter Artifacts by Type
    Given I am viewing all artifacts
    When I select "requirement" from the type filter
    Then only requirement artifacts should be displayed

  Scenario: Filter Artifacts by Status
    Given I am viewing all artifacts
    When I select "open" from the status filter
    Then only open artifacts should be displayed

  Scenario: Search Artifacts by Text
    Given I am viewing all artifacts
    When I enter "testing" in the search box
    Then only artifacts containing "testing" should be displayed

  Scenario: Filter by Category Link
    Given I am viewing all artifacts
    When I click on a category link in an artifact tile

  Scenario: Preserve Filter State After Edit
    Given I have filtered artifacts by type "requirement"
    When I edit an artifact
    When I save the changes
    Then the type filter should still show "requirement"
    Then only requirement artifacts should be displayed

  Scenario: Refresh Artifacts
    Given I have applied filters to the view
    When I click the "Refresh" button
    Then all filters should be reset
    Then filter dropdowns should show default values
