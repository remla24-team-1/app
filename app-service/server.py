import os
from flask import Flask, render_template, request
from flask_cors import CORS
import remlaversionutilpy
import requests
from dotenv import load_dotenv

app = Flask(__name__, template_folder='../app-frontend/templates', static_folder='../app-frontend/static')
CORS(app)
load_dotenv()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/version', methods=['GET'])
def version():
    return f'Version {remlaversionutilpy.VersionUtil.get_version()}'

@app.route('/check-url', methods=['POST'])
def check_url():
    json = request.get_json()
    response = requests.post(os.getenv('MODEL_SERVICE_URL'), json=json)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True, port=8080)
