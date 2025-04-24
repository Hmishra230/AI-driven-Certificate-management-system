// Example: Toggle profile edit section
const editButton = document.querySelector('#edit-profile');
if (editButton) {
    editButton.addEventListener('click', () => {
        const editForm = document.querySelector('.profile-edit-form');
        editForm.style.display = editForm.style.display === 'none' ? 'block' : 'none';
    });
}
