from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder='../app-frontend/templates', static_folder='../app-frontend/static')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
