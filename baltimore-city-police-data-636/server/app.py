from flask import Flask, jsonify
from flask_cors import CORS
from env.Include.visualizations.CrimeVisualizations import buildVisualization
from env.Include.util.Preprocessing import Preprocessing
from env.Include.visualizations.ImageReturn import returnImage
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return buildVisualization()


@app.route('/vue', methods=['GET'])
def return_image():
    return returnImage()

if __name__ == '__main__':
    app.run()