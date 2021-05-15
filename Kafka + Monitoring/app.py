from Monitoring.flaskr.app import app as monitor
from KafkaApi.flaskr.app import app as api
from werkzeug.middleware.dispatcher import DispatcherMiddleware

import flask
app = flask.Flask(__name__)
app.wsgi_app = DispatcherMiddleware(api, {
    '/spark': monitor.server
})

if __name__ == '__main__':
    app.run(port = 8080)