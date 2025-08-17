// Tile Management System
// This file contains all tile/artifact display functionality for the iflow application

class TileManager {
    constructor() {
        this.workItemTypes = [];
        this.artifactStatuses = [];
        this.currentArtifacts = [];
        this.isInitialized = false;
    }

    // Initialize tile manager with data
    initializeData(workItemTypes, artifactStatuses) {
        if (!Array.isArray(workItemTypes) || !Array.isArray(artifactStatuses)) {
            console.error('Invalid data provided to initializeData');
            return false;
        }
        
        this.workItemTypes = [...workItemTypes];
        this.artifactStatuses = [...artifactStatuses];
        this.isInitialized = true;
        
        console.log(`TileManager initialized with ${this.workItemTypes.length} work item types and ${this.artifactStatuses.length} artifact statuses`);
        return true;
    }

    // Update current artifacts
    updateArtifacts(artifacts) {
        this.currentArtifacts = artifacts;
    }

    // Display artifacts as tiles
    displayArtifacts(artifacts, containerId = 'artifacts-container') {
        if (!this.isInitialized) {
            console.error('TileManager not initialized. Call initializeData() first.');
            return false;
        }

        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container with id '${containerId}' not found`);
            return false;
        }

        if (artifacts.length === 0) {
            container.innerHTML = '<div class="loading">No artifacts found. Create your first artifact to get started!</div>';
            return true;
        }

        container.innerHTML = artifacts.map(artifact => this.createArtifactTile(artifact)).join('');
        return true;
    }

    // Create a single artifact tile
    createArtifactTile(artifact) {
        const typeInfo = this.getTypeDisplayInfo(artifact.type);
        const statusInfo = this.getStatusDisplayInfo(artifact.status);
        
        return `
        <div class="artifact-card">
            <div class="artifact-header">
                <span class="artifact-type" style="border-color: ${typeInfo.color}; color: ${typeInfo.color}">
                    ${this.renderIcon(typeInfo.icon)} ${typeInfo.name}
                </span>
                <span class="artifact-status" style="color: ${statusInfo.color}">
                    ${this.renderIcon(statusInfo.icon)} ${statusInfo.name}
                </span>
                <span class="artifact-id">${artifact.artifact_id}</span>
            </div>
            <div class="artifact-content">
                <div class="artifact-summary">${artifact.summary}</div>
                <div class="artifact-description">${artifact.description || 'No description'}</div>
                <div class="artifact-meta">
                    <span>Created: ${new Date(artifact.created_at).toLocaleDateString()}</span>
                    <span>Updated: ${new Date(artifact.updated_at).toLocaleDateString()}</span>
                </div>
            </div>
            <div class="artifact-actions">
                <button class="btn btn-danger" onclick="deleteArtifact('${artifact.artifact_id}')" title="Delete artifact">
                    <ion-icon name="trash-outline"></ion-icon>
                </button>
                <button class="btn btn-primary" onclick="openEditModal('${artifact.artifact_id}')" title="Edit artifact">
                    <ion-icon name="create-outline"></ion-icon>
                </button>
            </div>
            ${artifact.category ? `<div class="artifact-category-bottom"><a href="#" onclick="filterByCategory('${artifact.category}', true); return false;" class="category-link">${artifact.category}</a></div>` : ''}
        </div>
        `;
    }

    // Get type display information
    getTypeDisplayInfo(typeId) {
        if (this.workItemTypes && this.workItemTypes.length > 0) {
            const typeInfo = this.workItemTypes.find(type => type.id === typeId);
            if (typeInfo) {
                return {
                    id: typeInfo.id,
                    name: typeInfo.name,
                    color: typeInfo.color,
                    icon: typeInfo.icon
                };
            }
        }
        
        // Fallback for unknown types
        return {
            id: typeId,
            name: typeId.charAt(0).toUpperCase() + typeId.slice(1),
            color: "#6B7280",
            icon: "📄"
        };
    }

    // Get status display information
    getStatusDisplayInfo(statusId) {
        // Handle empty or undefined statusId
        if (!statusId || statusId === '') {
            if (this.artifactStatuses && this.artifactStatuses.length > 0) {
                const defaultStatus = this.artifactStatuses.find(status => status.id === 'open');
                if (defaultStatus) {
                    return {
                        "name": defaultStatus.name,
                        "icon": defaultStatus.icon,
                        "color": defaultStatus.color
                    };
                }
            }
            return {
                "name": "Open",
                "icon": "🔓",
                "color": "#10B981"
            };
        }
        
        if (this.artifactStatuses && this.artifactStatuses.length > 0) {
            const statusInfo = this.artifactStatuses.find(status => status.id === statusId);
            if (statusInfo) {
                return {
                    "name": statusInfo.name,
                    "icon": statusInfo.icon,
                    "color": statusInfo.color
                };
            }
        }
        
        return {
            "name": statusId || "Unknown",
            "icon": "⚪",
            "color": "#6B7280"
        };
    }

    // Render icon (supports both emoji and Ionic icons)
    renderIcon(iconValue) {
        if (iconValue.startsWith('ion-')) {
            // Ionic icon - return the icon element HTML
            const iconName = iconValue.replace('ion-', '');
            return `<ion-icon name="${iconName}"></ion-icon>`;
        } else {
            // Emoji or other icon - return as is
            return iconValue;
        }
    }

    // Get tile count
    getTileCount() {
        return this.currentArtifacts.length;
    }

    // Get tiles by type
    getTilesByType(typeId) {
        return this.currentArtifacts.filter(artifact => artifact.type === typeId);
    }

    // Get tiles by status
    getTilesByStatus(statusId) {
        return this.currentArtifacts.filter(artifact => artifact.status === statusId);
    }

    // Get tiles by category
    getTilesByCategory(category) {
        return this.currentArtifacts.filter(artifact => artifact.category === category);
    }

    // Search tiles
    searchTiles(query) {
        const searchTerm = query.toLowerCase().trim();
        return this.currentArtifacts.filter(artifact => 
            artifact.summary.toLowerCase().includes(searchTerm) ||
            (artifact.description && artifact.description.toLowerCase().includes(searchTerm)) ||
            (artifact.category && artifact.category.toLowerCase().includes(searchTerm))
        );
    }

    // Refresh tiles
    refreshTiles(containerId = 'artifacts-container') {
        return this.displayArtifacts(this.currentArtifacts, containerId);
    }

    // Cleanup
    cleanup() {
        this.workItemTypes = [];
        this.artifactStatuses = [];
        this.currentArtifacts = [];
        this.isInitialized = false;
        console.log('TileManager cleanup completed');
    }
}

// Export the class
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TileManager;
}
