document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('addNoteModal');
    const form = document.getElementById('createNoteForm');
    const submitBtn = document.getElementById('submitNote');

    submitBtn.addEventListener('click', function() {
        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const modalInstance = bootstrap.Modal.getInstance(modal);
                    modalInstance.hide();
                    window.location.reload();
                } else {
                    alert('Error saving note: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
    });
});