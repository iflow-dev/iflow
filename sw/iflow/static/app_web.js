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

// Global error handling
let globalErrorHandler = null;

// Initialize the managers
let dropdownManager = null;
let statisticsManager = null;

// API base URL
const API_BASE = '/api';

// Legacy function - no longer needed
function cyclestate() {
    console.log('cyclestate() deprecated - filters handle their own state now');
}

// Initialize application components
async function initializeApp() {
    try {
        // Load views using composite approach for complex views
        const containers = document.querySelectorAll('[data-view]');
        
        for (const container of containers) {
            const viewName = container.dataset.view;
            if (viewName === 'filter') {
                await ViewLoader.loadCompositeView(viewName, container);
            } else {
                await ViewLoader.load(viewName, container);
            }
        }
        
        // Auto-discover and setup filter controls
        FilterControl.setupAllFilters();
        
        // Initialize managers after views are loaded
        await initializeManagers();
        
        // Connect filters to FilterManager
        if (window.filterManager) {
            FilterControl.connectToFilterManager(window.filterManager);
        }
        
        console.log('Application initialized successfully');
        
    } catch (error) {
        console.error('Error initializing application:', error);
    }
}

// Initialize all managers after views are loaded
async function initializeManagers() {
    try {
        console.log('Initializing managers...');
        
        // Update filter options now that DOM elements exist
        updateStatusFilterOptions();
        updateStatusFormOptions();
        
        // Initialize managers with the loaded data
        dropdownManager = new CustomDropdownManager();
        statisticsManager = new StatisticsManager();
        
        // Get singleton instances (these set window.tileManager, window.searchManager, window.filterManager)
        TileManager.getInstance();
        SearchManager.getInstance();
        FilterManager.getInstance();
        
        // Initialize managers in dependency order
        if (dropdownManager.initializeData(workItemTypes, artifactStatuses)) {
            dropdownManager.createCustomDropdowns();
            // Expose dropdown accessibility functions for testing (Ticket #00073)
            dropdownManager.exposeForTesting();
        }
        
        if (window.tileManager.initializeData(workItemTypes, artifactStatuses)) {
            console.log('Tile manager initialized successfully');
        }
        
        if (statisticsManager) {
            statisticsManager.initialize(projectConfig);
        }
        
        // Initialize search manager with tile manager reference
        if (window.searchManager) {
            window.searchManager.initialize(window.tileManager);
        }
        
        // Initialize filter manager with search manager reference
        if (window.filterManager) {
            window.filterManager.initialize(window.searchManager);
        }
        
        // Toolbar initialization is now handled by filter auto-discovery
        
        // Initialize UI components
        if (window.statusLine) {
            window.statusLine.initialize();
        }
        
        if (window.statisticsLine) {
            window.statisticsLine.initialize();
        }
        
        if (window.statusLine) {
            window.statusLine.showInfo(`Loaded ${artifactStatuses.length} artifact statuses`);
        }
        
        console.log('All managers initialized successfully');
        
        // Load artifacts after everything is initialized
        await loadArtifacts();
        
    } catch (error) {
        console.error('Error initializing managers:', error);
        if (window.statusLine) {
            window.statusLine.showError('Manager initialization failed: ' + error.message);
        }
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', async function() {
    console.log('DOM loaded, starting to load data...');
    
    // Set up global error handling
    setupGlobalErrorHandling();
    console.log('Global error handling set up');
    
    try {
        console.log('Starting configuration loading...');
        await loadConfiguration();
        console.log('Configuration loaded successfully');
        
        // Initialize application with auto-discovery approach
        await initializeApp();
        
    } catch (error) {
        console.error('Error during application initialization:', error);
        if (window.statusLine) {
            window.statusLine.showError('Application initialization failed: ' + error.message);
        }
    }
});

// Global Error Handling
function setupGlobalErrorHandling() {
    // Catch unhandled promise rejections
    window.addEventListener('unhandledrejection', function(event) {
        console.error('Unhandled promise rejection:', event.reason);
        if (window.statusLine) {
            window.statusLine.showError('Unhandled error: ' + (event.reason?.message || event.reason || 'Unknown error'));
        }
        event.preventDefault();
    });
    
    // Catch global JavaScript errors
    window.addEventListener('error', function(event) {
        console.error('Global JavaScript error:', event.error);
        if (window.statusLine) {
            window.statusLine.showError('JavaScript error: ' + (event.error?.message || event.message || 'Unknown error'));
        }
        event.preventDefault();
    });
    
    // Catch fetch errors globally
    const originalFetch = window.fetch;
    window.fetch = async function(...args) {
        try {
            const response = await originalFetch(...args);
            if (!response.ok) {
                const errorText = `HTTP ${response.status}: ${response.statusText}`;
                console.error('Fetch error:', errorText);
                if (window.statusLine) {
                    window.statusLine.showError(errorText);
                }
            }
            return response;
        } catch (error) {
            console.error('Fetch error:', error);
            if (window.statusLine) {
                window.statusLine.showError('Network error: ' + error.message);
            }
            throw error;
        }
    };
}

// Error status line functionality is now handled by the StatusLine class

// Success status line functionality is now handled by the StatusLine class

// Info status line functionality is now handled by the StatusLine class

// Configuration Management
async function loadConfiguration() {
    try {
        console.log('Loading project configuration...');
        console.log('API_BASE:', API_BASE);
        
        // Load project info
        const projectResponse = await fetch(`${API_BASE}/project-info`);
        console.log('Project info response status:', projectResponse.status);
        if (projectResponse.ok) {
            projectConfig = await projectResponse.json();
            console.log('Project config loaded:', projectConfig);
            updateProjectHeader();
            if (window.statusLine) {
            window.statusLine.showInfo('Project configuration loaded');
        }
        } else {
            if (window.statusLine) {
            window.statusLine.showError(`Failed to load project info: HTTP ${projectResponse.status}`);
        }
        }
        
        // Load work item types
        const typesResponse = await fetch(`${API_BASE}/work-item-types`);
        if (typesResponse.ok) {
            workItemTypes = await typesResponse.json();
            console.log('Work item types loaded:', workItemTypes);
            console.log('workItemTypes array length:', workItemTypes.length);
            updateTypeFilterOptions();
            if (window.statusLine) {
            window.statusLine.showInfo(`Loaded ${workItemTypes.length} work item types`);
        }
        } else {
            console.error('Failed to load work item types:', typesResponse.status);
            if (window.statusLine) {
            window.statusLine.showError(`Failed to load work item types: HTTP ${typesResponse.status}`);
        }
        }
        
        // Load artifact statuses
        const statusesResponse = await fetch(`${API_BASE}/artifact-statuses`);
        if (statusesResponse.ok) {
            artifactStatuses = await statusesResponse.json();
            console.log('Artifact statuses loaded:', artifactStatuses);
            
            // Don't initialize managers here - wait for views to be loaded
            console.log('Artifact statuses loaded, waiting for views to initialize managers...');
        } else {
            console.error('Failed to load artifact statuses:', statusesResponse.status);
            if (window.statusLine) {
            window.statusLine.showError(`Failed to load artifact statuses: HTTP ${statusesResponse.status}`);
        }
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
        statusFilter.innerHTML = '<option value="">All</option>';
        
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
        typeFilter.innerHTML = '<option value="">All</option>';
        
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
        statusFilter.innerHTML = '<option value="">All</option>';
        
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
    
    // Set default status to the first status from the status list for new artifacts
    const artifactStatusSelect = document.getElementById('artifactStatus');
    if (artifactStatusSelect && artifactStatuses.length > 0) {
        artifactStatusSelect.value = artifactStatuses[0].id;
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
        document.getElementById('artifactActivity').value = artifact.activity || '';
        document.getElementById('artifactIteration').value = artifact.iteration || '';
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
                dropdownManager.setCustomDropdownValue(customDropdown, artifact.status || (artifactStatuses.length > 0 ? artifactStatuses[0].id : 'open'));
            } else {
                // Fallback to native select
                artifactStatusSelect.value = artifact.status || (artifactStatuses.length > 0 ? artifactStatuses[0].id : 'open');
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
        
        // Update the filtered count display using StatusLine
        if (window.statusLine) {
            window.statusLine.updateFilteredCount(artifacts.length);
        }
        
        // Update tile manager with artifacts
        if (window.tileManager) {
            window.tileManager.updateArtifacts(artifacts);
            window.tileManager.displayArtifacts(artifacts);
            if (window.statusLine) {
                window.statusLine.showSuccess(`Loaded ${artifacts.length} artifacts successfully`);
            }
        } else {
            // Fallback to old method if tile manager not available
            displayArtifacts(artifacts);
            if (window.statusLine) {
            window.statusLine.showInfo(`Loaded ${artifacts.length} artifacts (using fallback display)`);
        }
        }
    } catch (error) {
        console.error('Error loading artifacts:', error);
        console.error('Error details:', error.message, error.stack);
        if (window.statusLine) {
            window.statusLine.showError('Failed to load artifacts: ' + error.message);
        }
        document.getElementById('artifacts-container').innerHTML = '<div class="error">Error loading artifacts: ' + error.message + '</div>';
    }
}

// Artifact display is now handled by the TileManager class

// Filtered count is now handled by the StatusLine class

// Fallback display function if TileManager is not available
function displayArtifacts(artifacts) {
    console.log('Using fallback displayArtifacts function');
    const container = document.getElementById('artifacts-container');
    if (!container) {
        console.error('Artifacts container not found');
        return;
    }
    
    if (!artifacts || artifacts.length === 0) {
        container.innerHTML = '<div class="no-results">No artifacts found</div>';
        return;
    }
    
    // Clear existing content
    container.innerHTML = '';
    
    // Create simple artifact tiles
    artifacts.forEach(artifact => {
        const tile = document.createElement('div');
        tile.className = 'artifact-tile';
        tile.innerHTML = `
            <div class="tile-header">
                <span class="artifact-id">${artifact.artifact_id}</span>
                <span class="artifact-type">${artifact.type || 'N/A'}</span>
                <span class="artifact-status">${artifact.status || 'N/A'}</span>
            </div>
            <div class="tile-summary">${artifact.summary || 'No summary'}</div>
            <div class="tile-category">${artifact.category || 'No category'}</div>
        `;
        container.appendChild(tile);
    });
}

// Search and filter functionality is now handled by the toolbar and filter managers

// Clear all filters functionality is now handled by the toolbar



async function filterByType(type) {
    if (window.filterManager) {
        window.filterManager.updateFilter('type', type);
    } else {
        console.warn('FilterManager not available');
    }
}

async function filterByStatus(status) {
    if (window.filterManager) {
        window.filterManager.updateFilter('status', status);
    } else {
        console.warn('FilterManager not available');
    }
}

// Old applyCombinedFilters function removed - now handled by FilterManager + SearchManager

// Old filter state management functions removed - now handled by FilterManager

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
        activity: document.getElementById('artifactActivity').value || '',
        iteration: document.getElementById('artifactIteration').value || '',
        flagged: document.getElementById('artifactFlagged').checked
    };
    
            try {
                // Capture current filter state before editing
                const currentFilterState = window.filterManager ? window.filterManager.getFilter() : {};
                
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
                if (window.filterManager && currentFilterState) {
                    window.filterManager.applyFilterState(currentFilterState);
                }
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
            const currentFilterState = window.filterManager ? window.filterManager.getFilter() : {};
            
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
            if (window.filterManager && currentFilterState) {
                window.filterManager.applyFilterState(currentFilterState);
            }
        } catch (error) {
            console.error('Error deleting artifact:', error);
            alert('Error deleting artifact: ' + error.message);
        }
    }
}

async function refreshArtifacts() {
    try {
        console.log('refreshArtifacts called');
        
        // Get current filter state from FilterManager
        const currentState = window.filterManager ? window.filterManager.getFilter() : {};
        console.log('Current filter state before refresh:', currentState);
        
        // Use SearchManager to refresh with current filters
        if (window.searchManager) {
            await window.searchManager.updateSearchResults(currentState);
        } else {
            // Fallback to loading all artifacts if SearchManager not available
            await loadArtifacts();
        }
        
        // Update statistics
        if (statisticsManager) {
            statisticsManager.loadStats();
        }
        
        console.log('Refresh completed successfully');
    } catch (error) {
        console.error('Error in refreshArtifacts:', error);
        // Fallback to loading all artifacts if refresh fails
        await loadArtifacts();
    }
}

// Filter state management now handled by FilterManager

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
    
    if (window.tileManager) {
        window.tileManager.cleanup();
        window.tileManager = null;
    }
    
    if (statisticsManager) {
        statisticsManager.cleanup();
        statisticsManager = null;
    }
    
    if (window.searchManager) {
        window.searchManager.cleanup();
        window.searchManager = null;
    }
    
    if (window.filterManager) {
        window.filterManager = null;
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
        
        // Refresh the display
        if (window.tileManager) {
            window.tileManager.refreshTiles();
        }
        
        console.log(`Artifact ${artifactId} flag toggled to ${newFlagState}`);
    } catch (error) {
        console.error('Error toggling artifact flag:', error);
        alert('Error toggling artifact flag: ' + error.message);
    }
}

// Flag filter functionality is now handled by the toolbar class

// Text input filter functionality is now handled by the toolbar class

