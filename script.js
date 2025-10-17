// In-memory storage for certificates
let certificates = [];
let currentCertId = 1;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeUploadForm();
    initializeProfileForm();
    initializeModal();
    initializeSearch();
    loadSampleData();
    updateDashboard();
});

// Navigation between pages
function initializeNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const pages = document.querySelectorAll('.page');

    navButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetPage = this.getAttribute('data-page');
            
            // Update active nav button
            navButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Update active page
            pages.forEach(p => p.classList.remove('active'));
            document.getElementById(targetPage).classList.add('active');
        });
    });
}

// Upload form handling
function initializeUploadForm() {
    const form = document.getElementById('uploadForm');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const name = document.getElementById('certName').value;
        const category = document.getElementById('certCategory').value;
        const issuer = document.getElementById('certIssuer').value;
        const date = document.getElementById('certDate').value;
        const description = document.getElementById('certDescription').value;
        const file = document.getElementById('certFile').files[0];
        
        if (file && file.size > 5 * 1024 * 1024) {
            alert('File size must be less than 5MB');
            return;
        }
        
        // Create certificate object
        const certificate = {
            id: currentCertId++,
            name,
            category,
            issuer,
            date,
            description,
            uploadDate: new Date().toISOString(),
            fileName: file ? file.name : 'certificate.pdf'
        };
        
        // If there's a file, read it
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                certificate.fileData = e.target.result;
                addCertificate(certificate);
            };
            reader.readAsDataURL(file);
        } else {
            addCertificate(certificate);
        }
    });
}

// Add certificate to storage
function addCertificate(certificate) {
    certificates.push(certificate);
    updateDashboard();
    
    // Reset form and show success message
    document.getElementById('uploadForm').reset();
    alert('Certificate uploaded successfully!');
    
    // Navigate to dashboard
    document.querySelector('[data-page="dashboard"]').click();
}

// Update dashboard with certificates
function updateDashboard() {
    updateStats();
    renderCertificates(certificates);
}

// Update statistics
function updateStats() {
    document.getElementById('totalCerts').textContent = certificates.length;
    
    // Calculate certificates added this month
    const now = new Date();
    const thisMonth = certificates.filter(cert => {
        const certDate = new Date(cert.uploadDate);
        return certDate.getMonth() === now.getMonth() && 
               certDate.getFullYear() === now.getFullYear();
    }).length;
    document.getElementById('recentCerts').textContent = thisMonth;
    
    // Calculate unique categories
    const uniqueCategories = new Set(certificates.map(cert => cert.category));
    document.getElementById('categories').textContent = uniqueCategories.size;
}

// Render certificates in grid
function renderCertificates(certs) {
    const container = document.getElementById('certificateList');
    
    if (certs.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
                    <rect x="10" y="20" width="60" height="40" rx="4" stroke="#CBD5E1" stroke-width="2"/>
                    <line x1="20" y1="35" x2="60" y2="35" stroke="#CBD5E1" stroke-width="2"/>
                    <line x1="20" y1="45" x2="50" y2="45" stroke="#CBD5E1" stroke-width="2"/>
                </svg>
                <p>No certificates yet. Upload your first certificate to get started!</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = certs.map(cert => `
        <div class="certificate-card" onclick="openCertificateModal(${cert.id})">
            <div class="cert-header">
                <span class="cert-category">${cert.category}</span>
                <div class="cert-actions" onclick="event.stopPropagation()">
                    <button onclick="downloadCertificate(${cert.id})" title="Download">
                        ⬇️
                    </button>
                    <button onclick="deleteCertificate(${cert.id})" title="Delete">
                        🗑️
                    </button>
                </div>
            </div>
            <div class="cert-body">
                <h3>${cert.name}</h3>
                <div class="cert-info">
                    <span>📋 Issued by: ${cert.issuer}</span>
                    <span>📅 Date: ${formatDate(cert.date)}</span>
                    <span>⬆️ Uploaded: ${formatDate(cert.uploadDate)}</span>
                </div>
            </div>
        </div>
    `).join('');
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

// Modal handling
function initializeModal() {
    const modal = document.getElementById('certModal');
    const span = document.getElementsByClassName('close')[0];
    
    span.onclick = function() {
        modal.style.display = 'none';
    }
    
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
}

// Open certificate details modal
function openCertificateModal(id) {
    const cert = certificates.find(c => c.id === id);
    if (!cert) return;
    
    const modal = document.getElementById('certModal');
    const modalBody = document.getElementById('modalBody');
    
    modalBody.innerHTML = `
        <h3>${cert.name}</h3>
        <p><strong>Category:</strong> ${cert.category}</p>
        <p><strong>Issued By:</strong> ${cert.issuer}</p>
        <p><strong>Issue Date:</strong> ${formatDate(cert.date)}</p>
        <p><strong>Upload Date:</strong> ${formatDate(cert.uploadDate)}</p>
        <p><strong>File Name:</strong> ${cert.fileName}</p>
        ${cert.description ? `<p><strong>Description:</strong> ${cert.description}</p>` : ''}
        <div class="modal-actions">
            <button class="btn-download" onclick="downloadCertificate(${cert.id})">Download</button>
            <button class="btn-delete" onclick="deleteCertificate(${cert.id}); document.getElementById('certModal').style.display='none';">Delete</button>
        </div>
    `;
    
    modal.style.display = 'block';
}

// Download certificate
function downloadCertificate(id) {
    const cert = certificates.find(c => c.id === id);
    if (!cert) return;
    
    if (cert.fileData) {
        const link = document.createElement('a');
        link.href = cert.fileData;
        link.download = cert.fileName;
        link.click();
    } else {
        alert('Certificate file not available for download');
    }
}

// Delete certificate
function deleteCertificate(id) {
    if (confirm('Are you sure you want to delete this certificate?')) {
        certificates = certificates.filter(c => c.id !== id);
        updateDashboard();
    }
}

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    
    searchInput.addEventListener('input', function() {
        const query = this.value.toLowerCase();
        
        if (query === '') {
            renderCertificates(certificates);
        } else {
            const filtered = certificates.filter(cert => 
                cert.name.toLowerCase().includes(query) ||
                cert.category.toLowerCase().includes(query) ||
                cert.issuer.toLowerCase().includes(query)
            );
            renderCertificates(filtered);
        }
    });
}
