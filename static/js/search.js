// Real-time search functionality
let searchTimeout;

function initializeSearch() {
    const searchInput = document.getElementById('globalSearch');
    const searchResults = document.getElementById('searchResults');
    
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length < 2) {
            searchResults.style.display = 'none';
            return;
        }
        
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 300);
    });
    
    // Hide results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });
}

function performSearch(query) {
    fetch(`/api/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            displaySearchResults(data.results);
        })
        .catch(error => {
            console.error('Search error:', error);
        });
}

function displaySearchResults(results) {
    const searchResults = document.getElementById('searchResults');
    
    if (results.length === 0) {
        searchResults.innerHTML = '<div class="p-3 text-muted">No results found</div>';
    } else {
        let html = '';
        results.forEach(result => {
            const icon = result.type === 'job' ? '💼' : '🚀';
            html += `
                <div class="search-result-item p-2 border-bottom">
                    <div class="d-flex align-items-center">
                        <span class="me-2">${icon}</span>
                        <div>
                            <div class="fw-bold">${result.title}</div>
                            <small class="text-muted">${result.subtitle}</small>
                        </div>
                    </div>
                </div>
            `;
        });
        searchResults.innerHTML = html;
    }
    
    searchResults.style.display = 'block';
}

// File upload functionality
function initializeFileUpload() {
    const fileInput = document.getElementById('resumeUpload');
    const uploadBtn = document.getElementById('uploadBtn');
    const uploadStatus = document.getElementById('uploadStatus');
    
    if (!fileInput) return;
    
    uploadBtn?.addEventListener('click', function() {
        const formData = new FormData();
        const file = fileInput.files[0];
        
        if (!file) {
            showUploadStatus('Please select a file first', 'error');
            return;
        }
        
        formData.append('resume', file);
        
        fetch('/upload-resume', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showUploadStatus(data.success, 'success');
            } else {
                showUploadStatus(data.error, 'error');
            }
        })
        .catch(error => {
            showUploadStatus('Upload failed. Please try again.', 'error');
        });
    });
}

function showUploadStatus(message, type) {
    const uploadStatus = document.getElementById('uploadStatus');
    if (!uploadStatus) return;
    
    uploadStatus.className = `alert alert-${type === 'success' ? 'success' : 'danger'}`;
    uploadStatus.textContent = message;
    uploadStatus.style.display = 'block';
    
    setTimeout(() => {
        uploadStatus.style.display = 'none';
    }, 5000);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeSearch();
    initializeFileUpload();
});