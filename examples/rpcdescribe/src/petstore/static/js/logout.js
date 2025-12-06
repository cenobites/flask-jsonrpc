document.addEventListener('DOMContentLoaded', () => {
    const logoutForm = document.getElementById('logoutForm');
    const errorMessage = document.getElementById('errorMessage');
    const logoutButton = document.getElementById('logoutButton');
    const buttonText = logoutButton.querySelector('.button-text');
    const buttonSpinner = logoutButton.querySelector('.button-spinner');

    logoutForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Clear previous errors
        errorMessage.style.display = 'none';
        errorMessage.textContent = '';

        // Disable button and show spinner
        logoutButton.disabled = true;
        buttonText.style.display = 'none';
        buttonSpinner.style.display = 'inline-block';

        try {
            // Get the access token
            const accessToken = localStorage.getItem('jwt');

            const response = await fetch('/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                }
            });

            if (response.ok) {
                // Redirect to login page
                window.location.href = '/api/browse/login';
            } else {
                const data = await response.json();
                errorMessage.textContent = data.msg || 'Failed to logout. Please try again.';
                errorMessage.style.display = 'block';
            }
        } catch (error) {
            errorMessage.textContent = 'An error occurred. Please try again.';
            errorMessage.style.display = 'block';
            console.error('Logout error:', error);
        } finally {
            // Clear the JWT token
            localStorage.removeItem('jwt');

            // Re-enable button and hide spinner
            logoutButton.disabled = false;
            buttonText.style.display = 'inline';
            buttonSpinner.style.display = 'none';
        }
    });
});
