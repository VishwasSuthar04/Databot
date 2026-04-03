// Global variable
let fileUploaded = false;

// Show file name when selected
function showFileName() {
    const fileInput = document.getElementById('fileInput');
    const fileName = document.getElementById('fileName');
    if (fileInput.files[0]) {
        fileName.textContent = '✅ ' + fileInput.files[0].name;
    }
}

// File Upload Function
async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    // File check
    if (!file) {
        alert('Please select a file first!');
        return;
    }

    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('summaryContent').textContent = '';

    // FormData
    const formData = new FormData();
    formData.append('file', file);

    try {
        // Send file to Flask
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // Hide loading
        document.getElementById('loading').style.display = 'none';

        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }

        // Show summary
        document.getElementById('summaryContent').textContent = data.summary;
        fileUploaded = true;

        // Chat message
        addMessage('bot', '✅ File uploaded successfully! You can now ask me anything about your data.');

    } catch (error) {
        document.getElementById('loading').style.display = 'none';
        alert('Something went wrong: ' + error.message);
    }
}

// Send Message Function
async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();

    // Checks
    if (!message) {
        alert('Please type a message first!');
        return;
    }

    if (!fileUploaded) {
        addMessage('bot', '⚠️ Please upload a file first before asking questions!');
        return;
    }

    // Show user message
    addMessage('user', message);
    userInput.value = '';

    // Show thinking
    const thinkingId = addMessage('bot', '⏳ Thinking...');

    try {
        // Send to Flask
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        // Remove thinking
        removeMessage(thinkingId);

        if (data.error) {
            addMessage('bot', '❌ Error: ' + data.error);
            return;
        }

        // Show AI response
        addMessage('bot', data.response);

    } catch (error) {
        removeMessage(thinkingId);
        addMessage('bot', '❌ Something went wrong: ' + error.message);
    }
}

// Add Message Function
function addMessage(type, text) {
    const chatBox = document.getElementById('chatBox');
    const msgDiv = document.createElement('div');
    const msgId = 'msg_' + Date.now();

    msgDiv.id = msgId;
    msgDiv.className = type === 'user' ? 'user-message' : 'bot-message';
    msgDiv.textContent = text;

    chatBox.appendChild(msgDiv);

    // Scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;

    return msgId;
}

// Remove Message Function
function removeMessage(msgId) {
    const msg = document.getElementById(msgId);
    if (msg) msg.remove();
}

// Handle Enter Key
function handleEnter(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}