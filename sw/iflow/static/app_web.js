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
    search: ''
};

// API base URL
const API_BASE = '/api';

// Initialize the application
document.addEventListener('DOMContentLoaded', async function() {
    console.log('DOM loaded, starting to load data...');
    await loadConfiguration();
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
            
            // Now that both data sets are loaded, create custom dropdowns
            createCustomDropdowns();
        } else {
            console.error('Failed to load artifact statuses:', statusesResponse.status);
        }
    } catch (error) {
        console.error('Error loading configuration:', error);
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
}

function createCustomDropdowns() {
    console.log('createCustomDropdowns called');
    console.log('workItemTypes:', workItemTypes);
    console.log('artifactStatuses:', artifactStatuses);
    
    // Replace the type filter dropdown with a custom one
    const typeFilter = document.getElementById('typeFilter');
    if (typeFilter && !typeFilter.classList.contains('custom-dropdown')) {
        console.log('Creating custom dropdown for type filter');
        createCustomDropdown(typeFilter, 'type', workItemTypes);
    }
    
    // Replace the status filter dropdown with a custom one
    const statusFilter = document.getElementById('statusFilter');
    if (statusFilter && !statusFilter.classList.contains('custom-dropdown')) {
        console.log('Creating custom dropdown for status filter with artifactStatuses:', artifactStatuses);
        createCustomDropdown(statusFilter, 'status', artifactStatuses);
    }
    
    // Replace the form dropdowns with custom ones
    const artifactTypeSelect = document.getElementById('artifactType');
    if (artifactTypeSelect && !artifactTypeSelect.classList.contains('custom-dropdown')) {
        console.log('Creating custom dropdown for artifact type form');
        createCustomDropdown(artifactTypeSelect, 'form', workItemTypes);
    }
    
    const artifactStatusSelect = document.getElementById('artifactStatus');
    if (artifactStatusSelect && !artifactStatusSelect.classList.contains('custom-dropdown')) {
        console.log('Creating custom dropdown for artifact status form');
        createCustomDropdown(artifactStatusSelect, 'status-form', artifactStatuses);
    }
}

function createCustomDropdown(originalSelect, type, items) {
    // Create custom dropdown container
    const customDropdown = document.createElement('div');
    customDropdown.className = 'custom-dropdown';
    customDropdown.style.position = 'relative';
    customDropdown.style.display = 'inline-block';
    customDropdown.style.width = originalSelect.offsetWidth + 'px';
    customDropdown.style.minWidth = '200px';
    customDropdown.style.maxWidth = '300px';
    
    // Create the dropdown button
    const dropdownButton = document.createElement('div');
    dropdownButton.className = 'custom-dropdown-button';
    dropdownButton.style.cssText = `
        padding: 6px 10px;
        border: 1px solid #ccc;
        border-radius: 4px;
        background: white;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: space-between;
        min-height: 32px;
        font-size: 14px;
        line-height: 1.2;
    `;
    
    // Create the selected value display
    const selectedValue = document.createElement('span');
    selectedValue.className = 'custom-dropdown-selected';
    if (type === 'type') {
        selectedValue.textContent = 'All Types';
    } else if (type === 'status') {
        selectedValue.textContent = 'All Statuses';
    } else if (type === 'form') {
        selectedValue.textContent = 'Select Type';
    } else if (type === 'status-form') {
        selectedValue.textContent = 'Select Status';
    }
    
    // Create the dropdown arrow
    const arrow = document.createElement('span');
    arrow.textContent = '▼';
    arrow.style.fontSize = '12px';
    arrow.style.transition = 'transform 0.2s';
    
    dropdownButton.appendChild(selectedValue);
    dropdownButton.appendChild(arrow);
    
    // Create the dropdown options container
    const optionsContainer = document.createElement('div');
    optionsContainer.className = 'custom-dropdown-options';
    optionsContainer.style.cssText = `
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        border: 1px solid #ccc;
        border-top: none;
        border-radius: 0 0 4px 4px;
        max-height: 200px;
        overflow-y: auto;
        z-index: 1000;
        display: none;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        width: 100%;
    `;
    
    // Add default option
    const defaultOption = document.createElement('div');
    defaultOption.className = 'custom-dropdown-option';
    defaultOption.style.cssText = `
        padding: 6px 10px;
        cursor: pointer;
        border-bottom: 1px solid #eee;
        font-size: 14px;
        line-height: 1.2;
    `;
    if (type === 'type') {
        defaultOption.textContent = 'All Types';
    } else if (type === 'status') {
        defaultOption.textContent = 'All Statuses';
    } else if (type === 'form') {
        defaultOption.textContent = 'Select Type';
    } else if (type === 'status-form') {
        defaultOption.textContent = 'Select Status';
    }
    defaultOption.setAttribute('data-value', '');
    optionsContainer.appendChild(defaultOption);
    
    // Add item options
    items.forEach(item => {
        const option = document.createElement('div');
        option.className = 'custom-dropdown-option';
        option.style.cssText = `
            padding: 6px 10px;
            cursor: pointer;
            border-bottom: 1px solid #eee;
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 14px;
            line-height: 1.2;
        `;
        
        // Create icon element
        if (item.icon.startsWith('ion-')) {
            const icon = document.createElement('ion-icon');
            icon.setAttribute('name', item.icon.replace('ion-', ''));
            icon.style.fontSize = '16px';
            icon.style.color = item.color;
            option.appendChild(icon);
        } else {
            const iconSpan = document.createElement('span');
            iconSpan.textContent = item.icon;
            iconSpan.style.fontSize = '16px';
            option.appendChild(iconSpan);
        }
        
        // Add item name
        const nameSpan = document.createElement('span');
        nameSpan.textContent = item.name;
        option.appendChild(nameSpan);
        
        option.setAttribute('data-value', item.id);
        optionsContainer.appendChild(option);
    });
    
    // Add event listeners
    dropdownButton.addEventListener('click', () => {
        const isOpen = optionsContainer.style.display === 'block';
        optionsContainer.style.display = isOpen ? 'none' : 'block';
        arrow.style.transform = isOpen ? 'rotate(0deg)' : 'rotate(180deg)';
    });
    
    // Handle option selection
    optionsContainer.addEventListener('click', (e) => {
        if (e.target.closest('.custom-dropdown-option')) {
            const option = e.target.closest('.custom-dropdown-option');
            const value = option.getAttribute('data-value');
            
            // Update selected value display
            if (value === '') {
                if (type === 'type') {
                    selectedValue.textContent = 'All Types';
                } else if (type === 'status') {
                    selectedValue.textContent = 'All Statuses';
                } else if (type === 'form') {
                    selectedValue.textContent = 'Select Type';
                } else if (type === 'status-form') {
                    selectedValue.textContent = 'Select Status';
                }
            } else {
                const item = items.find(i => i.id === value);
                selectedValue.innerHTML = '';
                
                if (item.icon.startsWith('ion-')) {
                    const icon = document.createElement('ion-icon');
                    icon.setAttribute('name', item.icon.replace('ion-', ''));
                    icon.style.fontSize = '16px';
                    icon.style.color = item.color;
                    selectedValue.appendChild(icon);
                } else {
                    const iconSpan = document.createElement('span');
                    iconSpan.textContent = item.icon;
                    iconSpan.style.fontSize = '16px';
                    selectedValue.appendChild(iconSpan);
                }
                
                const nameSpan = document.createElement('span');
                nameSpan.textContent = ` ${item.name}`;
                selectedValue.appendChild(nameSpan);
            }
            
            // Trigger the original select change event
            originalSelect.value = value;
            originalSelect.dispatchEvent(new Event('change'));
            
            // Close dropdown
            optionsContainer.style.display = 'none';
            arrow.style.transform = 'rotate(0deg)';
        }
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!customDropdown.contains(e.target)) {
            optionsContainer.style.display = 'none';
            arrow.style.transform = 'rotate(0deg)';
        }
    });
    
    // Assemble the custom dropdown
    customDropdown.appendChild(dropdownButton);
    customDropdown.appendChild(optionsContainer);
    
    // Replace the original select
    originalSelect.style.display = 'none';
    originalSelect.parentNode.insertBefore(customDropdown, originalSelect);
}

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
}

function updateProjectHeader() {
    if (projectConfig) {
        const header = document.querySelector('.header h1');
        if (header) {
            header.textContent = `${projectConfig.name} - ${projectConfig.description}`;
        }
    }
}

// Helper function to convert icon names to visual symbols
function convertIconToSymbol(iconName) {
    // Map Ionic icon names to their visual representations
    const iconMap = {
        'ion-flash-outline': '⚡',
        'ion-checkmark-circle': '✅',
        'ion-close-circle': '❌',
        'ion-warning': '⚠️',
        'ion-information-circle': 'ℹ️',
        'ion-heart': '❤️',
        'ion-star': '⭐',
        'ion-home': '🏠',
        'ion-person': '👤',
        'ion-settings': '⚙️',
        'ion-search': '🔍',
        'ion-add': '➕',
        'ion-remove': '➖',
        'ion-arrow-up': '⬆️',
        'ion-arrow-down': '⬇️',
        'ion-arrow-forward': '➡️',
        'ion-arrow-back': '⬅️',
        'ion-menu': '☰',
        'ion-close': '✕',
        'ion-refresh': '🔄',
        'ion-download': '⬇️',
        'ion-upload': '⬆️',
        'ion-mail': '✉️',
        'ion-call': '📞',
        'ion-camera': '📷',
        'ion-image': '🖼️',
        'ion-videocam': '📹',
        'ion-mic': '🎤',
        'ion-musical-notes': '🎵',
        'ion-calendar': '📅',
        'ion-time': '🕐',
        'ion-location': '📍',
        'ion-navigate': '🧭',
        'ion-car': '🚗',
        'ion-bicycle': '🚲',
        'ion-airplane': '✈️',
        'ion-boat': '🚢',
        'ion-train': '🚂',
        'ion-bus': '🚌',
        'ion-truck': '🚛',
        'ion-rocket': '🚀',
        'ion-bulb': '💡',
        'ion-battery-charging': '🔋',
        'ion-wifi': '📶',
        'ion-bluetooth': '📡',
        'ion-phone-portrait': '📱',
        'ion-tablet-portrait': '📱',
        'ion-laptop': '💻',
        'ion-desktop': '🖥️',
        'ion-server': '🖥️',
        'ion-cloud': '☁️',
        'ion-rainy': '🌧️',
        'ion-sunny': '☀️',
        'ion-moon': '🌙',
        'ion-snow': '❄️',
        'ion-thunderstorm': '⛈️',
        'ion-umbrella': '☂️',
        'ion-leaf': '🍃',
        'ion-flower': '🌸',
        'ion-tree': '🌳',
        'ion-fish': '🐟',
        'ion-bird': '🐦',
        'ion-cat': '🐱',
        'ion-dog': '🐕',
        'ion-horse': '🐎',
        'ion-cow': '🐄',
        'ion-pig': '🐷',
        'ion-sheep': '🐑',
        'ion-chicken': '🐔',
        'ion-bee': '🐝',
        'ion-butterfly': '🦋',
        'ion-spider': '🕷️',
        'ion-snake': '🐍',
        'ion-lizard': '🦎',
        'ion-frog': '🐸',
        'ion-turtle': '🐢',
        'ion-crab': '🦀',
        'ion-octopus': '🐙',
        'ion-dolphin': '🐬',
        'ion-whale': '🐋',
        'ion-shark': '🦈',
        'ion-jellyfish': '🪼',
        'ion-starfish': '⭐',
        'ion-coral': '🪸',
        'ion-seashell': '🐚',
        'ion-pearl': '💎',
        'ion-diamond': '💎',
        'ion-ruby': '💎',
        'ion-emerald': '💎',
        'ion-sapphire': '💎',
        'ion-gold': '🥇',
        'ion-silver': '🥈',
        'ion-bronze': '🥉',
        'ion-trophy': '🏆',
        'ion-medal': '🏅',
        'ion-ribbon': '🎗️',
        'ion-crown': '👑',
        'ion-gem': '💎',
        'ion-coins': '🪙',
        'ion-banknote': '💵',
        'ion-credit-card': '💳',
        'ion-receipt': '🧾',
        'ion-calculator': '🧮',
        'ion-abacus': '🧮',
        'ion-chart': '📊',
        'ion-graph': '📈',
        'ion-pie-chart': '🥧',
        'ion-bar-chart': '📊',
        'ion-line-chart': '📈',
        'ion-area-chart': '📊',
        'ion-scatter-plot': '📊',
        'ion-histogram': '📊',
        'ion-box-plot': '📦',
        'ion-violin-plot': '🎻',
        'ion-heatmap': '🔥',
        'ion-tree-map': '🗺️',
        'ion-sankey': '🌊',
        'ion-chord': '🎵',
        'ion-force': '💪',
        'ion-cluster': '🔗',
        'ion-bubble': '🫧',
        'ion-scatter': '✨',
        'ion-bubble-chart': '🫧',
        'ion-radar': '📡',
        'ion-polar': '🧭',
        'ion-candlestick': '🕯️',
        'ion-ohlc': '📊',
        'ion-kagi': '📊',
        'ion-renko': '🧱',
        'ion-point-and-figure': '📊',
        'ion-ichimoku': '☁️',
        'ion-macd': '📊',
        'ion-rsi': '📊',
        'ion-bollinger': '📊',
        'ion-fibonacci': '📐',
        'ion-elliott-wave': '🌊',
        'ion-harmonic': '🎵',
        'ion-pattern': '🔍',
        'ion-support': '🆘',
        'ion-resistance': '🛡️',
        'ion-trend': '📈',
        'ion-breakout': '🚀',
        'ion-breakdown': '📉',
        'ion-consolidation': '📊',
        'ion-accumulation': '📈',
        'ion-distribution': '📊',
        'ion-manipulation': '🎭',
        'ion-pump': '📈',
        'ion-dump': '📉',
        'ion-squeeze': '🫧',
        'ion-short': '📉',
        'ion-long': '📈',
        'ion-bull': '🐂',
        'ion-bear': '🐻',
        'ion-whale': '🐋',
        'ion-shark': '🦈',
        'ion-piranha': '🐟',
        'ion-minnow': '🐟',
        'ion-guppy': '🐟',
        'ion-goldfish': '🐟',
        'ion-koi': '🐟',
        'ion-angelfish': '🐟',
        'ion-betta': '🐟',
        'ion-tetra': '🐟',
        'ion-platy': '🐟',
        'ion-molly': '🐟',
        'ion-swordtail': '🐟',
        'ion-livebearer': '🐟',
        'ion-egg-layer': '🥚',
        'ion-bubble-nest': '🫧',
        'ion-cave-spawner': '🕳️',
        'ion-substrate-spawner': '🌱',
        'ion-mouthbrooder': '👄',
        'ion-pouch-brooder': '👛',
        'ion-gill-brooder': '🫁',
        'ion-skin-brooder': '🦠',
        'ion-egg-eater': '🥚',
        'ion-fry-eater': '🐟',
        'ion-adult-eater': '🐟',
        'ion-herbivore': '🌿',
        'ion-carnivore': '🥩',
        'ion-omnivore': '🍽️',
        'ion-filter-feeder': '🔍',
        'ion-grazer': '🌱',
        'ion-browser': '🌿',
        'ion-picker': '✋',
        'ion-sifter': '🔍',
        'ion-scraper': '🔧',
        'ion-rasper': '🔧',
        'ion-crusher': '🦷',
        'ion-grinder': '🦷',
        'ion-cutter': '✂️',
        'ion-piercer': '🔪',
        'ion-sucker': '👄',
        'ion-picker': '✋',
        'ion-grazer': '🌱',
        'ion-browser': '🌿',
        'ion-picker': '✋',
        'ion-sifter': '🔍',
        'ion-scraper': '🔧',
        'ion-rasper': '🔧',
        'ion-crusher': '🦷',
        'ion-grinder': '🦷',
        'ion-cutter': '✂️',
        'ion-piercer': '🔪',
        'ion-sucker': '👄'
    };
    
    // If it's an Ionic icon, return the mapped symbol, otherwise return the icon as-is
    if (iconName.startsWith('ion-')) {
        return iconMap[iconName] || iconName; // Fallback to original if not mapped
    }
    
    // Return emojis and other icons as-is
    return iconName;
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
    console.log('getStatusDisplayInfo called with statusId:', statusId);
    console.log('artifactStatuses array:', artifactStatuses);
    console.log('artifactStatuses length:', artifactStatuses ? artifactStatuses.length : 'undefined');
    
    // Handle empty or undefined statusId
    if (!statusId || statusId === '') {
        console.log('Empty statusId, returning default "open" status');
        if (artifactStatuses && artifactStatuses.length > 0) {
            const defaultStatus = artifactStatuses.find(status => status.id === 'open');
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
    
    if (artifactStatuses && artifactStatuses.length > 0) {
        const statusInfo = artifactStatuses.find(status => status.id === statusId);
        console.log('Found statusInfo:', statusInfo);
        if (statusInfo) {
            return {
                "name": statusInfo.name,
                "icon": statusInfo.icon,
                "color": statusInfo.color
            };
        }
    }
    console.log('Returning fallback status info for:', statusId);
    return {
        "name": statusId || "Unknown",
        "icon": "⚪",
        "color": "#6B7280"
    };
}

// Modal Management
function openCreateModal() {
    editingArtifactId = null;
    document.getElementById('modalTitle').textContent = 'Create New Artifact';
    document.getElementById('artifactForm').reset();
    
    // Set default status to 'open' for new artifacts
    const artifactStatusSelect = document.getElementById('artifactStatus');
    if (artifactStatusSelect) {
        artifactStatusSelect.value = 'open';
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
        document.getElementById('artifactType').value = artifact.type;
        document.getElementById('artifactSummary').value = artifact.summary;
        document.getElementById('artifactDescription').value = artifact.description || '';
        document.getElementById('artifactCategory').value = artifact.category || '';
        document.getElementById('artifactStatus').value = artifact.status || 'open';
        
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
    currentFilterState.search = query.trim();
    
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
        
        // Update DOM filter values to keep them in sync
        updateFilterDOMValues();
        
        displayArtifacts(filtered);
    } catch (error) {
        console.error('Error applying combined filters:', error);
        // Fallback to showing all artifacts
        displayArtifacts(currentArtifacts);
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
    const searchBox = document.querySelector('input[placeholder="Search artifacts..."]');
    if (searchBox) {
        searchBox.value = currentFilterState.search;
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
        status: document.getElementById('artifactStatus').value || 'open'
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
    
    // Reset filter state
    currentFilterState = {
        type: '',
        status: '',
        category: '',
        search: ''
    };
    
    loadStats();
    loadArtifacts();
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
