/**
 * StartSmart Search
 * JavaScript functionality for search features
 */

document.addEventListener('DOMContentLoaded', function() {
    // Global search functionality
    const globalSearch = document.getElementById('global-search');
    
    if (globalSearch) {
        const searchInput = globalSearch.querySelector('input');
        const searchResults = document.getElementById('search-results');
        
        if (searchInput && searchResults) {
            let searchTimeout;
            
            searchInput.addEventListener('input', function() {
                const query = this.value.trim();
                
                // Clear previous timeout
                clearTimeout(searchTimeout);
                
                // Hide results if query is empty
                if (!query) {
                    searchResults.style.display = 'none';
                    return;
                }
                
                // Set timeout to prevent too many requests
                searchTimeout = setTimeout(function() {
                    // Make API request
                    fetch(`/api/search?q=${encodeURIComponent(query)}`)
                        .then(response => response.json())
                        .then(data => {
                            // Clear previous results
                            searchResults.innerHTML = '';
                            
                            // Show results container
                            searchResults.style.display = 'block';
                            
                            // Check if there are results
                            if (data.results && data.results.length > 0) {
                                // Create results list
                                const resultsList = document.createElement('div');
                                resultsList.className = 'list-group';
                                
                                // Add results
                                data.results.forEach(result => {
                                    const resultItem = document.createElement('a');
                                    resultItem.className = 'list-group-item list-group-item-action';
                                    resultItem.href = getResultUrl(result);
                                    
                                    const resultContent = `
                                        <div class="d-flex w-100 justify-content-between">
                                            <h6 class="mb-1">${result.title}</h6>
                                            <small class="text-muted">${result.type}</small>
                                        </div>
                                        <p class="mb-1">${result.subtitle || ''}</p>
                                    `;
                                    
                                    resultItem.innerHTML = resultContent;
                                    resultsList.appendChild(resultItem);
                                });
                                
                                searchResults.appendChild(resultsList);
                            } else {
                                // Show no results message
                                searchResults.innerHTML = '<div class="p-3 text-center text-muted">No results found</div>';
                            }
                        })
                        .catch(error => {
                            console.error('Search error:', error);
                            searchResults.innerHTML = '<div class="p-3 text-center text-danger">Error performing search</div>';
                        });
                }, 300);
            });
            
            // Close search results when clicking outside
            document.addEventListener('click', function(e) {
                if (!globalSearch.contains(e.target)) {
                    searchResults.style.display = 'none';
                }
            });
            
            // Helper function to get URL for result
            function getResultUrl(result) {
                switch (result.type) {
                    case 'job':
                        return `/job/${result.id}`;
                    case 'startup':
                        return `/startup/${result.id}`;
                    case 'mentor':
                        return `/view-profile/${result.id}`;
                    default:
                        return '#';
                }
            }
        }
    }
    
    // Job search functionality
    const jobSearchForm = document.getElementById('job-search-form');
    
    if (jobSearchForm) {
        const searchInput = jobSearchForm.querySelector('input[name="search"]');
        const locationInput = jobSearchForm.querySelector('input[name="location"]');
        const jobTypeSelect = jobSearchForm.querySelector('select[name="job_type"]');
        
        // Update URL with search parameters
        function updateSearchParams() {
            const searchParams = new URLSearchParams();
            
            if (searchInput && searchInput.value.trim()) {
                searchParams.set('search', searchInput.value.trim());
            }
            
            if (locationInput && locationInput.value.trim()) {
                searchParams.set('location', locationInput.value.trim());
            }
            
            if (jobTypeSelect && jobTypeSelect.value) {
                searchParams.set('job_type', jobTypeSelect.value);
            }
            
            // Update URL without reloading page
            const newUrl = `${window.location.pathname}?${searchParams.toString()}`;
            window.history.replaceState({}, '', newUrl);
        }
        
        // Add event listeners to form elements
        if (searchInput) {
            searchInput.addEventListener('input', updateSearchParams);
        }
        
        if (locationInput) {
            locationInput.addEventListener('input', updateSearchParams);
        }
        
        if (jobTypeSelect) {
            jobTypeSelect.addEventListener('change', function() {
                updateSearchParams();
                jobSearchForm.submit();
            });
        }
    }
});