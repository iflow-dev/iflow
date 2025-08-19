Feature: Refresh Button Filter Persistence
    As an iflow user
    I want my filter settings to persist when I refresh the view
    So that I don't lose my current filter state

    Scenario: Filter persists after refresh
        Given I go to home
        And I have applied a filter to the view
        When I click the refresh button
        Then the filter should still be applied
        And I should see only filtered items
        And the filter settings should remain visible in the status bar

    Scenario: Multiple filters persist after refresh
        Given I go to home
        And I have applied multiple filters to the view
        When I click the refresh button
        Then all filters should still be applied
        And I should see only items matching all filters
        And all filter settings should remain visible in the status bar

    Scenario: Filter state is preserved during refresh
        Given I go to home
        And I have applied a type filter to "requirement"
        And I have applied a status filter to "open"
        When I click the refresh button
        Then the type filter should show "requirement"
        And the status filter should show "open"
        And I should see only requirement artifacts with open status
