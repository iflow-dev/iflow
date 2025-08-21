/**
 * Event Manager for Filter Controls
 * Handles event distribution between controls without affecting internal state updates
 */
class EventManager {
    constructor() {
        this.subscribers = new Map(); // eventType -> Set of callback functions
        this.eventQueue = []; // Queue of pending events
        this.isProcessing = false; // Flag to prevent recursive processing
        this.controlRegistry = new Map(); // controlId -> control instance
        
        // Event activity tracking
        this.eventStats = {
            totalEventsProcessed: 0,
            eventsProcessedThisSecond: 0,
            lastEventTime: 0,
            lastEventType: 'None',
            lastEventSource: 'None',
            eventTypes: new Map(), // eventType -> count
            recentEvents: [] // Array of last 10 events
        };
        
        // Reset event stats every second
        setInterval(() => {
            this.eventStats.eventsProcessedThisSecond = 0;
        }, 1000);
    }

    /**
     * Register a control with the event manager
     * @param {string} controlId - Unique identifier for the control
     * @param {Object} control - The control instance
     */
    registerControl(controlId, control) {
        this.controlRegistry.set(controlId, control);
        console.log(`EventManager: Registered control ${controlId}`);
    }

    /**
     * Unregister a control from the event manager
     * @param {string} controlId - Unique identifier for the control
     */
    unregisterControl(controlId) {
        this.controlRegistry.delete(controlId);
        console.log(`EventManager: Unregistered control ${controlId}`);
    }

    /**
     * Subscribe to a specific event type
     * @param {string} eventType - Type of event to subscribe to
     * @param {Function} callback - Function to call when event occurs
     * @param {string} subscriberId - Unique identifier for the subscriber
     */
    subscribe(eventType, callback, subscriberId) {
        if (!this.subscribers.has(eventType)) {
            this.subscribers.set(eventType, new Map());
        }
        
        const eventSubscribers = this.subscribers.get(eventType);
        eventSubscribers.set(subscriberId, callback);
        console.log(`EventManager: ${subscriberId} subscribed to ${eventType}`);
    }

    /**
     * Unsubscribe from a specific event type
     * @param {string} eventType - Type of event to unsubscribe from
     * @param {string} subscriberId - Unique identifier for the subscriber
     */
    unsubscribe(eventType, subscriberId) {
        if (this.subscribers.has(eventType)) {
            const eventSubscribers = this.subscribers.get(eventType);
            eventSubscribers.delete(subscriberId);
            console.log(`EventManager: ${subscriberId} unsubscribed from ${eventType}`);
        }
    }

    /**
     * Queue a user input event for distribution
     * @param {string} eventType - Type of event
     * @param {Object} eventData - Event data including source control and details
     */
    queueUserEvent(eventType, eventData) {
        console.log(`EventManager: queueUserEvent called with type: ${eventType}, data:`, eventData);
        
        const event = {
            type: eventType,
            data: eventData,
            timestamp: Date.now(),
            isUserEvent: true
        };
        
        this.eventQueue.push(event);
        console.log(`EventManager: Queued user event ${eventType} from ${eventData.sourceId}. Queue length: ${this.eventQueue.length}`);
        
        // Process the queue if not already processing
        if (!this.isProcessing) {
            console.log(`EventManager: Starting to process queue...`);
            this.processEventQueue();
        } else {
            console.log(`EventManager: Queue processing already in progress, event queued`);
        }
    }

    /**
     * Process all events in the queue sequentially
     */
    async processEventQueue() {
        console.log(`EventManager: processEventQueue called. isProcessing: ${this.isProcessing}, queueLength: ${this.eventQueue.length}`);
        
        if (this.isProcessing || this.eventQueue.length === 0) {
            console.log(`EventManager: Skipping queue processing. isProcessing: ${this.isProcessing}, queueLength: ${this.eventQueue.length}`);
            return;
        }

        this.isProcessing = true;
        console.log(`EventManager: Processing ${this.eventQueue.length} events`);

        while (this.eventQueue.length > 0) {
            const event = this.eventQueue.shift();
            console.log(`EventManager: Processing event: ${event.type}`);
            await this.distributeEvent(event);
        }

        this.isProcessing = false;
        console.log('EventManager: Event queue processing complete');
        
        // Trigger status update after processing events
        this.triggerStatusUpdate();
    }
    
    /**
     * Trigger a status update (can be overridden by subclasses)
     */
    triggerStatusUpdate() {
        // This method can be overridden to trigger UI updates
        console.log(`EventManager: Status update triggered. Total events: ${this.eventStats.totalEventsProcessed}`);
    }

    /**
     * Distribute a single event to all subscribers
     * @param {Object} event - Event object to distribute
     */
    async distributeEvent(event) {
        const { type, data, isUserEvent } = event;
        
        if (!this.subscribers.has(type)) {
            return; // No subscribers for this event type
        }

        const eventSubscribers = this.subscribers.get(type);
        console.log(`EventManager: Distributing ${type} to ${eventSubscribers.size} subscribers`);

        // Distribute to all subscribers
        for (const [subscriberId, callback] of eventSubscribers) {
            try {
                if (typeof callback === 'function') {
                    await callback(event);
                }
            } catch (error) {
                console.error(`EventManager: Error in subscriber ${subscriberId} for event ${type}:`, error);
            }
        }
        
        // Update event statistics
        this.eventStats.totalEventsProcessed++;
        this.eventStats.eventsProcessedThisSecond++;
        this.eventStats.lastEventTime = Date.now();
        this.eventStats.lastEventType = type;
        this.eventStats.lastEventSource = data.sourceId || 'Unknown';
        
        // Add to recent events (keep only last 10)
        const eventRecord = {
            type: type,
            source: data.sourceId || 'Unknown',
            timestamp: Date.now(),
            data: { ...data } // Copy data to avoid reference issues
        };
        
        this.eventStats.recentEvents.unshift(eventRecord); // Add to beginning
        if (this.eventStats.recentEvents.length > 10) {
            this.eventStats.recentEvents = this.eventStats.recentEvents.slice(0, 10); // Keep only last 10
        }
        
        // Track event type counts
        if (!this.eventStats.eventTypes.has(type)) {
            this.eventStats.eventTypes.set(type, 0);
        }
        this.eventStats.eventTypes.set(type, this.eventStats.eventTypes.get(type) + 1);
        
        console.log(`EventManager: Event processed. Total: ${this.eventStats.totalEventsProcessed}, This second: ${this.eventStats.eventsProcessedThisSecond}, Last: ${type} from ${this.eventStats.lastEventSource}`);
    }

    /**
     * Get a control instance by ID
     * @param {string} controlId - Unique identifier for the control
     * @returns {Object|null} The control instance or null if not found
     */
    getControl(controlId) {
        return this.controlRegistry.get(controlId) || null;
    }

    /**
     * Get all registered controls
     * @returns {Array} Array of all registered control instances
     */
    getAllControls() {
        return Array.from(this.controlRegistry.values());
    }

    /**
     * Clear all events and subscribers (useful for testing)
     */
    clear() {
        this.eventQueue = [];
        this.subscribers.clear();
        this.controlRegistry.clear();
        this.isProcessing = false;
        console.log('EventManager: Cleared all events and subscribers');
    }

    /**
     * Get current queue status
     * @returns {Object} Status information about the event queue
     */
    getStatus() {
        return {
            queueLength: this.eventQueue.length,
            isProcessing: this.isProcessing,
            subscriberCount: Array.from(this.subscribers.values()).reduce((total, subscribers) => total + subscribers.size, 0),
            controlCount: this.controlRegistry.size,
            totalEventsProcessed: this.eventStats.totalEventsProcessed,
            eventsPerSecond: this.eventStats.eventsProcessedThisSecond,
            lastEventTime: this.eventStats.lastEventTime,
            lastEventType: this.eventStats.lastEventType,
            lastEventSource: this.eventStats.lastEventSource,
            recentEvents: this.eventStats.recentEvents,
            eventTypeCounts: Object.fromEntries(this.eventStats.eventTypes)
        };
    }
}

// Create a global instance
window.eventManager = new EventManager();
