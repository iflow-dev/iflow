/**
 * iflow - Project Artifact Manager (Web Version)
 * Main JavaScript application file for web browser usage
 */

// Global state
let currentArtifacts = [];
let editingArtifactId = null;

// API base URL
const API_BASE = '/api';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, starting to load data...');
    loadStats();
    loadArtifacts();
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
