# iFlow Glossary

This glossary contains definitions for iFlow-specific terms and concepts.

## A

### Active State
A filter state where the filter is actively applying its value and affecting the application's data or view. Filters in active state typically have visual indicators like orange borders.

### Architecture
The overall design and structure of the iFlow system, including component relationships, data flow, and system organization.

## B

### Base Class
A fundamental class that provides common functionality to other classes. In iFlow, `FilterControl` is the base class for all filter components.

## C

### Clear Button
A UI element that allows users to reset a filter to its default state, typically removing any applied values.

### Component
A reusable piece of functionality in the iFlow system, such as filters, event managers, or UI controls.

### Control ID
A unique identifier assigned to each filter control instance, used for event routing and state management.

## D

### Disabled State
A filter state where the filter is temporarily inactive but retains its configuration. Filters in disabled state have muted visual appearance.

### Dropdown Filter
A filter component that presents options in a selectable dropdown menu, allowing users to choose from predefined values.

## E

### Event
A message that represents something that has happened in the system, such as user interactions or state changes.

### Event Manager
A central system component that handles event queuing, distribution, and routing between different parts of the application.

### Event Queue
A sequential list of events waiting to be processed by the Event Manager.

### Event-Driven Architecture
A system design pattern where components communicate through events rather than direct method calls, promoting loose coupling.

## F

### Filter
A component that allows users to narrow down or focus on specific data or content within the application.

### Filter Control
The base class for all filter components, providing common functionality like state management and event handling.

### Filter Footer
The clickable area of a filter that displays the filter name and allows users to cycle through filter states.

### Filter Manager
A system component that coordinates multiple filters and manages their collective impact on the application.

### Filter State
The current operational mode of a filter, which can be active, inactive, or disabled.

### Filter Type
A category identifier for filters, such as "search", "status", or "category", used for organization and event routing.

## G

### Glossary
A reference document containing definitions of terms and concepts used within the iFlow system.

## I

### Inactive State
A filter state where the filter is not applying any values and has no visual emphasis.

### iFlow
The main application framework that provides filtering, state management, and UI components.

## M

### Markdown
A lightweight markup language used for creating documentation and content in the iFlow system.

### MkDocs
A static site generator used to create the iFlow documentation site.

## P

### Plugin
An extension that adds functionality to the MkDocs documentation system, such as the ezglossary plugin.

### Puppeteer
A Node.js library used for automated testing of the iFlow frontend components in headless browsers.

## S

### SelectFilter
A dropdown-based filter component that extends FilterControl and provides selection functionality.

### State Cycling
The process of transitioning a filter through different states (active → disabled → active) by clicking on the filter footer.

### State Machine
A computational model that defines the states a filter can be in and the transitions between those states.

## T

### TextInputFilter
A text-based filter component that extends FilterControl and provides text input functionality.

### Testing
The process of verifying that iFlow components work correctly through automated and manual verification methods.

## U

### User Interaction
Any action taken by a user that triggers events in the system, such as typing, clicking, or selecting options.

## V

### Visual State
The appearance and styling of a filter component based on its current state and user interactions.

