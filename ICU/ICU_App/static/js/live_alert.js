let aiSocket;
let webSocket;
let videoElement = document.getElementById('videoElement');

const connectAI = () => {
    aiSocket = new WebSocket('ws://127.0.0.1:8000/AIserver_ws/');
    
    aiSocket.onmessage = function(event) {
        try {
            const data = JSON.parse(event.data);
            if (data.message === "Anomaly detected!") {
                showNotification("Anomaly detected! Please check the CCTV.");
            }
            if (data['alert'] === true) {
                videoElement.src = data['alert_stream'];
            } else {
                videoElement.src = "{% url 'live_feed' %}";
            }
        } catch(err) {
            console.error("Received invalid data:", event.data);
        }
    };
    
    aiSocket.onclose = function(event) {
        console.error('AI Socket closed unexpectedly. Reconnecting...');
        setTimeout(connectAI, 1000);
    };
};

const connectWeb = () => {
    webSocket = new WebSocket('ws://127.0.0.1:8000/WEBserver_ws/');

    webSocket.onmessage = function(event) {
        let data = JSON.parse(event.data);
        if (data.hasOwnProperty('stream')) {
        videoElement.src = data['stream'];
    }
    };

    webSocket.onclose = function(event) {
        console.error('Web Socket closed unexpectedly. Reconnecting...');
        setTimeout(connectWeb, 1000);
    };
};

const connectBrowser = () => {
    let browserSocket = new WebSocket('ws://127.0.0.1:8000/BROWSERserver_ws/');

    browserSocket.onmessage = function(event) {
        let frameData = event.data;
        let blob = new Blob([frameData], { type: 'image/jpeg' });
        let imageUrl = URL.createObjectURL(blob);
        videoElement.src = imageUrl;
    };

    browserSocket.onclose = function(event) {
        console.error('Browser Socket closed unexpectedly. Reconnecting...');
        setTimeout(connectBrowser, 1000);
    };
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

// 초기 연결 시도
connectAI();
connectWeb();
connectBrowser();

