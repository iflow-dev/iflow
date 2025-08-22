/**
 * Status Line Management Class
 * Handles the status line at the bottom of the window
 */
class StatusLine {
    constructor() {
        this.statusLine = null;
        this.lastMessageElement = null;
        this.filteredCountElement = null;
        this.initialized = false;
    }
    
    /**
     * Initialize the status line
     */
    initialize() {
        try {
            this.statusLine = document.getElementById('status-line');
            this.lastMessageElement = document.getElementById('last-message');
            this.filteredCountElement = document.getElementById('filtered-count');
            
            if (this.statusLine && this.lastMessageElement && this.filteredCountElement) {
                this.initialized = true;
                console.log('Status line initialized');
            } else {
                console.error('Status line elements not found');
            }
        } catch (error) {
            console.error('Error initializing status line:', error);
        }
    }
    
    /**
     * Show a message in the status line
     */
    showMessage(message, type = 'info') {
        if (!this.initialized || !this.lastMessageElement) return;
        
        try {
            // Remove existing type classes
            this.lastMessageElement.classList.remove('info', 'success', 'error', 'warning');
            
            // Add the new type class
            this.lastMessageElement.classList.add(type);
            
            // Update the message text
            this.lastMessageElement.textContent = message;
            
            // Update status line styling based on type
            if (this.statusLine) {
                this.statusLine.className = `status-line ${type}`;
            }
            
            console.log(`Status line message: ${message} (${type})`);
        } catch (error) {
            console.error('Error showing status message:', error);
        }
    }
    
    /**
     * Show info message
     */
    showInfo(message) {
        this.showMessage(message, 'info');
    }
    
    /**
     * Show success message
     */
    showSuccess(message) {
        this.showMessage(message, 'success');
    }
    
    /**
     * Show error message
     */
    showError(message) {
        this.showMessage(message, 'error');
    }
    
    /**
     * Show warning message
     */
    showWarning(message) {
        this.showMessage(message, 'warning');
    }
    
    /**
     * Update the filtered count
     */
    updateFilteredCount(count) {
        if (!this.initialized || !this.filteredCountElement) return;
        
        try {
            this.filteredCountElement.textContent = count;
        } catch (error) {
            console.error('Error updating filtered count:', error);
        }
    }
    
    /**
     * Clear the status line
     */
    clear() {
        if (!this.initialized || !this.lastMessageElement) return;
        
        try {
            this.lastMessageElement.textContent = 'Ready';
            this.lastMessageElement.classList.remove('info', 'success', 'error', 'warning');
            this.lastMessageElement.classList.add('info');
            
            if (this.statusLine) {
                this.statusLine.className = 'status-line';
            }
        } catch (error) {
            console.error('Error clearing status line:', error);
        }
    }
    
    /**
     * Get current status
     */
    getStatus() {
        if (!this.initialized) return null;
        
        return {
            message: this.lastMessageElement ? this.lastMessageElement.textContent : '',
            type: this.lastMessageElement ? this.getCurrentType() : '',
            filteredCount: this.filteredCountElement ? this.filteredCountElement.textContent : '0'
        };
    }
    
    /**
     * Get current message type
     */
    getCurrentType() {
        if (!this.lastMessageElement) return '';
        
        if (this.lastMessageElement.classList.contains('info')) return 'info';
        if (this.lastMessageElement.classList.contains('success')) return 'success';
        if (this.lastMessageElement.classList.contains('error')) return 'error';
        if (this.lastMessageElement.classList.contains('warning')) return 'warning';
        
        return '';
    }
    
    /**
     * Destroy the status line
     */
    destroy() {
        try {
            this.statusLine = null;
            this.lastMessageElement = null;
            this.filteredCountElement = null;
            this.initialized = false;
            console.log('Status line destroyed');
        } catch (error) {
            console.error('Error destroying status line:', error);
        }
    }
}

// Create global status line instance
window.statusLine = new StatusLine();
