import os
from flask import Flask, render_template, request
from flask_cors import CORS
import remlaversionutilpy
import requests

app = Flask(__name__, template_folder='../app-frontend/templates', static_folder='../app-frontend/static')
CORS(app)

model_service_url = os.getenv('MODEL_SERVICE_URL')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/version', methods=['GET'])
def version():
    return f'Version {remlaversionutilpy.VersionUtil.get_version()}'

@app.route('/check-url', methods=['POST'])
def check_url():
    json = request.get_json()
    for i in range(10):
        print(model_service_url)
    #response = requests.post(os.getenv('MODEL_SERVICE_URL'), json=json)
    response = requests.post(model_service_url + "/querymodel", json=json)
    return response.json()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8080)
