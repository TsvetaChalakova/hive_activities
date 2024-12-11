// document.addEventListener('DOMContentLoaded', function() {
//     const modal = document.getElementById('newActivityModal');
//     const form = document.getElementById('createActivityForm');
//     const submitBtn = document.getElementById('submitActivity');
//     const errorDiv = document.getElementById('modalFormErrors');
//
//     modal.addEventListener('hidden.bs.modal', function () {
//         form.reset();
//         errorDiv.style.display = 'none';
//         errorDiv.innerHTML = '';
//     });
//
//     submitBtn.addEventListener('click', function() {
//         const formData = new FormData(form);
//
//         fetch(form.action, {
//             method: 'POST',
//             body: formData,
//             headers: {
//                 'X-Requested-With': 'XMLHttpRequest'
//             },
//             credentials: 'same-origin'
//         })
//             .then(response => response.json())
//             .then(data => {
//                 if (data.status === 'success') {
//
//                     const modalInstance = bootstrap.Modal.getInstance(modal);
//                     modalInstance.hide();
//
//
//                     const toast = new bootstrap.Toast(document.createElement('div'));
//                     toast.innerText = data.message;
//                     document.body.appendChild(toast._element);
//                     toast.show();
//
//
//                     window.location.reload();
//                 } else {
//
//                     errorDiv.style.display = 'block';
//                     errorDiv.innerHTML = Object.entries(data.errors)
//                         .map(([field, errors]) => `<p>${field}: ${errors.join(', ')}</p>`)
//                         .join('');
//                 }
//             })
//             .catch(error => {
//                 console.error('Error:', error);
//                 errorDiv.style.display = 'block';
//                 errorDiv.innerHTML = '<p>An error occurred. Please try again.</p>';
//             });
//     });
// });
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
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken,
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => Promise.reject(data));
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {

                const modalInstance = bootstrap.Modal.getInstance(modal);
                modalInstance.hide();

                const toastDiv = document.createElement('div');
                toastDiv.className = 'toast align-items-center text-bg-success';
                toastDiv.setAttribute('role', 'alert');
                toastDiv.innerHTML = `
                    <div class="d-flex">
                        <div class="toast-body">
                            ${data.message}
                        </div>
                        <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast"></button>
                    </div>
                `;
                document.body.appendChild(toastDiv);
                const toast = new bootstrap.Toast(toastDiv);
                toast.show();

                if (data.redirect_url) {
                    window.location.href = data.redirect_url;
                } else {
                    window.location.reload();
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            errorDiv.style.display = 'block';
            if (error.errors) {
                errorDiv.innerHTML = Object.entries(error.errors)
                    .map(([field, errors]) => `<p>${field}: ${errors.join(', ')}</p>`)
                    .join('');
            } else {
                errorDiv.innerHTML = '<p>An error occurred. Please try again.</p>';
            }
        });
    });
});