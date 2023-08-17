// WebSocket 연결 시작
// client
document.addEventListener("DOMContentLoaded", function() {

const socket = new WebSocket('ws://127.0.0.1:8000/alerts/');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.message === "Anomaly detected!") {
        showNotification("Anomaly detected! Please check the CCTV.");
    }
};
});

socket.onclose = function(event) {
    console.error('WebSocket closed', event);
};


// 알림창 생성 및 표시
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.innerHTML = `
        ${message}
        <button onclick="closeNotification(this)">확인</button>
    `;
    document.body.appendChild(notification);
}

// 확인버튼 누를 경우 : 창 종료
function closeNotification(buttonElement) {
    const notification = buttonElement.parentElement;
    document.body.removeChild(notification);
}


// 현재 시간 표시
function updateCurrentTime() {
    const timeElement = document.getElementById("time");
    const currentTime = new Date();
    const formattedTime = currentTime.toLocaleTimeString('ko-KR');
    timeElement.textContent = formattedTime;
}

// 1초마다 시간 업데이트
setInterval(updateCurrentTime, 1000);

// // 서버에 알림 정보 요청, 반환 메시지로 알림창 표시 -> 웹소켓 방식 우선 사용
// function getNotification() {
//     fetch('/notify/')
//     .then(response => response.json())
//     .then(data => {
//         if (data.message) {
//             showNotification(data.message);
//         }
//     })
//     .catch(error => console.error('Error:', error));
// }