document.getElementById('send-button').addEventListener('click', sendMessage);
document.getElementById('close-modal').addEventListener('click', closeModal);
document.getElementById('submit-feedback').addEventListener('click', submitFeedback);
const stars = document.querySelectorAll('.star');
stars.forEach(star => star.addEventListener('click', setRating));

let currentResponse = '';
let currentRating = null;

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    const userEmail = document.getElementById('user-email').value;
    if (!userInput) return;

    // Display user's message
    const messagesDiv = document.getElementById('messages');
    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'user-message';
    userMessageDiv.innerText = userInput;
    messagesDiv.appendChild(userMessageDiv);

    // Clear input field
    document.getElementById('user-input').value = '';

    // Call the chatbot API
    fetch('https://your-api-endpoint.amazonaws.com/prod/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_input: userInput,
            user_id: 'user_123',
            user_email: userEmail
        })
    })
    .then(response => response.json())
    .then(data => {
        const botMessageDiv = document.createElement('div');
        botMessageDiv.className = 'bot-message';
        if (data.response) {
            botMessageDiv.innerText = data.response;
            currentResponse = data.response;
            openModal();
        } else if (data.error) {
            botMessageDiv.innerText = `Error: ${data.error}`;
        }
        messagesDiv.appendChild(botMessageDiv);

        if (userEmail) {
            alert('A copy of this conversation will be sent to your email.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerText = 'An error occurred. Please try again later.';
        messagesDiv.appendChild(errorDiv);
    });
}

function openModal() {
    document.getElementById('feedback-modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('feedback-modal').style.display = 'none';
    resetFeedbackForm();
}

function setRating(event) {
    currentRating = parseInt(event.target.getAttribute('data-value'));
    stars.forEach(star => {
        if (parseInt(star.getAttribute('data-value')) <= currentRating) {
            star.classList.add('selected');
        } else {
            star.classList.remove('selected');
        }
    });
}

function submitFeedback() {
    const feedbackComment = document.getElementById('feedback-comment').value;

    // Send feedback to the chatbot API
    fetch('https://your-api-endpoint.amazonaws.com/prod/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_input: '', // Empty input, only submitting feedback
            user_id: 'user_123',
            feedback_rating: currentRating,
            feedback_comment: feedbackComment
        })
    })
    .then(response => response.json())
    .then(data => {
        // Handle response if needed
    })
    .catch(error => {
        console.error('Error submitting feedback:', error);
    });

    closeModal();
}

function resetFeedbackForm() {
    currentRating = null;
    document.getElementById('feedback-comment').value = '';
    stars.forEach(star => star.classList.remove('selected'));
}
