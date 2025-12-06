document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('errorMessage');
    const loginButton = document.getElementById('loginButton');
    const buttonText = loginButton.querySelector('.button-text');
    const buttonSpinner = loginButton.querySelector('.button-spinner');

    // Clear previous errors
    errorMessage.style.display = 'none';
    errorMessage.textContent = '';

    // Disable button and show spinner
    loginButton.disabled = true;
    buttonText.style.display = 'none';
    buttonSpinner.style.display = 'inline-block';

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok && data.access_token) {
            // Store the JWT token
            localStorage.setItem('jwt', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);

            // Redirect to dashboard or home
            window.location.href = '/api/browse';
        } else {
            localStorage.removeItem('jwt');
            localStorage.removeItem('refresh_token');

            // Show error message
            errorMessage.textContent = data.msg || 'Invalid username or password';
            errorMessage.style.display = 'block';
        }
    } catch (error) {
        errorMessage.textContent = 'An error occurred. Please try again.';
        errorMessage.style.display = 'block';
        console.error('Login error:', error);
    } finally {
        // Re-enable button and hide spinner
        loginButton.disabled = false;
        buttonText.style.display = 'inline';
        buttonSpinner.style.display = 'none';
    }
});
