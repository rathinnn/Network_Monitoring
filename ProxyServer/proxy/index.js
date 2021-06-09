const express = require('express');
const cookie_parser = require('cookie-parser');
const body_parser = require('body-parser');
const mysql = require('mysql');
const path = require('path');

let app = express();

let mysql_connection = mysql.createConnection({
	host : 'localhost',
	user : 'root',
	password : '',
	database : 'zeltron'
});

mysql_connection.on('error', (error) => {
	console.log('MYSQL connection failed!');
	process.exit();
});

app.set('view engine', 'ejs');

app.use(body_parser.urlencoded({
	extended : true
}));

app.use(body_parser.json());

app.use(cookie_parser());

app.use('/pictures', express.static(path.join(__dirname + '/images')));
app.use('/style', express.static(path.join(__dirname + '/css')));
app.use('/javascript', express.static(path.join(__dirname + '/javascript_files')));

let port = 8080;
let cookie_length = 10;

let cookie_generator = (length) => {
	let characters_list = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
	let temp = '';
	for (let i = 0; i < length; i ++) {
		temp += characters_list.charAt(Math.floor(Math.random() * characters_list.length));
	}
	return temp;
}

let cookie_remover = (request, response) => {
	if (request.cookies['session_id'] && request.cookies['username']) {
		response.clearCookie('session_id');
		response.clearCookie('username');
	}
}

app.get('/', (request, response) => {
	cookie_remover(request, response);
	response.sendFile(path.join(__dirname + '/html/homepagewithoutlogin.html'));
});

app.get('/signup', (request, response) => {
	cookie_remover(request, response);
	response.render(path.join(__dirname + '/html/signuppage.ejs'), {
		check : 0
	});
});

app.get('/login', (request, response) => {
	cookie_remover(request, response);
	response.render(path.join(__dirname + '/html/loginpage.ejs'), {
		check : 0
	});
});

app.post("/signupinfo", (request, response) => {
	cookie_remover(request, response);
	if (request.body.username && request.body.password && request.body.checkpassword && request.body.username.length < 999 && request.body.password.length < 999 & request.body.checkpassword.length < 999) {
		if (request.body.password == request.body.checkpassword) {
			mysql_connection.query("SELECT * FROM users WHERE username = ?", [request.body.username], (error, results, fields) => {
				if (error) {
					console.log("MYSQL error!");
				} else {
					if (results.length == 1) {
						response.render(path.join(__dirname + '/html/signuppage.ejs'), {
							check : 3
						});
					} else {
						mysql_connection.query("INSERT INTO users (username, password, session_id) VALUES (?, ?, ?)", [request.body.username, request.body.password, 'not set'], (error, results, fields) => {
							if (error) {
								console.log("MYSQL error!");
							} else {
								response.redirect("/login");
							}
						});
					}
				}
			});
		} else {
			response.render(path.join(__dirname + '/html/signuppage.ejs'), {
				check : 2
			});
		}
	} else {
		response.render(path.join(__dirname + '/html/signuppage.ejs'), {
			check : 1
		});
	}
});

app.post('/logininfo', (request, response) => {
	cookie_remover(request, response);
	if (request.body.username && request.body.password && request.body.username.length < 999 && request.body.password.length < 999) {
		mysql_connection.query("SELECT * FROM users WHERE username = ? AND password = ?", [request.body.username, request.body.password], (error, results, fields) => {
			if (error) {
				console.log('MYSQL error!');
			} else {
				if (results.length == 1) {
					response.cookie('username', request.body.username, {
						httpOnly : true
					});
					let temp = cookie_generator(cookie_length);
					response.cookie('session_id', temp, {
						httpOnly : true
					});
					mysql_connection.query('UPDATE users SET session_id = ? WHERE username = ?', [temp, request.body.username], (error, results, fields) => {
						if (error) {
							console.log("MYSQL error!");
						} else {
							response.redirect('/loggedin');
						}
					});
				} else {
					response.render(path.join(__dirname + '/html/loginpage.ejs'), {
						check : 2
					});
				}
			}
		});
	} else {
		response.render(path.join(__dirname + '/html/loginpage.ejs'), {
			check : 1
		});
	}
});

app.get('/loggedin', (request, response) => {
	if (request.cookies['username'] && request.cookies['session_id']) {
		mysql_connection.query("SELECT * FROM users WHERE username = ?", [request.cookies['username']], (error, results, fields) => {
			if (error) {
				console.log("MYSQL error!");
			} else {
				if (results.length == 1) {
					if (results[0].session_id == request.cookies['session_id'] && results[0].session_id != 'not set') {
						response.render(path.join(__dirname + '/html/homepagelogin.ejs'), {
							user : request.cookies['username'],
							check : 0
						});
					} else {
						cookie_remover(request, response);
						response.redirect("/login");
					}
				} else {
					cookie_remover(request, response);
					response.redirect("/login");
				}
			}
		});
	} else {
		cookie_remover(request, response);
		response.redirect('/login');
	}
});

app.post('/addurl', (request, response) => {
	if (request.cookies['username'] && request.cookies['session_id']) {
		mysql_connection.query("SELECT * FROM users WHERE username = ?", [request.cookies['username']], (error, results, fields) => {
			if (error) {
				console.log("MYSQL error!");
			} else {
				if (results.length == 1) {
					if (results[0].session_id == request.cookies['session_id'] && results[0].session_id != 'not set') {
						let temp = request.body.url;
						let domain_array = temp.split('.');
						let check = false;
						let regex = /^[A-Za-z0-9 ]+$/;
						for (let i = 0; i < domain_array.length; i ++) {
							if (domain_array[i].match(regex)) {
								continue;
							} else {
								check = true;
								break;
							}
						}
						if (check) {
							response.render(path.join(__dirname + '/html/homepagelogin.ejs'), {
								user : request.cookies['username'],
								check : 1
							});
						} else {
							mysql_connection.query('SELECT * FROM urls WHERE url = ?', [request.body.url], (error, results, fields) => {
								if (error) {
									console.log('MYSQL error!');
								} else {
									if (results.length == 1) {
										response.render(path.join(__dirname + '/html/homepagelogin.ejs'), {
											user : request.cookies['username'],
											check : 2
										});
									} else {
										mysql_connection.query("INSERT INTO urls (url) VALUES (?)", [request.body.url], (error, results, fields) => {
											if (error) {
												console.log('MYSQL error!');
											} else {
												response.render(path.join(__dirname + '/html/homepagelogin.ejs'), {
													user : request.cookies['username'],
													check : 3
												});
											}
										});
									}
								}
							});
						}
					} else {
						cookie_remover(request, response);
						response.redirect("/login");
					}
				} else {
					cookie_remover(request, response);
					response.redirect('/login');
				}
			}
		});
	} else {
		cookie_remover(request, response);
		response.redirect('/login');
	}
});

app.post('/searchurl', (request, response) => {
	if (request.cookies['username'] && request.cookies['session_id']) {
		mysql_connection.query("SELECT * FROM users WHERE username = ?", [request.cookies['username']], (error, results, fields) => {
			if (error) {
				console.log("MYSQL error!");
			} else {
				if (results.length == 1) {
					if (results[0].session_id == request.cookies['session_id'] && results[0].session_id != 'not set') {
						let temp = request.body.url;
						let domain_array = temp.split('.');
						let check = false;
						let regex = /^[A-Za-z0-9 ]+$/;
						for (let i = 0; i < domain_array.length; i ++) {
							if (domain_array[i].match(regex)) {
								continue;
							} else {
								check = true;
								break;
							}
						}
						if (check) {
							response.render(path.join(__dirname + '/html/homepagelogin.ejs'), {
								user : request.cookies['username'],
								check : 4
							});
						} else {
							mysql_connection.query("SELECT * FROM urls WHERE url = ?", [request.body.url], (error, results, fields) => {
								if (error) {
									console.log('MYSQL error!');
								} else {
									if (results.length == 1) {
										response.render(path.join(__dirname + '/html/homepagelogin.ejs'), {
											user : request.cookies['username'],
											check : 5
										});
									} else {
										response.render(path.join(__dirname + '/html/homepagelogin.ejs'), {
											user : request.cookies['username'],
											check : 6
										});
									}
								}
							});
						}
					} else {
						cookie_remover(request, response);
						response.redirect("/login");
					}
				} else {
					cookie_remover(request, response);
					response.redirect('/login');
				}
			}
		});
	} else {
		cookie_remover(request, response);
		response.redirect('/login');
	}
});

app.get('/logout', (request, response) => {
	cookie_remover(request, response);
	if (request.cookies['username'] && request.cookies['session_id']) {
		mysql_connection.query("SELECT * FROM users WHERE username = ?", [request.cookies['username']], (error, results, fields) => {
			if (error) {
				console.log("MYSQL error!");
			} else {
				if (request.cookies['session_id'] == results[0].session_id) {
					mysql_connection.query("UPDATE users SET session_id = ? WHERE username = ?", ['not set', request.cookies['username']], (error, results, fields) => {
						if (error) {
							console.log("MYSQL error!");
						}
					});
				}
			}
		});
	}
	response.redirect('/');
});

app.listen(port, (error) => {
	if (error) {
		console.log('Port 8080 not idle!');
		process.exit();
	} else {
		console.log('Listening at port: 8080');
	}
});
