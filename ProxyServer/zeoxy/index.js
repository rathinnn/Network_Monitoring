const http = require('http');
const net = require('net');
const url = require('url');

const temp_port = 8080;

const proxy_server = http.createServer((request, response) => {
	response.write('Methods other than HTTP/1.1 CONNECT method are not accepted!');
	response.end();
});

const proxy_server_listener = proxy_server.listen(temp_port, (error) => {
	if (error) {
		return console.error(error);
	}
	const listener_local_ip = proxy_server_listener.address();
	console.log('Nodejs Proxy Server running on port: ' + listener_local_ip.port);
	console.log('================================================');
});

proxy_server.on('connect', (request, client_socket, head) => {
	console.log(request.method, request.url);
	const { port, hostname } = url.parse(`//${request.url}`, false, true);
	if (hostname && port) {
		const server_socket = net.connect(port, hostname);
		client_socket.on('error', (error) => {
			console.error(error.message);
			if (server_socket) {
				server_socket.end();
			}
		});
		client_socket.on('end', () => {
			if (server_socket) {
				server_socket.end();
			}
		});
		server_socket.on('error', (error) => {
			console.error(error.message);
			if (client_socket) {
				client_socket.end(`HTTP/1.1 500 ${error.message}\r\n`);
			}
		});
		server_socket.on('end', () => {
			if (client_socket) {
				client_socket.end(`HTTP/1.1 500 External Server End\r\n`);
			}
		});
		server_socket.on('connect', () => {
			client_socket.write([
				'HTTP/1.1 200 Connection Established',
				'Proxy-agent: zeltron',
			].join('\r\n'));
			client_socket.write('\r\n\r\n');
			server_socket.pipe(client_socket, { end : false });
			client_socket.pipe(server_socket, { end : false });
		});
	} else {
		client_socket.end('HTTP/1.1 400 Bad Request\r\n');
		client_socket.destroy();
	}
});
