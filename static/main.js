// voice_call_app/static/main.js

const socket = io.connect('http://localhost:8000/ws/call/', { transports: ['websocket', 'polling', 'flashsocket'] ,cors: {
    origin: "http://localhost:8000",
    methods: ["GET", "POST"]
  }});

function makeCall() {
    const recipient = document.getElementById('recipient').value;

    socket.send(JSON.stringify({
        type: 'call',
        recipient: recipient
    }));
}

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);

    if (data.type === 'call_notification') {
        const callNotification = document.getElementById('call-notification');
        callNotification.innerText = `Incoming call from ${data.caller}`;
        callNotification.classList.remove('hidden');
    } else if (data.type === 'call_acceptance') {
        alert(`${data.recipient} accepted the call.`);
    } else if (data.type === 'call_rejection') {
        alert(`${data.recipient} rejected the call.`);
    }
};
