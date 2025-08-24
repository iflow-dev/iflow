Feature: Refresh Button Filter Persistence
    As an iflow user
    I want my filter settings to persist when I refresh the view
    So that I don't lose my current filter state

    @tid:0149
    Scenario: Filter persists after refresh
        Given I go to home
        And I filter for type "requirement"
        When I refresh the view
        Then I see the type filter is set to "requirement"
        And I only see requirement items

    @tid:0150
    Scenario: Multiple filters persist after refresh
        Given I go to home
        And I filter for type "requirement"
        And I filter for status "open"
        When I refresh the view
        Then I see the type filter is set to "requirement"
        And I see the status filter is set to "open"
        And I only see requirement items with open status

    @tid:0151
    Scenario: Filter state is preserved during refresh
        Given I go to home
        And I filter for type "requirement"
        And I filter for status "open"
        When I refresh the view
        Then I see the type filter is set to "requirement"
        And I see the status filter is set to "open"
        And I only see requirement items with open status
