// WebSocket 연결 시작
// client
const socket = new WebSocket('ws://127.0.0.1:8000/alerts/');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.message === "Anomaly detected!") {
        alert("Anomaly detected! Please check the CCTV.");
    }
};

socket.onclose = function(event) {
    console.error('WebSocket closed', event);
};

// 알림창
function getNotification() {
    fetch('/notify/')
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            showNotification(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.innerHTML = `
        ${message}
        <button onclick="closeNotification(this)">확인</button>
    `;
    document.body.appendChild(notification);
}

function closeNotification(buttonElement) {
    const notification = buttonElement.parentElement;
    document.body.removeChild(notification);
}