document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Get form data
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // Check if passwords match
    if (password !== confirmPassword) {
        alert('Passwords do not match');
        return;
    }

    // Prepare data for API request
    const data = {
        username: email,
        password_hash: password,
        role: 'user' // Assuming default role is 'user'
    };

    // Make API call
    fetch('http://127.0.0.1:5000/api/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Handle successful registration response
        console.log('Registration successful:', data);
        alert('Registration successful');
        window.location.href = 'login.html'; // Change 'login.html' to the desired page URL
        // Optionally, redirect to login page or display a success message
    })
    .catch(error => {
        // Handle errors
        console.error('There was a problem with the registration:', error);
        alert('There was a problem with the registration');
        // Optionally, display an error message to the user
    });
});
