document.addEventListener('DOMContentLoaded', () => {
    const cancelButtons = document.querySelectorAll('.cancel-bet-btn');

    cancelButtons.forEach(cancelButton => {
        cancelButton.addEventListener('click', async () => {
            const betId = cancelButton.getAttribute('data-bet-id');

            if (!confirm('Are you sure you want to cancel this bet?')) {
                return;
            }

            try {
                const response = await fetch(`/bets/${betId}/cancel/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken(),
                        'Content-Type': 'application/json',
                    }
                });

                const data = await response.json();

                if (response.ok) {
                    alert(data.message);
                    location.reload();
                } else {
                    alert(data.error);
                }
        })
});

function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') return value;
    }
    return '';
}