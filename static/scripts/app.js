let mediaRecorder;
let audioChunks = [];
let audioBlob;

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };
            mediaRecorder.onstop = () => {
                audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                audioChunks = [];
                sendAudio();
            };
            mediaRecorder.start();
            setTimeout(() => mediaRecorder.stop(), 5000); // Record for 5 seconds
        });
}

function sendAudio() {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'audio.wav');

    fetch('/speech-to-text', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        sendText(data.text);
    });
}

function sendText(text) {
    fetch('/chatgpt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
    })
    .then(response => response.json())
    .then(data => {
        const audio = document.getElementById('audio');
        audio.src = '/audio';
        audio.style.display = 'block';
    });
}
