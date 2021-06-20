
const express = require('express');
const expressLayouts = require('express-ejs-layouts');
const bodyParser = require('body-parser')
const child_process = require('child_process');
const app = express();
var dir = process.cwd();

const port = 1235;
const fs = require('fs');
const { Console } = require('console');
const { mainModule } = require('process');
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);
var net = require('net');

var HOST = '192.168.100.47';
var PORT = 1234;
var clientPi = new net.Socket();

// directorul 'views' va conține fișierele .ejs (html + js executat la server)
app.set('view engine', 'ejs');
// suport pentru layout-uri - implicit fișierul care reprezintă template-ul site-ului este views/layout.ejs
app.use(expressLayouts);
// directorul 'public' va conține toate resursele accesibile direct de către client (e.g., fișiere css, javascript, imagini)
app.use(express.static('public'))
// corpul mesajului poate fi interpretat ca json; datele de la formular se găsesc în format json în req.body
app.use(bodyParser.json());
// utilizarea unui algoritm de deep parsing care suportă obiecte în obiecte
app.use(bodyParser.urlencoded({ extended: true }));





app.get('/favicon.ico', (req, res) => {
	res.sendFile("/home/pi/AutonomousCar/public/images/favicon.ico");
});


app.get('/home', (req, res) => {
	res.render('home', {
		title: "Home",

	})
});

function GetCurrentLogTime() {
	var today = new Date();
	var date = today.getDate() + '-' + (today.getMonth() + 1) + '-' + today.getFullYear();
	var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
	var dateTime = '[' + date + ' ' + time + ']';

	return dateTime
}

var carMovementProcess = null;
var carLightsProcess = null;
io.on('connection', (socket) => {
	console.log('A user connected');
	socket.send(GetCurrentLogTime() + " " + "Connection successfully")
	
	socket.on('lights', (msg) => {
		if (carLightsProcess != null) {
			carLightsProcess.stdin.write(msg);
				socket.send(GetCurrentLogTime() + " " + msg)
		}
		else{
			console.log("lightsProcess doesn't exist");
		}
	});


	socket.on('commands', (msg) => {
		var command = msg.split(':')
		console.log('key: ' + command[0] + '=> command: ' + command[1]);
		if (command[0] == "start") {
			carMovementProcess = child_process.spawn('python3', ['./PythonCode/functions.py']);
			carMovementProcess.stdin.setEncoding('utf-8');


			carMovementProcess.stdout.on('data', function (data) {
				console.log(`stdout:${data}`);
				//dataToSend = data.toString();
			});

			carMovementProcess.stderr.on('data', function (data) {
				console.log(`stderr:${data}`);
				//dataToSend += data.toString();
			});

			carMovementProcess.on('close', (code) => {
				console.log(`movement process close all stdio with code ${code}`);
				//console.log(data);
			});

			carLightsProcess = child_process.spawn('python3', ['./PythonCode/leds.py']);
			carLightsProcess.stdin.setEncoding('utf-8');

			carLightsProcess.stdout.on('data', function (data) {
				console.log(`stdout:${data}`);
				//dataToSend = data.toString();
			});

			carLightsProcess.stderr.on('data', function (data) {
				console.log(`stderr:${data}`);
				//dataToSend += data.toString();
			});

			carLightsProcess.on('close', (code) => {
				console.log(`lights process close all stdio with code ${code}`);
				//console.log(data);
			});

			socket.send(GetCurrentLogTime() + " " + "Python script running...")
		}
		console.log(command[1] == "pressed" && carMovementProcess != null)
		if (command[1] == "pressed" && carMovementProcess != null) {

			if (command[0] == "w") {
				carMovementProcess.stdin.write("w:pressed\n");
				socket.send(GetCurrentLogTime() + " " + "Forward pressed")
			}
			else if (command[0] == "a") {
				carMovementProcess.stdin.write("w:pressed\n");
				carMovementProcess.stdin.write("a:pressed\n");
				socket.send(GetCurrentLogTime() + " " + "Left pressed")
			} else if (command[0] == "s") {
				carMovementProcess.stdin.write("s:pressed\n");
				socket.send(GetCurrentLogTime() + " " + "Back pressed")
			} else if (command[0] == "d") {
				carMovementProcess.stdin.write("w:pressed\n");
				carMovementProcess.stdin.write("d:pressed\n");
				socket.send(GetCurrentLogTime() + " " + "Right pressed")
			}
		}
		else if (command[1] == "released" && carMovementProcess != null) {

			if (command[0] == "w") {
				carMovementProcess.stdin.write("w:released\n")
				socket.send(GetCurrentLogTime() + " " + "Forward released")
			} else if (command[0] == "a") {
				carMovementProcess.stdin.write("a:released\n");
				carMovementProcess.stdin.write("w:released\n");
				socket.send(GetCurrentLogTime() + " " + "Left released")
			} else if (command[0] == "s") {
				carMovementProcess.stdin.write("s:released\n");
				socket.send(GetCurrentLogTime() + " " + "Back released")
			} else if (command[0] == "d") {
				carMovementProcess.stdin.write("w:released\n");
				carMovementProcess.stdin.write("d:released\n");
				socket.send(GetCurrentLogTime() + " " + "Right released")
			}
		}

	});
	socket.on('disconnect', () => {
		console.log('User disconnected');
	});
});



app.get('/live-feed', (req, res) => {

	var cameraPython = child_process.spawn('python3', ['./PythonCode/cameraScript.py']);
	cameraPython.stdout.on('data', function (data) {
		console.log(`stdout:${data}`);

	});

	cameraPython.stderr.on('data', function (data) {
		console.log(`stderr:${data}`);

	});

	cameraPython.on('close', (code) => {
		console.log(`child process close all stdio with code ${code}`);
		res.writeHead(200, { 'Content-Type': 'text/txt' });
		res.end();
	});

});

server.listen(port, () => console.log(`Serverul rulează la adresa http://localhost:${port}/home`));
