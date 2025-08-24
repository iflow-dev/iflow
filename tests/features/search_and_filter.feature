Feature: Search and Filter Functionality
  As a user
  I want to quickly find relevant artifacts
  So that I can work efficiently

  Background:
    Given I go to home
    And I am on the artifacts page
    

  @tid:0123
  Scenario: Real-time Search
    When I type "BDD" in the search box
    Then only artifacts containing "BDD" should be displayed
    # And the search results should update as I type

  Scenario: Search with No Results
    # When I search for "nonexistentterm"
    # Then no artifacts should be displayed
    # And a "No artifacts found" message should appear

  Scenario: Clear Search
    # Given I have searched for "testing"
    # And the results are filtered
    #     When I clear the search box
    # And the filter should be removed

  # Scenario: Type Filter - Requirements
    # Given I am viewing all artifacts
    # When I select "requirement" from the type filter
    # Then only requirement artifacts should be displayed
    # And the artifact count should update accordingly

  # Scenario: Type Filter - Tasks
    # Given I am viewing all artifacts
    # When I select "task" from the type filter
    # Then only task artifacts should be displayed
    # And the artifact count should update accordingly

  # Scenario: Status Filter - Open
    # Given I am viewing all artifacts
    # When I select "open" from the status filter
    # Then only open artifacts should be displayed
    # And the artifact count should update accordingly

  # Scenario: Status Filter - Done
    # Given I am viewing all artifacts
    # When I select "done" from the status filter
    # Then only done artifacts should be displayed
    # And the artifact count should update accordingly

  # Scenario: Category Filter Input
    # Given I am viewing all artifacts
    # When I type "Security" in the category filter
    # Then only artifacts with "Security" category should be displayed
    # And the filter should work with partial matches

  # Scenario: Multiple Filter Combination
    # Given I have filtered by type "requirement"
    # When I also filter by status "open"
    # Then the view should show only open requirement artifacts
    # And both filter dropdowns should show their selected values

  # Scenario: Reset All Filters
    # Given I have applied multiple filters
    # When I click the "Refresh" button
    # Then all filters should be reset to default values
    # And all artifacts should be displayed
