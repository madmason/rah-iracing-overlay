document.addEventListener("DOMContentLoaded", function() {
    // Establish socket connection
    var socket = io();

    const canvas = document.getElementById("telemetry-graph");
    const ctx = canvas.getContext("2d");

    const steeringWheelImage = document.getElementById("steering-wheel");

    let throttleData = [];
    let brakeData = [];
    let clutchData = [];

    // Listen for telemetry updates
    socket.on('telemetry_update', function(data) {
        document.getElementById('gear-display').innerText = data.gear;
        document.getElementById('speed-display').innerText = `${data.speed.toFixed(0)} kph`;
        
        // Update throttle, brake, clutch bar fill heights
        document.getElementById('brake-fill').style.height = `${data.brake * 100}%`;
        document.getElementById('throttle-fill').style.height = `${data.throttle * 100}%`;
        document.getElementById('clutch-fill').style.height = `${data.clutch * 100}%`;
        
        // Update steering wheel rotation based on angle (reverse direction and convert to degrees)
        let steeringAngleRadians = data.steering_wheel_angle;
        let steeringAngleDegrees = -steeringAngleRadians * (180 / Math.PI); // Convert and reverse
        steeringWheelImage.style.transform = `rotate(${steeringAngleDegrees}deg)`;

        // Update data arrays for graph
        throttleData.push(data.throttle * 100);
        brakeData.push(data.brake * 100);
        clutchData.push(data.clutch * 100);

        if (throttleData.length > canvas.width) {
            throttleData.shift();
            brakeData.shift();
            clutchData.shift();
        }

        drawGraph();
    });

    function drawGraph() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Set line width for wider lines
        ctx.lineWidth = 3;

        // Draw throttle (green)
        ctx.strokeStyle = "green";
        ctx.beginPath();
        throttleData.forEach((value, index) => {
            ctx.lineTo(index, canvas.height - value);
        });
        ctx.stroke();

        // Draw brake (red)
        ctx.strokeStyle = "red";
        ctx.beginPath();
        brakeData.forEach((value, index) => {
            ctx.lineTo(index, canvas.height - value);
        });
        ctx.stroke();

        // Draw clutch (blue)
        ctx.strokeStyle = "blue";
        ctx.beginPath();
        clutchData.forEach((value, index) => {
            ctx.lineTo(index, canvas.height - value);
        });
        ctx.stroke();
    }
});
