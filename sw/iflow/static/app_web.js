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
let currentFilterState = {
    type: '',
    status: '',
    category: '',
    search: '',
    flagged: false
};

// Initialize the managers
let dropdownManager = null;
let tileManager = null;
let statisticsManager = null;
let searchManager = null;

// API base URL
const API_BASE = '/api';

// Initialize the application
document.addEventListener('DOMContentLoaded', async function() {
    console.log('DOM loaded, starting to load data...');
    await loadConfiguration();
    if (statisticsManager) {
        statisticsManager.loadStats();
    }
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
            updateStatusFilterOptions();
            updateStatusFormOptions();
            
            // Initialize managers with the loaded data
            dropdownManager = new CustomDropdownManager();
            tileManager = new TileManager();
            statisticsManager = new StatisticsManager();
            searchManager = new SearchManager();
            
            if (dropdownManager.initializeData(workItemTypes, artifactStatuses)) {
                dropdownManager.createCustomDropdowns();
                // Expose dropdown accessibility functions for testing (Ticket #00073)
                dropdownManager.exposeForTesting();
            }
            
            if (tileManager.initializeData(workItemTypes, artifactStatuses)) {
                console.log('Tile manager initialized successfully');
            }
            
            if (statisticsManager) {
                statisticsManager.initialize(projectConfig);
            }
            
            if (searchManager) {
                searchManager.initialize();
            }
        } else {
            console.error('Failed to load artifact statuses:', statusesResponse.status);
        }
    } catch (error) {
        console.error('Error loading configuration:', error);
    }
}

function updateStatusFilterOptions() {
    // Update the status filter dropdown using specific ID
    const statusFilter = document.getElementById('statusFilter');
    if (statusFilter && artifactStatuses.length > 0) {
        // Clear existing options
        statusFilter.innerHTML = '<option value="">All Statuses</option>';
        
        // Add options for each status
        artifactStatuses.forEach(status => {
            const option = document.createElement('option');
            option.value = status.id;
            // For emojis, show the emoji
            const displayText = status.icon.startsWith('ion-') ? status.icon : status.icon;
            option.textContent = `${displayText} ${status.name}`;
            option.style.color = status.color;
            option.setAttribute('data-icon', status.icon);
            statusFilter.appendChild(option);
        });
    }
}

function updateTypeFilterOptions() {
    // Update the type filter dropdown using specific ID
    const typeFilter = document.getElementById('typeFilter');
    if (typeFilter && workItemTypes.length > 0) {
        // Clear existing options
        typeFilter.innerHTML = '<option value="">All Types</option>';
        
        // Add options for each work item type
        workItemTypes.forEach(type => {
            const option = document.createElement('option');
            option.value = type.id;
            // For Ionic icons, we'll show the icon name; for emojis, show the emoji
            // Note: HTML options cannot display ion-icon elements directly
            const displayText = type.icon.startsWith('ion-') ? type.icon : type.icon;
            option.textContent = `${displayText} ${type.name}`;
            option.style.color = type.color;
            option.setAttribute('data-icon', type.icon);
            typeFilter.appendChild(option);
        });
    }
    
    // Note: Status filter dropdown is updated by updateStatusFormOptions()
    
    // Update the form dropdown
    const artifactTypeSelect = document.getElementById('artifactType');
    if (artifactTypeSelect && workItemTypes.length > 0) {
        // Clear existing options
        artifactTypeSelect.innerHTML = '<option value="">Select Type</option>';
        
        // Add options for each work item type
        workItemTypes.forEach(type => {
            const option = document.createElement('option');
            option.value = type.id;
            // For Ionic icons, we'll show the icon name; for emojis, show the emoji
            // Note: HTML options cannot display ion-icon elements directly
            const displayText = type.icon.startsWith('ion-') ? type.icon : type.icon;
            option.textContent = `${displayText} ${type.name}`;
            option.style.color = type.color;
            option.setAttribute('data-icon', type.icon);
            artifactTypeSelect.appendChild(option);
        });
    }
    
    // Update dropdown manager if available
    if (dropdownManager) {
        dropdownManager.updateDropdownOptions();
    }
}

// Dropdown creation is now handled by the CustomDropdownManager class

function updateStatusFormOptions() {
    // Update the status form dropdown
    const artifactStatusSelect = document.getElementById('artifactStatus');
    if (artifactStatusSelect && artifactStatuses.length > 0) {
        // Clear existing options
        artifactStatusSelect.innerHTML = '<option value="">Select Status</option>';
        
        // Add options for each status
        artifactStatuses.forEach(status => {
            const option = document.createElement('option');
            option.value = status.id;
            option.textContent = `${status.icon} ${status.name}`;
            option.style.color = status.color;
            artifactStatusSelect.appendChild(option);
        });
    }
    
    // Update the status filter dropdown
    const statusFilter = document.getElementById('statusFilter');
    if (statusFilter && artifactStatuses.length > 0) {
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
    
    // Update dropdown manager if available
    if (dropdownManager) {
        dropdownManager.updateDropdownOptions();
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

// Custom dropdown value setting is now handled by the CustomDropdownManager class



// Tile-related functions are now handled by the TileManager class

// Modal Management
function openCreateModal() {
    editingArtifactId = null;
    document.getElementById('modalTitle').textContent = 'Create New Artifact';
    document.getElementById('artifactForm').reset();
    
    // Set submit button text to "Create"
    const submitButton = document.getElementById('submitButton');
    if (submitButton) {
        submitButton.textContent = 'Create';
    }
    
    // Debug: Log the current state
    console.log('openCreateModal: workItemTypes.length =', workItemTypes.length);
    console.log('openCreateModal: artifactStatuses.length =', artifactStatuses.length);
    
    // Check if configuration is loaded
    if (workItemTypes.length === 0 || artifactStatuses.length === 0) {
        console.log('Configuration not loaded yet, waiting for it...');
        // Wait for configuration to be loaded using polling
        const checkConfig = () => {
            if (workItemTypes.length > 0 && artifactStatuses.length > 0) {
                console.log('Configuration loaded, now opening modal...');
                openModalWithConfig();
            } else {
                console.log('Still waiting for configuration...');
                setTimeout(checkConfig, 100);
            }
        };
        checkConfig();
        return; // Exit early, modal will be opened by checkConfig
    }
    
    // Configuration is already loaded, open modal immediately
    openModalWithConfig();
}

function openModalWithConfig() {
    console.log('Opening modal with configuration loaded');
    
    // Ensure dropdown options are populated before opening modal
    if (workItemTypes.length > 0) {
        console.log('Populating type dropdown options...');
        updateTypeFilterOptions();
    } else {
        console.error('Failed to load workItemTypes');
    }
    
    if (artifactStatuses.length > 0) {
        console.log('Populating status dropdown options...');
        updateStatusFormOptions();
    } else {
        console.error('Failed to load artifactStatuses');
    }
    
    // Refresh custom dropdowns to ensure they work properly
    if (dropdownManager) {
        console.log('Refreshing custom dropdowns...');
        dropdownManager.updateDropdownOptions();
        
        // Re-create custom dropdowns for form elements to ensure they work
        const artifactTypeSelect = document.getElementById('artifactType');
        const artifactStatusSelect = document.getElementById('artifactStatus');
        
        if (artifactTypeSelect) {
            dropdownManager.refreshDropdownDisplay(artifactTypeSelect.parentNode.querySelector('.custom-dropdown'));
        }
        
        if (artifactStatusSelect) {
            dropdownManager.refreshDropdownDisplay(artifactStatusSelect.parentNode.querySelector('.custom-dropdown'));
        }
    }
    
    // Set default status to 'open' for new artifacts
    const artifactStatusSelect = document.getElementById('artifactStatus');
    if (artifactStatusSelect) {
        artifactStatusSelect.value = 'open';
    }
    
    // Reset flag checkbox for new artifacts
    const artifactFlaggedCheckbox = document.getElementById('artifactFlagged');
    if (artifactFlaggedCheckbox) {
        artifactFlaggedCheckbox.checked = false;
    }
    
    // Set default verification method for new artifacts
    const artifactVerificationField = document.getElementById('artifactVerification');
    if (artifactVerificationField) {
        artifactVerificationField.value = 'BDD';
    }
    
    // Hide artifact ID display for new artifacts
    document.getElementById('artifactIdDisplay').style.display = 'none';
    document.getElementById('artifactModal').style.display = 'block';
}

function openEditModal(artifactId) {
    editingArtifactId = artifactId;
    const artifact = currentArtifacts.find(a => a.artifact_id === artifactId);
    if (artifact) {
        document.getElementById('modalTitle').textContent = 'Edit Artifact';
        
        // Set submit button text to "Save"
        const submitButton = document.getElementById('submitButton');
        if (submitButton) {
            submitButton.textContent = 'Save';
        }
        
        // Set values on form fields
        document.getElementById('artifactSummary').value = artifact.summary;
        document.getElementById('artifactDescription').value = artifact.description || '';
        document.getElementById('artifactCategory').value = artifact.category || '';
        document.getElementById('artifactVerification').value = artifact.verification || 'BDD';
        document.getElementById('artifactFlagged').checked = artifact.flagged || false;
        
        // Set values on custom dropdowns
        const artifactTypeSelect = document.getElementById('artifactType');
        const artifactStatusSelect = document.getElementById('artifactStatus');
        
        if (artifactTypeSelect) {
            // Check if it's a custom dropdown by looking for the custom dropdown element
            let customDropdown = null;
            if (artifactTypeSelect.classList.contains('custom-dropdown')) {
                customDropdown = artifactTypeSelect;
            } else {
                // Look for the custom dropdown that replaced this select
                customDropdown = artifactTypeSelect.parentNode.querySelector('.custom-dropdown');
            }
            
            if (customDropdown && customDropdown.classList.contains('custom-dropdown')) {
                dropdownManager.setCustomDropdownValue(customDropdown, artifact.type);
            } else {
                // Fallback to native select
                artifactTypeSelect.value = artifact.type;
            }
        }
        
        if (artifactStatusSelect) {
            // Check if it's a custom dropdown by looking for the custom dropdown element
            let customDropdown = null;
            if (artifactStatusSelect.classList.contains('custom-dropdown')) {
                customDropdown = artifactStatusSelect;
            } else {
                // Look for the custom dropdown that replaced this select
                customDropdown = artifactStatusSelect.parentNode.querySelector('.custom-dropdown');
            }
            
            if (customDropdown && customDropdown.classList.contains('custom-dropdown')) {
                dropdownManager.setCustomDropdownValue(customDropdown, artifact.status || 'open');
            } else {
                // Fallback to native select
                artifactStatusSelect.value = artifact.status || 'open';
            }
        }
        
        // Show and populate artifact ID display
        const artifactIdDisplay = document.getElementById('artifactIdDisplay');
        const artifactIdLarge = document.getElementById('artifactIdLarge');
        artifactIdDisplay.style.display = 'block';
        artifactIdLarge.textContent = artifact.artifact_id;
        
        document.getElementById('artifactModal').style.display = 'block';
    }
}

function closeModal() {
    document.getElementById('artifactModal').style.display = 'none';
}

// Statistics Management is now handled by the StatisticsManager class

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
        
        // Update tile manager with artifacts
        if (tileManager) {
            tileManager.updateArtifacts(artifacts);
            tileManager.displayArtifacts(artifacts);
        } else {
            // Fallback to old method if tile manager not available
            displayArtifacts(artifacts);
        }
    } catch (error) {
        console.error('Error loading artifacts:', error);
        console.error('Error details:', error.message, error.stack);
        document.getElementById('artifacts-container').innerHTML = '<div class="error">Error loading artifacts: ' + error.message + '</div>';
    }
}

// Artifact display is now handled by the TileManager class

// Search and Filter
async function searchArtifacts(query) {
    if (searchManager) {
        searchManager.setSearchValue(query);
        currentFilterState.search = query.trim();
    } else {
        // Fallback to old method
        currentFilterState.search = query.trim();
    }
    
    // Apply all active filters
    await applyCombinedFilters();
}

async function filterByType(type) {
    // Store the type filter value for combination with other filters
    currentFilterState.type = type;
    
    // Apply all active filters
    await applyCombinedFilters();
}

async function filterByCategory(category, exactMatch = false) {
    if (category.trim() === '') {
        currentFilterState.category = '';
    } else {
        currentFilterState.category = category;
        
        // Update the category filter input box to show the selected category
        const categoryFilter = document.querySelector('input[placeholder="Filter by category..."]');
        if (categoryFilter) {
            categoryFilter.value = category;
        }
    }
    
    // Apply all active filters
    await applyCombinedFilters();
}

async function filterByStatus(status) {
    // Store the status filter value for combination with other filters
    currentFilterState.status = status;
    
    // Apply all active filters
    await applyCombinedFilters();
}

async function applyCombinedFilters() {
    try {
        let artifactsToFilter = currentArtifacts;
        
        // First, apply type filter if active (API call)
        if (currentFilterState.type && currentFilterState.type !== '') {
            const response = await fetch(`${API_BASE}/artifacts?type=${encodeURIComponent(currentFilterState.type)}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            artifactsToFilter = await response.json();
        }
        
        // Then apply local filters (status, category, search)
        let filtered = artifactsToFilter;
        
        if (currentFilterState.status && currentFilterState.status !== '') {
            filtered = filtered.filter(artifact => artifact.status === currentFilterState.status);
        }
        
        if (currentFilterState.category && currentFilterState.category !== '') {
            filtered = filtered.filter(artifact => 
                artifact.category && artifact.category.toLowerCase().includes(currentFilterState.category.toLowerCase())
            );
        }
        
        if (currentFilterState.search && currentFilterState.search !== '') {
            filtered = filtered.filter(artifact => 
                artifact.summary.toLowerCase().includes(currentFilterState.search.toLowerCase()) ||
                (artifact.description && artifact.description.toLowerCase().includes(currentFilterState.search.toLowerCase())) ||
                (artifact.category && artifact.category.toLowerCase().includes(currentFilterState.search.toLowerCase()))
            );
        }
        
        // Apply flag filter
        if (currentFilterState.flagged) {
            filtered = filtered.filter(artifact => artifact.flagged === true);
        }
        
        // Update DOM filter values to keep them in sync
        updateFilterDOMValues();
        
        // Use tile manager to display filtered artifacts
        if (tileManager) {
            tileManager.displayArtifacts(filtered);
        } else {
            // Fallback to old method
            displayArtifacts(filtered);
        }
    } catch (error) {
        console.error('Error applying combined filters:', error);
        // Fallback to showing all artifacts
        if (tileManager) {
            tileManager.displayArtifacts(currentArtifacts);
        } else {
            displayArtifacts(currentArtifacts);
        }
    }
}

function updateFilterDOMValues() {
    // Update type filter dropdown
    const typeFilter = document.getElementById('typeFilter');
    if (typeFilter) {
        typeFilter.value = currentFilterState.type;
    }
    
    // Update status filter dropdown
    const statusFilter = document.getElementById('statusFilter');
    if (statusFilter) {
        statusFilter.value = currentFilterState.status;
    }
    
    // Update category filter input
    const categoryFilter = document.querySelector('input[placeholder="Filter by category..."]');
    if (categoryFilter) {
        categoryFilter.value = currentFilterState.category;
    }
    
    // Update search input
    if (searchManager) {
        searchManager.setSearchValue(currentFilterState.search);
    } else {
        // Fallback to old method
        const searchBox = document.querySelector('input[placeholder="Search artifacts..."]');
        if (searchBox) {
            searchBox.value = currentFilterState.search;
        }
    }
}

// Form Handling
document.getElementById('artifactForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        type: document.getElementById('artifactType').value,
        summary: document.getElementById('artifactSummary').value,
        description: document.getElementById('artifactDescription').value,
        category: document.getElementById('artifactCategory').value,
        status: document.getElementById('artifactStatus').value || 'open',
        verification: document.getElementById('artifactVerification').value || 'BDD',
        flagged: document.getElementById('artifactFlagged').checked
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
            if (statisticsManager) {
                statisticsManager.loadStats();
            }
            
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
            
            if (statisticsManager) {
                statisticsManager.loadStats();
            }
            
            // Load artifacts and then reapply the filter state
            await loadArtifacts();
            applyFilterState(currentFilterState);
        } catch (error) {
            console.error('Error deleting artifact:', error);
            alert('Error deleting artifact: ' + error.message);
        }
    }
}

async function refreshArtifacts() {
    try {
        console.log('refreshArtifacts called');
        
        // Get current filter state
        const currentState = getCurrentFilterState();
        console.log('Current filter state before refresh:', currentState);
        
        // Build query parameters for all active filters
        const params = new URLSearchParams();
        
        if (currentState.type && currentState.type !== '') {
            params.append('type', currentState.type);
        }
        
        if (currentState.status && currentState.status !== '') {
            params.append('status', currentState.status);
        }
        
        if (currentState.category && currentState.category !== '') {
            params.append('category', currentState.category);
        }
        
        if (currentState.search && currentState.search !== '') {
            params.append('search', currentState.search);
        }
        
        // Make API call with filter parameters
        const url = params.toString() ? `${API_BASE}/artifacts?${params.toString()}` : `${API_BASE}/artifacts`;
        console.log('Making refresh API call to:', url);
        
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const artifacts = await response.json();
        console.log('Artifacts received from refresh:', artifacts);
        currentArtifacts = artifacts;
        
        // Apply flag filter locally (since it's not supported by the API yet)
        let filtered = artifacts;
        if (currentState.flagged) {
            filtered = filtered.filter(artifact => artifact.flagged === true);
        }
        
        // Update tile manager with filtered artifacts
        if (tileManager) {
            tileManager.updateArtifacts(filtered);
            tileManager.displayArtifacts(filtered);
        } else {
            // Fallback to old method
            displayArtifacts(filtered);
        }
        
        // Update statistics
        if (statisticsManager) {
            statisticsManager.loadStats();
        }
        
        console.log('Refresh completed successfully');
    } catch (error) {
        console.error('Error in refreshArtifacts:', error);
        // Fallback to loading all artifacts if refresh fails
        loadArtifacts();
    }
}

// Filter State Management
function getCurrentFilterState() {
    // Return a copy of the current filter state
    return { ...currentFilterState };
}

function applyFilterState(filterState) {
    // Restore the filter state
    currentFilterState = { ...filterState };
    
    // Apply all active filters
    applyCombinedFilters();
}

// Event Listeners
window.onclick = function(event) {
    const modal = document.getElementById('artifactModal');
    if (event.target === modal) {
        closeModal();
    }
}

// Cleanup function for managers
function cleanupManagers() {
    if (dropdownManager) {
        dropdownManager.cleanup();
        dropdownManager = null;
    }
    
    if (tileManager) {
        tileManager.cleanup();
        tileManager = null;
    }
    
    if (statisticsManager) {
        statisticsManager.cleanup();
        statisticsManager = null;
    }
    
    if (searchManager) {
        searchManager.cleanup();
        searchManager = null;
    }
}

// Page unload cleanup
window.addEventListener('beforeunload', cleanupManagers);

// Flag functionality
async function toggleArtifactFlag(artifactId) {
    try {
        console.log(`Toggling flag for artifact ${artifactId}`);
        
        // Find the current artifact to get its current flag state
        const artifact = currentArtifacts.find(a => a.artifact_id === artifactId);
        if (!artifact) {
            console.error(`Artifact ${artifactId} not found`);
            return;
        }
        
        const newFlagState = !artifact.flagged;
        
        // Update the artifact via API
        const response = await fetch(`${API_BASE}/artifacts/${artifactId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                flagged: newFlagState
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Update the local artifact state
        artifact.flagged = newFlagState;
        
        // Refresh the display while maintaining current filters
        await applyCombinedFilters();
        
        console.log(`Artifact ${artifactId} flag toggled to ${newFlagState}`);
    } catch (error) {
        console.error('Error toggling artifact flag:', error);
        alert('Error toggling artifact flag: ' + error.message);
    }
}

async function toggleFlagFilter() {
    try {
        // Toggle the flag filter state
        currentFilterState.flagged = !currentFilterState.flagged;
        
        // Update the filter button appearance
        const flagFilterBtn = document.getElementById('flagFilter');
        if (flagFilterBtn) {
            const icon = flagFilterBtn.querySelector('ion-icon');
            if (currentFilterState.flagged) {
                // Active filter - red flag
                icon.name = 'flag';
                flagFilterBtn.style.background = '#dc3545';
                flagFilterBtn.style.color = 'white';
            } else {
                // Inactive filter - grey flag
                icon.name = 'flag-outline';
                flagFilterBtn.style.background = '#6c757d';
                flagFilterBtn.style.color = 'white';
            }
        }
        
        // Apply the filter
        await applyCombinedFilters();
        
        console.log(`Flag filter toggled to: ${currentFilterState.flagged}`);
    } catch (error) {
        console.error('Error toggling flag filter:', error);
    }
}
