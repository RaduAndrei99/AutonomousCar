
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
	res.sendFile("./public/images/favicon.ico");
});


app.get('/home', (req, res) => {
	res.render('home', {
		title: "Home",

	})
});

var childPython = null
io.on('connection', (socket) => {
	console.log('A user connected');

	socket.on('commands', (msg) => {
		var command = msg.split(':')
		console.log('key: ' + command[0] + '=> command: ' + command[1]);
		if (command[0] == "start") {
			childPython = child_process.spawn('python3', ['./PythonCode/functions.py']);
			childPython.stdin.setEncoding('utf-8');

			childPython.stdout.on('data', function (data) {
				console.log(`stdout:${data}`);
				//dataToSend = data.toString();
			});

			childPython.stderr.on('data', function (data) {
				console.log(`stderr:${data}`);
				//dataToSend += data.toString();
			});

			childPython.on('close', (code) => {
				console.log(`child process close all stdio with code ${code}`);
				//console.log(data);
			});
			console.log(command[1].length)
		}
		console.log(command[1] == "pressed" && childPython != null)
		if (command[1] == "pressed" && childPython != null) {

			if (command[0] == "w") {
				childPython.stdin.write("w:pressed\n");
			}
			else if (command[0] == "a") {
				childPython.stdin.write("a:pressed\n");
			} else if (command[0] == "s") {
				childPython.stdin.write("s:pressed\n");
			} else if (command[0] == "d") {
				childPython.stdin.write("d:pressed\n");
			}
		}
		else if (command[1] == "released" && childPython != null) {

			if (command[0] == "w") {
				childPython.stdin.write("w:released\n")
			} else if (command[0] == "a") {
				childPython.stdin.write("a:released\n");
			} else if (command[0] == "s") {
				childPython.stdin.write("a:released\n");
			} else if (command[0] == "d") {
				childPython.stdin.write("a:released\n");
			}
		}

	});
	socket.on('disconnect', () => {
		console.log('user disconnected');
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


server.listen(port, () => console.log(`Serverul rulează la adresa http://localhost:1235/home`));
