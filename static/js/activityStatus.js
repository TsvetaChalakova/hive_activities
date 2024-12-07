document.addEventListener('DOMContentLoaded', function () {
    const statusColors = {
        'TO_DO': 'lightblue',
        'IN_PROGRESS': 'lightgreen',
        'COMPLETED': 'lightgray'
    };

    function updateCardStatus(card, newStatus, displayStatus) {
        card.dataset.status = newStatus;
        card.style.backgroundColor = statusColors[newStatus];
        const statusElement = card.querySelector('.activity-status');
        if (statusElement) {
            statusElement.textContent = displayStatus;
        }
    }

    function getCsrfToken() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        return token ? token.value : '';
    }

    document.querySelectorAll('.activity-card').forEach(card => {
        card.addEventListener('click', async function() {
            try {
                const response = await fetch(`/activities/update-activity-status/${this.dataset.id}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                        'Content-Type': 'application/json'
                    }
                });

                const data = await response.json();

                if (data.success) {
                    updateCardStatus(this, data.new_status, data.display_status);
                } else {
                    console.error('Error:', data.error);
                    alert('Failed to update status: ' + data.error);
                }
            } catch (error) {
                console.error('Error updating status:', error);
                alert('Failed to update status. Please try again.');
            }
        });
    });
});