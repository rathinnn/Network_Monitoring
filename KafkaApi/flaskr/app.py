from flask import Flask, render_template, request, url_for, redirect,jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/sendJsonlog',methods=['POST'])
def getData():
    content = request.json
    return jsonify({"Status":True})

if __name__ == '__main__':
    app.run(debug=True)