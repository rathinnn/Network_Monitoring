import requests
from flask import Flask
from flask import render_template
from Monitoring.flaskr.dashboard.dashapp import init_dashboard

app = Flask(__name__, instance_relative_config=False)
app = init_dashboard(app)

#if __name__ == '__main__':
#    app.run(port = 8000)
