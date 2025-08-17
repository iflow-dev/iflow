/**
 * iflow - Project Artifact Manager (Web Version)
 * Main JavaScript application file for web browser usage
 */

// Global state
let currentArtifacts = [];
let editingArtifactId = null;
let projectConfig = null;
let workItemTypes = [];
let artifactStatuses = [];

// API base URL
const API_BASE = '/api';

// Initialize the application
document.addEventListener('DOMContentLoaded', async function() {
    console.log('DOM loaded, starting to load data...');
    await loadConfiguration();
    loadStats();
    loadArtifacts();
    
    // Add event listeners for filter changes
    setupFilterEventListeners();
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
            console.log('workItemTypes array length:', workItemTypes.length);
            updateTypeFilterOptions();
        } else {
            console.error('Failed to load work item types:', typesResponse.status);
        }
        
        // Load artifact statuses
        const statusesResponse = await fetch(`${API_BASE}/artifact-statuses`);
        if (statusesResponse.ok) {
            artifactStatuses = await statusesResponse.json();
            console.log('Artifact statuses loaded:', artifactStatuses);
            updateStatusFormOptions();
        } else {
            console.error('Failed to load artifact statuses:', statusesResponse.status);
        }
    } catch (error) {
        console.error('Error loading configuration:', error);
    }
}

function updateTypeFilterOptions() {
    // Update the type filter dropdown (first filter-select)
    const typeFilters = document.querySelectorAll('.filter-select');
    if (typeFilters.length >= 1 && workItemTypes.length > 0) {
        const typeFilter = typeFilters[0];
        // Clear existing options
        typeFilter.innerHTML = '<option value="">All Types</option>';
        
        // Add options for each work item type
        workItemTypes.forEach(type => {
            const option = document.createElement('option');
            option.value = type.id;
            // For Ionic icons, show the icon name; for emojis, show the emoji
            const displayIcon = type.icon.startsWith('ion-') ? type.icon.replace('ion-', '') : type.icon;
            option.textContent = `${displayIcon} ${type.name}`;
            option.style.color = type.color;
            typeFilter.appendChild(option);
        });
    }
    
    // Update the status filter dropdown (second filter-select)
    if (typeFilters.length >= 2 && artifactStatuses.length > 0) {
        const statusFilter = typeFilters[1];
        // Clear existing options
        statusFilter.innerHTML = '<option value="">All Statuses</option>';
        
        // Add options for each status
        artifactStatuses.forEach(status => {
            const option = document.createElement('option');
            option.value = status.id;
            option.textContent = `${status.icon} ${status.name}`;
            option.style.color = status.color;
            statusFilter.appendChild(option);
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
            // For Ionic icons, show the icon name; for emojis, show the emoji
            const displayIcon = type.icon.startsWith('ion-') ? type.icon.replace('ion-', '') : type.icon;
            option.textContent = `${displayIcon} ${type.name}`;
            option.style.color = type.color;
            artifactTypeSelect.appendChild(option);
        });
    }
}

function updateStatusFormOptions() {
    // Update the status form dropdown
    const artifactStatusSelect = document.getElementById('artifactStatus');
    if (artifactStatusSelect && artifactStatuses.length > 0) {
        // Clear existing options
        artifactStatusSelect.innerHTML = '';
        
        // Add options for each status
        artifactStatuses.forEach(status => {
            const option = document.createElement('option');
            option.value = status.id;
            option.textContent = `${status.icon} ${status.name}`;
            option.style.color = status.color;
            artifactStatusSelect.appendChild(option);
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
    console.log('getTypeDisplayInfo called with:', typeId);
    console.log('Available workItemTypes:', workItemTypes);
    
    if (workItemTypes && workItemTypes.length > 0) {
        const typeInfo = workItemTypes.find(type => type.id === typeId);
        console.log('Found typeInfo:', typeInfo);
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
    console.log('Using fallback for type:', typeId);
    return {
        id: typeId,
        name: typeId.charAt(0).toUpperCase() + typeId.slice(1),
        color: "#6B7280",
        icon: "📄"
    };
}

// Helper function to render icon (supports both emoji and Ionic icons)
function renderIcon(iconValue) {
    if (iconValue.startsWith('ion-')) {
        // Ionic icon - return the icon element HTML
        const iconName = iconValue.replace('ion-', '');
        return `<ion-icon name="${iconName}"></ion-icon>`;
    } else {
        // Emoji or other icon - return as is
        return iconValue;
    }
}

// Helper function to get status display information
function getStatusDisplayInfo(statusId) {
    if (artifactStatuses && artifactStatuses.length > 0) {
        const statusInfo = artifactStatuses.find(status => status.id === statusId);
        if (statusInfo) {
            return {
                "name": statusInfo.name,
                "icon": statusInfo.icon,
                "color": statusInfo.color
            };
        }
    }
    return {
        "name": statusId,
        "icon": "⚪",
        "color": "#6B7280"
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
        document.getElementById('artifactCategory').value = artifact.category || '';
        document.getElementById('artifactStatus').value = artifact.status || 'open';
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
        const statusInfo = getStatusDisplayInfo(artifact.status);
        return `
        <div class="artifact-card">
            <div class="artifact-header">
                <span class="artifact-type" style="border-color: ${typeInfo.color}; color: ${typeInfo.color}">
                    ${renderIcon(typeInfo.icon)} ${typeInfo.name}
                </span>
                <span class="artifact-status" style="color: ${statusInfo.color}">
                    ${renderIcon(statusInfo.icon)} ${statusInfo.name}
                </span>
                <span class="artifact-id">${artifact.artifact_id}</span>
            </div>
            <div class="artifact-content">
                <div class="artifact-summary">${artifact.summary}</div>
                <div class="artifact-description">${artifact.description || 'No description'}</div>
                ${artifact.category ? `<div class="artifact-category"><a href="#" onclick="filterByCategory('${artifact.category}', true); return false;" class="category-link">${artifact.category}</a></div>` : ''}
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
        // If no search query, apply other active filters
        applyAllFilters();
        return;
    }
    
    // Apply search filter locally and then apply all other active filters
    applyAllFilters();
}

async function filterByType(type) {
    if (type === '') {
        // If no type filter, apply other active filters
        applyAllFilters();
        return;
    }
    
    // Apply type filter locally and then apply all other active filters
    applyAllFilters();
}

async function filterByCategory(category, exactMatch = false) {
    if (category.trim() === '') {
        // If no category filter, apply other active filters
        applyAllFilters();
        return;
    }
    
    // Update the category filter input box to show the selected category
    if (exactMatch) {
        const categoryFilter = document.querySelector('input[placeholder="Filter by category..."]');
        if (categoryFilter) {
            categoryFilter.value = category;
        }
    }
    
    // Apply category filter locally and then apply all other active filters
    applyAllFilters();
}

async function filterByStatus(status) {
    if (status === '') {
        // If no status filter, apply other active filters
        applyAllFilters();
        return;
    }
    
    // Apply status filter locally and then apply all other active filters
    applyAllFilters();
}

// Form Handling
document.getElementById('artifactForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        type: document.getElementById('artifactType').value,
        summary: document.getElementById('artifactSummary').value,
        description: document.getElementById('artifactDescription').value,
        category: document.getElementById('artifactCategory').value,
        status: document.getElementById('artifactStatus').value
    };
    
            try {
            // Capture current filter state before editing
            const currentFilterState = getCurrentFilterState();
            
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
            
            // Load artifacts and then reapply the filter state
            await loadArtifacts();
            applyFilterState(currentFilterState);
        } catch (error) {
        console.error('Error saving artifact:', error);
        alert('Error saving artifact: ' + error.message);
    }
});

// Artifact Operations
async function deleteArtifact(artifactId) {
    if (confirm('Are you sure you want to delete this artifact?')) {
        try {
            // Capture current filter state before deleting
            const currentFilterState = getCurrentFilterState();
            
            const response = await fetch(`${API_BASE}/artifacts/${artifactId}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            loadStats();
            
            // Load artifacts and then reapply the filter state
            await loadArtifacts();
            applyFilterState(currentFilterState);
        } catch (error) {
            console.error('Error deleting artifact:', error);
            alert('Error deleting artifact: ' + error.message);
        }
    }
}

function refreshArtifacts() {
    // Reset all filters
    const typeFilters = document.querySelectorAll('.filter-select');
    if (typeFilters.length >= 1) typeFilters[0].value = '';
    if (typeFilters.length >= 2) typeFilters[1].value = '';
    
    // Reset category filter
    const categoryFilter = document.querySelector('input[placeholder="Filter by category..."]');
    if (categoryFilter) categoryFilter.value = '';
    
    // Reset search
    const searchBox = document.querySelector('input[placeholder="Search artifacts..."]');
    if (searchBox) searchBox.value = '';
    
    loadStats();
    loadArtifacts();
}

// Filter State Management
function getCurrentFilterState() {
    const typeFilters = document.querySelectorAll('.filter-select');
    const categoryFilter = document.querySelector('input[placeholder="Filter by category..."]');
    const searchBox = document.querySelector('input[placeholder="Search artifacts..."]');
    
    return {
        type: typeFilters.length >= 1 ? typeFilters[0].value : '',
        status: typeFilters.length >= 2 ? typeFilters[1].value : '',
        category: categoryFilter ? categoryFilter.value : '',
        search: searchBox ? searchBox.value : ''
    };
}

function applyFilterState(filterState) {
    if (filterState.type || filterState.status || filterState.category || filterState.search) {
        applyAllFilters();
    } else {
        // No filters active, show all artifacts
        displayArtifacts(currentArtifacts);
    }
}

// New function to apply all active filters in combination
function applyAllFilters() {
    const filterState = getCurrentFilterState();
    let filtered = [...currentArtifacts]; // Start with all artifacts
    
    // Apply type filter
    if (filterState.type) {
        filtered = filtered.filter(artifact => artifact.type === filterState.type);
    }
    
    // Apply status filter
    if (filterState.status) {
        filtered = filtered.filter(artifact => artifact.status === filterState.status);
    }
    
    // Apply category filter
    if (filterState.category) {
        filtered = filtered.filter(artifact => 
            artifact.category && artifact.category.toLowerCase().includes(filterState.category.toLowerCase())
        );
    }
    
    // Apply search filter
    if (filterState.search) {
        filtered = filtered.filter(artifact => 
            artifact.summary.toLowerCase().includes(filterState.search.toLowerCase()) ||
            artifact.description.toLowerCase().includes(filterState.search.toLowerCase()) ||
            (artifact.category && artifact.category.toLowerCase().includes(filterState.search.toLowerCase()))
        );
    }
    
    console.log(`Applied filters - Type: ${filterState.type}, Status: ${filterState.status}, Category: ${filterState.category}, Search: ${filterState.search}`);
    console.log(`Filtered from ${currentArtifacts.length} to ${filtered.length} artifacts`);
    
    displayArtifacts(filtered);
}

// Event Listeners
window.onclick = function(event) {
    const modal = document.getElementById('artifactModal');
    if (event.target === modal) {
        closeModal();
    }
}

// Setup event listeners for filter changes
function setupFilterEventListeners() {
    // Add event listeners for filter dropdowns
    const typeFilters = document.querySelectorAll('.filter-select');
    if (typeFilters.length >= 1) {
        typeFilters[0].addEventListener('change', function() {
            applyAllFilters();
        });
    }
    if (typeFilters.length >= 2) {
        typeFilters[1].addEventListener('change', function() {
            applyAllFilters();
        });
    }
    
    // Add event listener for category filter input
    const categoryFilter = document.querySelector('input[placeholder="Filter by category..."]');
    if (categoryFilter) {
        categoryFilter.addEventListener('input', function() {
            applyAllFilters();
        });
    }
    
    // Add event listener for search input
    const searchBox = document.querySelector('input[placeholder="Search artifacts..."]');
    if (searchBox) {
        searchBox.addEventListener('input', function() {
            applyAllFilters();
        });
    }
}
