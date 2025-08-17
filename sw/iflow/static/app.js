/**
 * iflow - Project Artifact Manager
 * Main JavaScript application file
 */

// Global state
let currentArtifacts = [];
let editingArtifactId = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, waiting for pywebview...');
    // Wait a bit for pywebview to be ready
    setTimeout(() => {
        console.log('Starting to load data...');
        loadStats();
        loadArtifacts();
    }, 1000);
});

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
        console.log('pywebview.api.get_stats:', pywebview.api.get_stats);
        
        const stats = await pywebview.api.get_stats();
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
    `;
}

// Artifact Management
async function loadArtifacts() {
    try {
        console.log('loadArtifacts called');
        console.log('pywebview.api:', pywebview.api);
        console.log('pywebview.api.list_artifacts:', pywebview.api.list_artifacts);
        
        const artifacts = await pywebview.api.list_artifacts();
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
    
    container.innerHTML = artifacts.map(artifact => `
        <div class="artifact-card">
            <div class="artifact-header">
                <span class="artifact-type">${artifact.type}</span>
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
    `).join('');
}

// Search and Filter
async function searchArtifacts(query) {
    if (query.trim() === '') {
        displayArtifacts(currentArtifacts);
        return;
    }
    
    try {
        const results = await pywebview.api.search_artifacts(query);
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
        const filtered = await pywebview.api.list_artifacts(type);
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
        if (editingArtifactId) {
            await pywebview.api.update_artifact(editingArtifactId, formData);
        } else {
            await pywebview.api.create_artifact(formData);
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
            await pywebview.api.delete_artifact(artifactId);
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
