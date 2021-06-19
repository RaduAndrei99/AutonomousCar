import { StreamCamera, Codec } from 'pi-camera-connect';
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


// la accesarea din browser adresei http://localhost:6789/ se va returna textul 'Hello World'
// proprietățile obiectului Request - req - https://expressjs.com/en/api.html#req
// proprietățile obiectului Response - res - https://expressjs.com/en/api.html#res
app.get('/favicon.ico', (req, res) => {
	res.sendFile("/home/ix_andrei/Documents/Facultate/AN3SEM2/OnlineCompilerPW/PW-Online-Compiler/public/images/favicon.ico");
	//res.sendFile("/public/images/favicon.ico");
});


app.get('/home', (req, res) => {


	res.render('home', {
		title: "Home",

	})
});


var childPython=null
io.on('connection', (socket) => {
	console.log('A user connected');
	
	socket.on('commands', (msg) => {
		var command = msg.split(':')
		console.log('key: ' + command[0]+'=>command: ' +command[1]);
		if (command[0] == "start") {
			childPython = child_process.spawn('python3', ['functions.py']);// ['-c', 'import functions; functions.prepare()']);
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
		console.log(command[1]=="pressed")
		console.log(command[1]=="pressed" &&childPython != null) 
		if (command[1] == "pressed" && childPython != null) {
			if (command[0] == "w") {
				console.log("dasffffffffffffffffff")
				childPython.stdin.write("w:pressed\n")
				
				/*
				childPython = child_process.spawn('python', ['-c', 'import functions; functions.move_forward(50)']);
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
				});*/
			}
		}
		else if (command[1] == "released" && childPython != null) {
			
			if (command[0] == "w") {
				childPython.stdin.write("w:released\n")
			}
			//childPython.kill();
			/*
			const childPython = child_process.spawn('python', ['-c', 'import functions; functions.stop_motors()']);
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
			*/
		}

	});
	socket.on('disconnect', () => {
		console.log('user disconnected');
	});
});


const runApp = async () => {
	const streamCamera = new StreamCamera({
	  codec: Codec.MJPEG,
	});
  
	await streamCamera.startCapture();
  
	const image = await streamCamera.takeImage();
	
	// Process image...
	fs.writeFile("./public/SavedImage/image.png", body, function(err) {
		if (err) throw err;
	});
	await streamCamera.stopCapture();
  };
  
app.get('/live-feed', (req, res) => {
	runApp().then(function (value) {
		res.writeHead(200, {'Content-Type': 'text/txt'});
		res.end();
	});
	/*
	var cameraPython = child_process.spawn('python3', ['cameraScript.py']);
	cameraPython.stdout.on('data', function (data) {
		console.log(`stdout:${data}`);
		//dataToSend = data.toString();
	});

	cameraPython.stderr.on('data', function (data) {
		console.log(`stderr:${data}`);
		//dataToSend += data.toString();
	});

	cameraPython.on('close', (code) => {
		console.log(`child process close all stdio with code ${code}`);
		//console.log(data);
		res.writeHead(200, {'Content-Type': 'text/txt'});
		res.end();
	});
	*/
});

/*
app.get('/chat', (req, res) => {


	res.render('chat', {
		title: "Chat",
		activ: 0,

	})
});
clientPi.connect(PORT, HOST, function () {
	console.log('CONNECTED TO: ' + HOST + ':' + PORT);
	// Write a message to the socket as soon as the client is connected, the server will receive it as message from the client
});
//clientPi.write('w:pressed');
client.on('data', function (data) {
console.log('DATA: ' + data);
// Close the client socket completely
client.destroy();
});
// Add a 'close' event handler for the client socket
clientPi.on('close', function () {
console.log('Connection closed');
});
*/

server.listen(port, () => console.log(`Serverul rulează la adresa http://localhost:1235/home`));
