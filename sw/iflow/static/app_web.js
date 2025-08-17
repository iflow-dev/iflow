/**
 * iflow - Project Artifact Manager (Web Version)
 * Main JavaScript application file for web browser usage
 */

// Global state
let currentArtifacts = [];
let editingArtifactId = null;
let projectConfig = null;
let workItemTypes = [];

// API base URL
const API_BASE = '/api';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, starting to load data...');
    loadConfiguration();
    loadStats();
    loadArtifacts();
});

// Configuration Management
async function loadConfiguration() {
    try {
        console.log('Loading project configuration...');
        
        // Load project info
        const projectResponse = await fetch(`${API_BASE}/project-info`);
        if (projectResponse.ok) {
            projectConfig = await projectResponse.json();
            console.log('Project config loaded:', projectConfig);
            updateProjectHeader();
        }
        
        // Load work item types
        const typesResponse = await fetch(`${API_BASE}/work-item-types`);
        if (typesResponse.ok) {
            workItemTypes = await typesResponse.json();
            console.log('Work item types loaded:', workItemTypes);
            updateTypeFilterOptions();
        }
    } catch (error) {
        console.error('Error loading configuration:', error);
    }
}

function updateTypeFilterOptions() {
    // Update the filter dropdown
    const typeFilter = document.querySelector('.filter-select');
    if (typeFilter && workItemTypes.length > 0) {
        // Clear existing options
        typeFilter.innerHTML = '<option value="">All Types</option>';
        
        // Add options for each work item type
        workItemTypes.forEach(type => {
            const option = document.createElement('option');
            option.value = type.id;
            option.textContent = `${type.icon} ${type.name}`;
            option.style.color = type.color;
            typeFilter.appendChild(option);
        });
    }
    
    // Update the form dropdown
    const artifactTypeSelect = document.getElementById('artifactType');
    if (artifactTypeSelect && workItemTypes.length > 0) {
        // Clear existing options
        artifactTypeSelect.innerHTML = '';
        
        // Add options for each work item type
        workItemTypes.forEach(type => {
            const option = document.createElement('option');
            option.value = type.id;
            option.textContent = `${type.icon} ${type.name}`;
            option.style.color = type.color;
            artifactTypeSelect.appendChild(option);
        });
    }
}

function updateProjectHeader() {
    if (projectConfig) {
        const header = document.querySelector('.header h1');
        if (header) {
            header.textContent = `${projectConfig.name} - ${projectConfig.description}`;
        }
    }
}

// Helper function to get type display information
function getTypeDisplayInfo(typeId) {
    if (workItemTypes && workItemTypes.length > 0) {
        const typeInfo = workItemTypes.find(type => type.id === typeId);
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

// Modal Management
function openCreateModal() {
    editingArtifactId = null;
    document.getElementById('modalTitle').textContent = 'Create New Artifact';
    document.getElementById('artifactForm').reset();
    document.getElementById('artifactModal').style.display = 'block';
}

function openEditModal(artifactId) {
    editingArtifactId = artifactId;
    const artifact = currentArtifacts.find(a => a.artifact_id === artifactId);
    if (artifact) {
        document.getElementById('modalTitle').textContent = 'Edit Artifact';
        document.getElementById('artifactType').value = artifact.type;
        document.getElementById('artifactSummary').value = artifact.summary;
        document.getElementById('artifactDescription').value = artifact.description || '';
        document.getElementById('artifactModal').style.display = 'block';
    }
}

function closeModal() {
    document.getElementById('artifactModal').style.display = 'none';
}

// Statistics Management
async function loadStats() {
    try {
        console.log('loadStats called');
        
        const response = await fetch(`${API_BASE}/stats`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const stats = await response.json();
        console.log('Stats received:', stats);
        displayStats(stats);
    } catch (error) {
        console.error('Error loading stats:', error);
        console.error('Error details:', error.message, error.stack);
        document.getElementById('stats-bar').innerHTML = '<div class="error">Error loading statistics: ' + error.message + '</div>';
    }
}

function displayStats(stats) {
    const statsBar = document.getElementById('stats-bar');
    
    let projectVersion = '';
    if (projectConfig && projectConfig.version) {
        projectVersion = `<div class="stat-item">
            <div class="stat-number">v${projectConfig.version}</div>
            <div class="stat-label">Version</div>
        </div>`;
    }
    
    statsBar.innerHTML = `
        <div class="stat-item">
            <div class="stat-number">${stats.total_artifacts}</div>
            <div class="stat-label">Total Artifacts</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">${stats.total_commits}</div>
            <div class="stat-label">Total Commits</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">${Object.keys(stats.by_type).length}</div>
            <div class="stat-label">Artifact Types</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">${stats.last_commit ? '✓' : '✗'}</div>
            <div class="stat-label">Git Status</div>
        </div>
        ${projectVersion}
    `;
}

// Artifact Management
async function loadArtifacts() {
    try {
        console.log('loadArtifacts called');
        
        const response = await fetch(`${API_BASE}/artifacts`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const artifacts = await response.json();
        console.log('Artifacts received:', artifacts);
        currentArtifacts = artifacts;
        displayArtifacts(artifacts);
    } catch (error) {
        console.error('Error loading artifacts:', error);
        console.error('Error details:', error.message, error.stack);
        document.getElementById('artifacts-container').innerHTML = '<div class="error">Error loading artifacts: ' + error.message + '</div>';
    }
}

function displayArtifacts(artifacts) {
    const container = document.getElementById('artifacts-container');
    
    if (artifacts.length === 0) {
        container.innerHTML = '<div class="loading">No artifacts found. Create your first artifact to get started!</div>';
        return;
    }
    
    container.innerHTML = artifacts.map(artifact => {
        const typeInfo = getTypeDisplayInfo(artifact.type);
        return `
        <div class="artifact-card">
            <div class="artifact-header">
                <span class="artifact-type" style="border-color: ${typeInfo.color}; color: ${typeInfo.color}">
                    ${typeInfo.icon} ${typeInfo.name}
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
                <button class="btn btn-secondary" onclick="openEditModal('${artifact.artifact_id}')">Edit</button>
                <button class="btn btn-danger" onclick="deleteArtifact('${artifact.artifact_id}')">Delete</button>
            </div>
        </div>
    `}).join('');
}

// Search and Filter
async function searchArtifacts(query) {
    if (query.trim() === '') {
        displayArtifacts(currentArtifacts);
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/search?q=${encodeURIComponent(query)}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const results = await response.json();
        displayArtifacts(results);
    } catch (error) {
        console.error('Error searching artifacts:', error);
    }
}

async function filterByType(type) {
    if (type === '') {
        displayArtifacts(currentArtifacts);
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/artifacts?type=${encodeURIComponent(type)}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const filtered = await response.json();
        displayArtifacts(filtered);
    } catch (error) {
        console.error('Error filtering artifacts:', error);
    }
}

// Form Handling
document.getElementById('artifactForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        type: document.getElementById('artifactType').value,
        summary: document.getElementById('artifactSummary').value,
        description: document.getElementById('artifactDescription').value
    };
    
    try {
        let response;
        if (editingArtifactId) {
            // Update existing artifact
            response = await fetch(`${API_BASE}/artifacts/${editingArtifactId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
        } else {
            // Create new artifact
            response = await fetch(`${API_BASE}/artifacts`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
        }
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        closeModal();
        loadStats();
        loadArtifacts();
    } catch (error) {
        console.error('Error saving artifact:', error);
        alert('Error saving artifact: ' + error.message);
    }
});

// Artifact Operations
async function deleteArtifact(artifactId) {
    if (confirm('Are you sure you want to delete this artifact?')) {
        try {
            const response = await fetch(`${API_BASE}/artifacts/${artifactId}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            loadStats();
            loadArtifacts();
        } catch (error) {
            console.error('Error deleting artifact:', error);
            alert('Error deleting artifact: ' + error.message);
        }
    }
}

function refreshArtifacts() {
    loadStats();
    loadArtifacts();
}

// Event Listeners
window.onclick = function(event) {
    const modal = document.getElementById('artifactModal');
    if (event.target === modal) {
        closeModal();
    }
}
