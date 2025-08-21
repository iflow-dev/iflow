/**
 * Enhanced View Loader with Template Support
 * Auto-loads views into containers based on data attributes and supports templating
 */
class ViewLoader {
    static async loadAll() {
        const containers = document.querySelectorAll('[data-view]');
        
        for (const container of containers) {
            const viewName = container.dataset.view;
            await ViewLoader.load(viewName, container);
        }
        
        console.log(`Loaded ${containers.length} views`);
    }
    
    static async load(viewName, container, params = {}) {
        try {
            const response = await fetch(`/static/view/${viewName}.html`);
            if (!response.ok) {
                throw new Error(`Failed to load ${viewName}: ${response.status}`);
            }
            
            let html = await response.text();
            
            // Apply template parameters if provided
            html = ViewLoader.applyTemplate(html, params);
            
            container.innerHTML = html;
            
        } catch (error) {
            console.error(`Error loading view ${viewName}:`, error);
            container.innerHTML = `<div class="error">Error loading ${viewName}: ${error.message}</div>`;
        }
    }
    
    static async loadTemplate(templateName, params = {}) {
        try {
            // Load toolbar templates from the toolbar subdirectory
            const response = await fetch(`/static/view/toolbar/${templateName}.html`);
            if (!response.ok) {
                throw new Error(`Failed to load template ${templateName}: ${response.status}`);
            }
            
            let html = await response.text();
            return ViewLoader.applyTemplate(html, params);
            
        } catch (error) {
            console.error(`Error loading template ${templateName}:`, error);
            return `<div class="error">Error loading template ${templateName}: ${error.message}</div>`;
        }
    }
    
    static applyTemplate(html, params) {
        // Replace template placeholders {KEY} with values
        return html.replace(/\{([^}]+)\}/g, (match, key) => {
            return params[key] !== undefined ? params[key] : match;
        });
    }
    
    static async loadCompositeView(viewName, container) {
        try {
            // Special handling for composite views that use templates
            if (viewName === 'filter') {
                await ViewLoader.loadFilterView(container);
                return;
            }
            
            // Default single view loading
            await ViewLoader.load(viewName, container);
            
        } catch (error) {
            console.error(`Error loading composite view ${viewName}:`, error);
            container.innerHTML = `<div class="error">Error loading ${viewName}: ${error.message}</div>`;
        }
    }
    
    static async loadFilterView(container) {
        // Compose the filter view from individual filter templates
        const filters = [
            { template: 'icon-button', params: { 
                FILTER_TYPE: 'create', 
                ACTION: 'openCreateModal()', 
                ICON: 'create-outline.svg', 
                ALT_TEXT: 'Create', 
                TITLE: 'Create new artifact', 
                FILTER_LABEL: 'create',
                WRAPPER_ID: '',
                BUTTON_ID: ''
            }},
            { template: 'text-filter', params: { 
                FILTER_TYPE: 'search', 
                FILTER_ID: 'search-input', 
                PLACEHOLDER: 'type to filter...', 
                CLEAR_TITLE: 'Clear search', 
                FILTER_ID_TITLE: 'Search', 
                FILTER_LABEL: 'text' 
            }},
            { template: 'dropdown-filter', params: { 
                FILTER_TYPE: 'type', 
                FILTER_ID: 'typeFilter', 
                FILTER_LABEL: 'Type' 
            }},
            { template: 'dropdown-filter', params: { 
                FILTER_TYPE: 'status', 
                FILTER_ID: 'statusFilter', 
                FILTER_LABEL: 'Status' 
            }},
            { template: 'text-filter', params: { 
                FILTER_TYPE: 'category', 
                FILTER_ID: 'categoryFilter', 
                PLACEHOLDER: 'type to filter...', 
                CLEAR_TITLE: 'Clear category filter', 
                FILTER_ID_TITLE: 'Category', 
                FILTER_LABEL: 'Category' 
            }},
            { template: 'icon-filter', params: { 
                FILTER_TYPE: 'flag', 
                FILTER_ID: 'flagFilter', 
                ICON: 'flag.svg', 
                ALT_TEXT: 'Flag', 
                TITLE: 'Filter flagged artifacts', 
                ICON_ID: 'flagIcon', 
                FILTER_LABEL: 'Flag' 
            }},
            { template: 'icon-button', params: { 
                FILTER_TYPE: 'clear', 
                ACTION: 'clearAllFilters()', 
                ICON: 'close.svg', 
                ALT_TEXT: 'Clear', 
                TITLE: 'Clear all filters', 
                FILTER_LABEL: 'clear',
                WRAPPER_ID: 'id="clearAllWrapper"',
                BUTTON_ID: 'id="clearAllFilters"'
            }},
            { template: 'icon-button', params: { 
                FILTER_TYPE: 'refresh', 
                ACTION: 'refreshArtifacts()', 
                ICON: 'refresh-outline.svg', 
                ALT_TEXT: 'Refresh', 
                TITLE: 'Refresh artifacts', 
                FILTER_LABEL: 'refresh',
                WRAPPER_ID: '',
                BUTTON_ID: 'id="refreshArtifacts"'
            }}
        ];
        
        let compositeHtml = '<!-- Filter Controls -->\n';
        
        for (const filter of filters) {
            const filterHtml = await ViewLoader.loadTemplate(filter.template, filter.params);
            compositeHtml += filterHtml + '\n';
        }
        
        container.innerHTML = compositeHtml;
        console.log('Loaded composite filter view with templates');
    }
}
