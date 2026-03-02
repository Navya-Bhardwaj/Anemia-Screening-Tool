// Handle file input change to show selected file name
document.getElementById('file-input').addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const label = document.querySelector('.upload-label span');
        label.textContent = `Selected: ${file.name}`;
    }
});

// Add loading animation on form submit
document.getElementById('upload-form').addEventListener('submit', function() {
    const btn = document.querySelector('.btn');
    btn.textContent = 'Analyzing...';
    btn.disabled = true;
    btn.style.background = '#ccc';
});
