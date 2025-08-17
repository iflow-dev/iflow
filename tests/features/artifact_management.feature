Feature: Artifact Management
  As a project manager
  I want to create, edit, and manage artifacts
  So that project requirements are properly tracked

  Background:
    Given I am on the artifacts page
    And I am logged in as a user

  Scenario: Create New Artifact
    Given I click the "+ New Artifact" button
    When I fill in the artifact details
      | Field      | Value           |
      | Type       | requirement     |
      | Summary    | Test requirement |
      | Description| This is a test  |
      | Category   | Testing         |
      | Status     | open            |
    And I click "Save Artifact"
    Then a new artifact should be created
    And it should appear in the artifacts list
    And the modal should close

  Scenario: Edit Existing Artifact
    Given I am viewing an artifact
    When I click the "Edit" button
    And I modify the artifact description
    And I save the changes
    Then the artifact should be updated
    And the changes should be reflected immediately
    And the current filter state should be preserved

  Scenario: Delete Artifact
    Given I am viewing an artifact
    When I click the "Delete" button
    And I confirm the deletion
    Then the artifact should be removed
    And it should no longer appear in the list

  Scenario: Filter Artifacts by Type
    Given I am viewing all artifacts
    When I select "requirement" from the type filter
    Then only requirement artifacts should be displayed
    And the filter dropdown should show "requirement"

  Scenario: Filter Artifacts by Status
    Given I am viewing all artifacts
    When I select "open" from the status filter
    Then only open artifacts should be displayed
    And the filter dropdown should show "open"

  Scenario: Search Artifacts by Text
    Given I am viewing all artifacts
    When I enter "testing" in the search box
    Then the results should filter in real-time
    And only artifacts containing "testing" should be displayed

  Scenario: Filter by Category Link
    Given I am viewing all artifacts
    When I click on a category link in an artifact tile
    Then the view should filter to show only artifacts with that category
    And the category filter input should be updated with the selected category

  Scenario: Preserve Filter State After Edit
    Given I have filtered artifacts by type "requirement"
    When I edit an artifact
    And save the changes
    Then the type filter should still show "requirement"
    And only requirement artifacts should be displayed

  Scenario: Refresh Artifacts
    Given I have applied filters to the view
    When I click the "Refresh" button
    Then all filters should be reset
    And all artifacts should be displayed
    And filter dropdowns should show default values
