Feature: Simple Page Title Check
  As a user
  I want to see the page title
  So that I know which page I'm on

  Scenario: Check Page Title Display
    Given I go to home
    Given I am on the main page
    Then the page title should be displayed
