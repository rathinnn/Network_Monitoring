const http = require('http');
const net = require('net');
const url = require('url');
const fs = require('fs');
const mysql = require('mysql');
const path = require('path');
const { base64encode, base64decode } = require('nodejs-base64');

let public_directory = path.join(__dirname, '/');

const temp_port = 8080;

let mysql_connection = mysql.createConnection({
	host : 'localhost',
	user : 'root',
	password : '',
	database : 'zeltron'
});

const proxy_server = http.createServer(function(client_request, client_response) {
	const client_http_url = url.parse(client_request.url, true);
	if (client_http_url.hostname && client_request.method) {
		mysql_connection.query('SELECT * FROM spam_websites_database WHERE url = ?', [client_http_url.hostname], function(error, results, fields) {
			let check = false;
			if (error) {
				throw error;
				check = true;
				return;
			} else {
				if (results.length > 0) {
					if (client_request.method == "GET") {
						console.log('BLOCKED', client_request.method, '   ', '|' + client_http_url.hostname);
					} else if (client_request.method == "POST") {
						console.log('BLOCKED', client_request.method, '  ', '|' + client_http_url.hostname);
					} else if (client_request.method == "HEAD") {
						console.log('BLOCKED', client_request.method, '  ', '|' + client_http_url.hostname);
					} else {
						console.log('BLOCKED', client_request.method, '  ', '|' + client_http_url.hostname);
					}
					fs.readFile("block.html", "utf-8", function(error, data) {
						client_response.write(data);
					});
					client_response.end();
					client_response.destroy();
					return;
				} else {
					if (client_request.method == "GET") {
						console.log('ALLOWED', client_request.method, '   ', '|' + client_http_url.hostname);
					} else if (client_request.method == "POST") {
						console.log('ALLOWED', client_request.method, '  ', '|' + client_http_url.hostname);
					} else if (client_request.method == "HEAD") {
						console.log('ALLOWED', client_request.method, '  ', '|' + client_http_url.hostname);
					} else {
						console.log('ALLOWED', client_request.method, '  ', '|' + client_http_url.hostname);
					}
					var options = {
						hostname : client_http_url.hostname,
						port : 80,
						path : client_http_url.pathname,
						method : client_request.method,
						headers : client_request.headers
					}
					var server_request = http.request(options, function(server_response) {
						server_response.on('error', function(error) {
							check = true;
							return;
						});
						client_response.writeHead(server_response.statusCode, server_response.headers);
						server_response.pipe(client_response, {
							end : true
						});
					});
					server_request.on('error', function(error) {
						check = true;
						return;
					});
					if (check == true) {
						fs.readFile("error.html", "utf-8", function(error, data) {
							client_response.write(data);
						});
						client_response.end();
						client_response.destroy();
						return;
					} else {
						client_request.pipe(server_request, {
							end : true
						});
					}
				}
			}
		});
	} else {
		fs.readFile("block.html", "utf-8", function(error, data) {
			client_response.write(data);
		});
		client_response.end();
		client_response.destroy();
		return;
	}
});

const proxy_server_listener = proxy_server.listen(temp_port, function(error) {
	if (error) {
		return;
	} else {
		const listener_local_ip = proxy_server_listener.address();
		console.log('Nodejs Proxy Server running on port: ' + listener_local_ip.port);
		console.log('================================================');
		console.log('STATUS ', 'METHOD ', ' URL');
		console.log('================================================');
	}
});

proxy_server.on('connect', function(request, client_socket, head) {
	const { port, hostname } = url.parse(`//${request.url}`, false, true);
	if (hostname && port) {
		mysql_connection.query('SELECT * FROM spam_websites_database WHERE url = ?', [hostname], function(error, results, fields) {
			if (error) {
				throw error;
				client_socket.end('HTTP/1.1 500 Internal Server Error\r\n');
				client_socket.destroy();
			} else {
				if (results.length > 0) {
					if (request.method == "GET") {
						console.log('BLOCKED', request.method, '   ', '|' + hostname);
					} else if (request.method == "POST") {
						console.log('BLOCKED', request.method, '  ', '|' + hostname);
					} else if (request.method == "CONNECT") {
						console.log('BLOCKED', request.method, '|' + hostname);
					} else if (request.method == "HEAD") {
						console.log('BLOCKED', request.method, '|' + hostname);
					} else {
						console.log('BLOCKED', request.method, '|' + hostname);
					}
					client_socket.end('HTTP/1.1 401 Unauthorized\r\n');
					client_socket.destroy();
				} else {
					const server_socket = net.connect(port, hostname);
					client_socket.on('error', function(error) {
						if (server_socket) {
							server_socket.end();
							return;
						}
					});
					client_socket.on('end', function() {
						if (server_socket) {
							server_socket.end();
							return;
						}
					});
					server_socket.on('error', function(error) {
						if (client_socket) {
							client_socket.end('HTTP/1.1 500 Internal Server Error\r\n');
							client_socket.destroy();
							return;
						}
					});
					server_socket.on('end', function() {
						if (client_socket) {
							client_socket.end();
							client_socket.destroy();
							return;
						}
					});
					server_socket.on('connect', function() {
						if (request.method == "GET") {
							console.log('ALLOWED', request.method, '   ', '|' + hostname);
						} else if (request.method == "POST") {
							console.log('ALLOWED', request.method, '  ', '|' + hostname);
						} else if (request.method == "CONNECT") {
							console.log('ALLOWED', request.method, '|' + hostname);
						} else if (request.method == "HEAD") {
							console.log('ALLOWED', request.method, '|' + hostname);
						} else {
							console.log('ALLOWED', request.method, '|' + hostname);
						}
						client_socket.write([
							'HTTP/1.1 200 Connection Established',
							'Proxy-agent: zeoxy'
						].join('\r\n'));
						client_socket.write('\r\n\r\n');
						server_socket.pipe(client_socket, {
							end : false
						});
						client_socket.pipe(server_socket, {
							end : false
						});
						return;
					});
				}
			}
		});
	} else {
		client_socket.end('HTTP/1.1 500 Internal Server Error\r\n');
		client_socket.destroy();
		return;
	}
});
