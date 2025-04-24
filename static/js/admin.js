// Example: Show a message on certificate hover
document.querySelectorAll('.certificate-row').forEach(row => {
    row.addEventListener('mouseenter', () => {
        row.style.backgroundColor = '#f0f8ff';
    });

    row.addEventListener('mouseleave', () => {
        row.style.backgroundColor = '';
    });
});
