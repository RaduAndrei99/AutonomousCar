var socket = io();
document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById('form');
    var input = document.getElementById('input');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            if (input.value) {
                socket.emit('chat message', input.value);
                input.value = '';
            }
        });
    }
});

function moveForwardPressed() {
    console.log("go forward");
    socket.emit('commands', "w:pressed")
}

function moveForwardReleased() {
    console.log("stop forward");
    socket.emit('commands', "w:released")
}

function moveBackwardPressed() {
    console.log("go backward");
    socket.emit('commands', "s:pressed")
}

function moveBackwardReleased() {
    console.log("stop backward");
    socket.emit('commands', "s:released")
}

function moveToTheLeftPressed() {
    console.log("go left");
    socket.emit('commands', "a:pressed")
}

function moveToTheLeftReleased() {
    console.log("stop left");
    socket.emit('commands', "a:released")
}
function moveToTheRightPressed() {
    console.log("go right");
    socket.emit('commands', "d:pressed")
}

function moveToTheRightReleased() {
    console.log("stop right");
    socket.emit('commands', "d:released")
}