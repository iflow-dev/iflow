/**
 * Simple View Loader
 * Auto-loads views into containers based on data attributes
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
    
    static async load(viewName, container) {
        try {
            const response = await fetch(`/static/view/${viewName}.html`);
            if (!response.ok) {
                throw new Error(`Failed to load ${viewName}: ${response.status}`);
            }
            
            const html = await response.text();
            container.innerHTML = html;
            
        } catch (error) {
            console.error(`Error loading view ${viewName}:`, error);
            container.innerHTML = `<div class="error">Error loading ${viewName}: ${error.message}</div>`;
        }
    }
}
