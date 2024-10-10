const socket = io();

socket.on('speed_update', (data) => {
    document.getElementById('speed').innerText = Math.round(data.speed);
});
