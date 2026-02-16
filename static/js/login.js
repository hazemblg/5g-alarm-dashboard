// Login form handler
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('errorMessage');
    const loginBtn = document.querySelector('.btn-primary');
    const loginText = document.getElementById('loginText');
    const loginLoader = document.getElementById('loginLoader');

    // Show loader
    loginText.classList.add('hidden');
    loginLoader.classList.remove('hidden');
    loginBtn.disabled = true;
    errorDiv.classList.add('hidden');

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Success - redirect to Streamlit dashboard with token
            window.location.href = data.redirect_url;
        } else {
            // Show error
            errorDiv.textContent = data.message || 'Invalid credentials';
            errorDiv.classList.remove('hidden');
        }
    } catch (error) {
        errorDiv.textContent = 'Connection error. Please try again.';
        errorDiv.classList.remove('hidden');
    } finally {
        // Hide loader
        loginText.classList.remove('hidden');
        loginLoader.classList.add('hidden');
        loginBtn.disabled = false;
    }
});

// Clear error on input change
document.getElementById('username').addEventListener('input', () => {
    document.getElementById('errorMessage').classList.add('hidden');
});

document.getElementById('password').addEventListener('input', () => {
    document.getElementById('errorMessage').classList.add('hidden');
});
