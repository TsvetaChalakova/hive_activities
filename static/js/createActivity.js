document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('newActivityModal');
    const form = document.getElementById('createActivityForm');
    const submitBtn = document.getElementById('submitActivity');
    const errorDiv = document.getElementById('modalFormErrors');

    modal.addEventListener('hidden.bs.modal', function () {
        form.reset();
        errorDiv.style.display = 'none';
        errorDiv.innerHTML = '';
    });

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


                    const toast = new bootstrap.Toast(document.createElement('div'));
                    toast.innerText = data.message;
                    document.body.appendChild(toast._element);
                    toast.show();


                    window.location.reload();
                } else {

                    errorDiv.style.display = 'block';
                    errorDiv.innerHTML = Object.entries(data.errors)
                        .map(([field, errors]) => `<p>${field}: ${errors.join(', ')}</p>`)
                        .join('');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                errorDiv.style.display = 'block';
                errorDiv.innerHTML = '<p>An error occurred. Please try again.</p>';
            });
    });
});