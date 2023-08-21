let aiSocket;
let webSocket;
let videoElement = document.getElementById('videoElement');

// AI Server
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
            } //else {
            //     videoElement.src = "{% url 'live_feed' %}";
            // }
        } catch(err) {
            console.error("Received invalid data:", event.data);
        }
    };

    aiSocket.onclose = function(event) {
        console.error('AI Socket closed unexpectedly. Reconnecting...');
        setTimeout(connectAI, 1000);
    };
};

// Web Server
const connectWeb = () => {
    webSocket = new WebSocket('ws://127.0.0.1:8000/WEBserver_ws/');

    // 웹 서버(브라우저)로부터 메시지를 받았을 때
    webSocket.onmessage = function(event) {
        // 수신된 메시지를 JSON으로 파싱
        let data = JSON.parse(event.data);

        // 데이터에 'alert' 프로퍼티가 있고, true면 알림창을 표시
        if (data.hasOwnProperty('alert') && data.alert === true) {
            showNotification(data.message);
        }
        // 데이터에 'frame' 프로퍼티가 있으면, 그 값으로 비디오 요소의 소스를 설정 -> 영상 송출
        else if (data.hasOwnProperty('frame')) {
            let frameData = "data:image/jpeg;base64," + data['frame'];
            videoElement.src = frameData;
        }
    };

    // 웹소켓 연결이 비정상적으로 종료되었을 때의 이벤트 핸들러
    webSocket.onclose = function(event) {
        // 연결이 종료되면 콘솔에 에러 메시지를 출력하고,
        console.error('Web Socket closed unexpectedly. Reconnecting...');
        // 1초 후에 웹 서버와의 웹소켓 연결을 재시도
        setTimeout(connectWeb, 1000);
    };
};

// 알림창 관련
function showNotification(message) { // 알림창 생성 및 표시
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.innerHTML = `
        ${message}
        <button onclick="closeNotification(this)">확인</button>
    `;
    document.body.appendChild(notification);
}


function closeNotification(buttonElement) { // 확인버튼 누를 경우 : 창 종료
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
// connectAI();
// connectWeb();


// 비디오 스트리밍
let localVideo = document.getElementById('localVideo');
let localStream; // 로컬 비디오 스트림
let peerConnection; // WebRTC 연결을 관리하는 객체
let websocket; // 서버와 시그널링을 위한 웹소켓

// STUN 서버 설정 (Google의 STUN 서버 사용)
const configuration = { iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] };

// 비디오 스트리밍을 시작하는 함수
async function startStreaming() {
    try {
        // 웹캠에서 비디오 스트림을 가져옴
        localStream = await navigator.mediaDevices.getUserMedia({ video: true });
        localVideo.srcObject = localStream;

        // 웹소켓을 초기화 -> 시그널링 준비
        initWebSocket();

        // WebRTC 연결을 설정
        peerConnection = new RTCPeerConnection(configuration);

        // 로컬 스트림의 모든 트랙을 peerConnection에 추가
        localStream.getTracks().forEach(track => {
            peerConnection.addTrack(track, localStream);
        });

        // offer를 생성
        const offer = await peerConnection.createOffer();
        await peerConnection.setLocalDescription(new RTCSessionDescription(offer));

        // 생성된 offer를 웹소켓을 통해 서버에 전송
        websocket.send(JSON.stringify({ 'offer': offer }));

    } catch (error) {
        // 카메라 접근 중 오류 발생 시 출력
        console.error('카메라 접근 중 오류 발생', error);
    }
}

// 웹소켓 초기화 함수
function initWebSocket() {
    websocket = new WebSocket('ws://127.0.0.1:8000/VideoStreaming_ws/');

    // 서버로부터 메시지가 도착할 경우 처리하는 이벤트 리스너
    websocket.onmessage = function(event) {
        let msg = JSON.parse(event.data);

        // offer, answer, iceCandidate에 따라 각각 처리
        if (msg.offer) {
            handleOffer(msg.offer);
        } else if (msg.answer) {
            handleAnswer(msg.answer);
         }// else if (msg.iceCandidate) {
    //         handleICECandidate(msg.iceCandidate);
    //     }
     };
}

// offer를 처리하는 함수
function handleOffer(offer) {
    peerConnection.setRemoteDescription(new RTCSessionDescription(offer));
}

// answer를 처리하는 함수
function handleAnswer(answer) {
    peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
}

// // ICE 후보군을 처리하는 함수
// function handleICECandidate(iceCandidate) {
//     peerConnection.addIceCandidate(new RTCIceCandidate(iceCandidate));
// }

// 저장된 비디오 불러옴
document.getElementById('videoFile').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const objectURL = URL.createObjectURL(file);
        localVideo.src = objectURL;
        localVideo.play();
    }
});
