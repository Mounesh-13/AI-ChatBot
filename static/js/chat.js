document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatLog = document.getElementById('chat-log');
    const clearButton = document.getElementById('clear-button');

    // Function to add a message to the chat log
    function addMessage(message, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
        
        // Simple markdown to HTML conversion for basic formatting
        let formattedMessage = message
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
            .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italic
            .replace(/`([^`]+)`/g, '<code>$1</code>') // Inline code
            .replace(/\n/g, '<br>'); // Line breaks
            
        messageDiv.innerHTML = formattedMessage;
        chatLog.appendChild(messageDiv);
        
        // Scroll to bottom of chat
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    // Function to handle form submission
    async function handleSubmit(e) {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage(message, true);
        userInput.value = '';
        
        try {
            // Show loading indicator
            const loadingIndicator = document.createElement('div');
            loadingIndicator.id = 'loading';
            loadingIndicator.className = 'message bot-message';
            loadingIndicator.textContent = 'AI is thinking...';
            chatLog.appendChild(loadingIndicator);
            chatLog.scrollTop = chatLog.scrollHeight;
            
            // Send message to backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });
            
            // Remove loading indicator
            chatLog.removeChild(loadingIndicator);
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Add bot response to chat
            addMessage(data.response, false);
            
        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, there was an error processing your request. Please try again.', false);
        }
    }

    // Handle clear chat
    if (clearButton) {
        clearButton.addEventListener('click', () => {
            chatLog.innerHTML = '';
            // Clear loading indicator if present
            const loading = document.getElementById('loading');
            if (loading) {
                loading.remove();
            }
        });
    }

    // Event listeners
    chatForm.addEventListener('submit', handleSubmit);
    
    // Allow Shift+Enter for new lines, Enter to send
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    });
    
    // Focus the input field on page load
    userInput.focus();
});
