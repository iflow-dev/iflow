Feature: Active Search Filter Borders
  As a user
  I want to see orange borders on active search filters
  So that I can easily identify which filters are currently applied

  Background:
    Given I go to home
    And the page has loaded completely

  Scenario: Type filter shows orange border when active
    When I select a type filter "requirement"
    Then the type filter should have an orange border
    When I clear the type filter
    Then the type filter should not have an orange border

  Scenario: Status filter shows orange border when active
    When I select a status filter "open"
    Then the status filter should have an orange border
    When I clear the status filter
    Then the status filter should not have an orange border

  Scenario: Category filter shows orange border when active
    When I enter "testing" in the category filter
    Then the category filter should have an orange border
    When I clear the category filter
    Then the category filter should not have an orange border

  Scenario: Search input shows orange border when active
    When I enter "test" in the search box
    Then the search input should have an orange border
    When I clear the search input
    Then the search input should not have an orange border

  Scenario: Multiple active filters show orange borders
    When I select a type filter "requirement"
    And I select a status filter "open"
    And I enter "test" in the search box
    Then the type filter should have an orange border
    And the status filter should have an orange border
    And the search input should have an orange border
    When I clear all filters
    Then no filters should have orange borders
