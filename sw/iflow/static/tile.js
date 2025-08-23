/**
 * Tile Manager - Handles artifact display and tile management
 * Uses singleton pattern for global access
 */
class TileManager {
    constructor() {
        if (TileManager.instance) {
            return TileManager.instance;
        }
        
        this.currentArtifacts = [];
        this.workItemTypes = [];
        this.artifactStatuses = [];
        this.container = null;
        
        // Store the singleton instance
        TileManager.instance = this;
        
        // Make it globally accessible
        window.tileManager = this;
        
        console.log('TileManager singleton created');
    }

    /**
     * Get the singleton instance
     */
    static getInstance() {
        if (!TileManager.instance) {
            new TileManager();
        }
        return TileManager.instance;
    }

    /**
     * Initialize the tile manager with data
     */
    initializeData(workItemTypes, artifactStatuses) {
        this.workItemTypes = workItemTypes || [];
        this.artifactStatuses = artifactStatuses || [];
        this.container = document.getElementById('artifacts-container');
        
        if (!this.container) {
            console.error('Artifacts container not found');
            return false;
        }
        
        console.log(`TileManager initialized with ${this.workItemTypes.length} types and ${this.artifactStatuses.length} statuses`);
        return true;
    }

    /**
     * Get the current artifacts count
     */
    getArtifactCount() {
        return this.currentArtifacts ? this.currentArtifacts.length : 0;
    }

    /**
     * Get all current artifacts
     */
    getAllArtifacts() {
        return this.currentArtifacts || [];
    }

    /**
     * Update artifacts data
     */
    updateArtifacts(artifacts) {
        this.currentArtifacts = artifacts || [];
        console.log(`TileManager artifacts updated: ${this.currentArtifacts.length} artifacts`);
    }

    /**
     * Display artifacts in the container
     */
    displayArtifacts(artifacts, containerId = null) {
        const targetContainer = containerId ? document.getElementById(containerId) : this.container;
        if (!targetContainer) {
            console.error('Container not found for artifact display');
            return;
        }

        const artifactsToDisplay = artifacts || this.currentArtifacts || [];
        console.log(`Displaying ${artifactsToDisplay.length} artifacts`);

        // Clear existing content
        targetContainer.innerHTML = '';

        if (artifactsToDisplay.length === 0) {
            targetContainer.innerHTML = '<div class="no-results">No artifacts found</div>';
            return;
        }

        // Create and display tiles
        artifactsToDisplay.forEach(artifact => {
            const tile = this.createArtifactTile(artifact);
            targetContainer.appendChild(tile);
        });
    }

    /**
     * Create an individual artifact tile
     */
    createArtifactTile(artifact) {
        const tile = document.createElement('div');
        tile.className = 'artifact-tile';
        tile.setAttribute('data-artifact-id', artifact.artifact_id);

        // Get type and status info
        const typeInfo = this.workItemTypes.find(t => t.id === artifact.type) || {};
        const statusInfo = this.artifactStatuses.find(s => s.id === artifact.status) || {};

        tile.innerHTML = `
            <div class="artifact-header">
                <div class="artifact-type">
                    <ion-icon name="${typeInfo.icon || 'document-outline'}"></ion-icon>
                    <span>${typeInfo.name || artifact.type || 'Unknown'}</span>
                </div>
                <div class="artifact-id">${artifact.artifact_id}</div>
                <div class="artifact-status">
                    <ion-icon name="${statusInfo.icon || 'help-circle-outline'}"></ion-icon>
                    <span>${statusInfo.name || artifact.status || 'None'}</span>
                </div>
            </div>
            <div class="artifact-summary">${artifact.summary || 'No summary'}</div>
            <div class="artifact-details">
                <div class="artifact-category">${artifact.category || 'No category'}</div>
                <div class="artifact-iteration">${artifact.iteration || 'No iteration'}</div>
            </div>
                <div class="artifact-actions">
                                <button class="btn btn-icon" onclick="openEditModal('${artifact.artifact_id}')" title="Edit">
                    <ion-icon name="create-outline"></ion-icon>
                </button>
                <button class="btn btn-icon" onclick="toggleArtifactFlag('${artifact.artifact_id}')" title="Toggle Flag">
                    <ion-icon name="${artifact.flagged ? 'flag' : 'flag-outline'}"></ion-icon>
                </button>
        </div>
        `;

        return tile;
    }

    /**
     * Refresh tiles display
     */
    refreshTiles() {
        this.displayArtifacts(this.currentArtifacts);
    }

    /**
     * Filter artifacts by type
     */
    filterByType(typeId) {
        if (!typeId) return this.currentArtifacts;
        return this.currentArtifacts.filter(artifact => artifact.type === typeId);
    }

    /**
     * Filter artifacts by status
     */
    filterByStatus(statusId) {
        if (!statusId) return this.currentArtifacts;
        return this.currentArtifacts.filter(artifact => artifact.status === statusId);
    }

    /**
     * Filter artifacts by category
     */
    filterByCategory(category) {
        if (!category) return this.currentArtifacts;
        return this.currentArtifacts.filter(artifact => 
            artifact.category && artifact.category.toLowerCase().includes(category.toLowerCase())
        );
    }

    /**
     * Search artifacts by text
     */
    searchArtifacts(query) {
        if (!query) return this.currentArtifacts;
        const lowerQuery = query.toLowerCase();
        return this.currentArtifacts.filter(artifact => 
            (artifact.summary && artifact.summary.toLowerCase().includes(lowerQuery)) ||
            (artifact.description && artifact.description.toLowerCase().includes(lowerQuery)) ||
            (artifact.category && artifact.category.toLowerCase().includes(lowerQuery))
        );
    }

    /**
     * Clear all artifacts
     */
    clearArtifacts() {
        this.currentArtifacts = [];
        if (this.container) {
            this.container.innerHTML = '<div class="loading">No artifacts loaded</div>';
        }
    }

    /**
     * Cleanup resources
     */
    cleanup() {
        this.currentArtifacts = [];
        this.workItemTypes = [];
        this.artifactStatuses = [];
        this.container = null;
        TileManager.instance = null;
        window.tileManager = null;
    }
}

// Create the singleton instance immediately
const tileManager = new TileManager();

// Export for module systems if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TileManager;
}
