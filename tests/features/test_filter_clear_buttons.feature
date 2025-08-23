Feature: Filter Clear Buttons
  As a user
  I want to easily clear individual filters and all filters at once
  So that I can quickly reset my search criteria

  Background:
    Given I go to home
    And the page has loaded completely

  Scenario: Individual clear buttons appear when filters have values
    When I enter "test" in the search box
    Then the search clear button should be visible
    When I enter "testing" in the category filter
    Then the category clear button should be visible
    When I clear the search input
    Then the search clear button should not be visible
    When I clear the category filter
    Then the category clear button should not be visible

  Scenario: Clear all button is enabled when filters are active
    When I select a type filter "requirement"
    And I select a status filter "open"
    Then the clear all button should be enabled
    When I clear all filters
    Then the clear all button should be disabled

  Scenario: Clear all button clears all filters
    When I select a type filter "requirement"
    And I select a status filter "open"
    And I enter "test" in the search box
    And I enter "testing" in the category filter
    And I toggle the flag filter
    Then all filters should have active states
    When I click the clear all button
    Then no filters should have active states
    And the clear all button should be disabled

  Scenario: Individual clear buttons work correctly
    When I enter "test" in the search box
    And I enter "testing" in the category filter
    Then both clear buttons should be visible
    When I click the search clear button
    Then the search input should be cleared
    And the search clear button should not be visible
    And the category clear button should still be visible
    When I click the category clear button
    Then the category filter should be cleared
    And the category clear button should not be visible
