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
    setInterval(updateImage, 750);
    var textarea = document.getElementById('log');
    textarea.readOnly = true;

    setTimeout(function () {
        var textArea = document.getElementById('log');
        textArea.scrollTop = textArea.scrollHeight;
    }, 100);

    var checkbox = document.querySelector("input[id='daytimeLights']");
    checkbox.addEventListener('change', function () {
        if (this.checked) {
            socket.emit('lights', "daytimeLights:on\n")
        } else {
            socket.emit('lights', "daytimeLights:off\n")
        }
    });

    var checkbox = document.querySelector("input[id='brakeLights']");
    checkbox.addEventListener('change', function () {
        if (this.checked) {
            socket.emit('lights', "brakeLights:on\n")
        } else {
            socket.emit('lights', "brakeLights:off\n")
        }
    });

    var checkbox = document.querySelector("input[id='leftSignal']");
    checkbox.addEventListener('change', function () {
        if (this.checked) {
            socket.emit('lights', "leftSignal:on\n")
        } else {
            socket.emit('lights', "leftSignal:off\n")
        }
    });

    var checkbox = document.querySelector("input[id='rightSignal']");
    checkbox.addEventListener('change', function () {
        if (this.checked) {
            socket.emit('lights', "rightSignal:on\n")
        } else {
            socket.emit('lights', "rightSignal:off\n")
        }
    });


});

socket.on('message', function (data) {
    document.getElementById("log").append(data + "\n")
});

function start() {
    console.log("start");
    socket.emit('commands', "start:start")
}
function stop() {
    console.log("stop");
    socket.emit('commands', "stop:stop")
    socket.emit('lights', "esc")
}
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

function updateImage() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('video-image').src = "SavedImage/image.jpg?" + new Date().getTime();
        }
    };

    xhttp.open("GET", "/live-feed", true);
    xhttp.send();
}
