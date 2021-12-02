from flask import Flask, jsonify, request
from flask_cors import CORS
from Include.visualizations.CrimeVisualizations import CrimeVisualizations
from Include.sample.Preprocessing import Preprocessing
from env.Include.visualizations.ImageReturn import returnImage
from sqlalchemy import create_engine

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__, static_folder='./dist', static_url_path='/')
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

sqlEngine = create_engine('mysql+pymysql://root:password@127.0.0.1/crime_data', pool_recycle=3600)
connection = sqlEngine.connect()

prepros_obj = Preprocessing()
data = prepros_obj.final_dataset

v = CrimeVisualizations(prepros_obj)

@app.route("/", defaults={"path": ""})
@app.route("/<string:path>")
@app.route("/<path:path>")
def index(path):
    return app.send_static_file("index.html")

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return 'Hit'


@app.route('/vue', methods=['GET'])
def return_image():
    return returnImage()

@app.route('/v/day_of_the_week_boxplot', methods=['GET'])
def v_day_of_the_week_boxplot():
    year_or_month = request.args.get('ym')
    lower = int(request.args.get('lower'))
    upper = int(request.args.get('upper'))
    swarm = bool(request.args.get('swarm'))
    return v.day_of_the_week_boxplot(year_or_month, lower, upper, swarm)

@app.route('/v/district_wise_boxplot', methods=['GET'])
def v_district_wise_boxplot():
    year_or_month = request.args.get('ym')
    lower = int(request.args.get('lower'))
    upper = int(request.args.get('upper'))
    swarm = bool(request.args.get('swarm'))
    return v.district_wise_boxplot(year_or_month, lower, upper, swarm)

@app.route('/v/indoor_outdoor_crimes_trends', methods=['GET'])
def indoor_outdoor_crimes_trends():
    year_or_month = request.args.get('ym')
    lower = int(request.args.get('lower'))
    upper = int(request.args.get('upper'))
    return v.indoor_outdoor_crimes_trends(year_or_month, lower, upper)

@app.route('/v/district_crime_bar_charts', methods=['GET'])
def district_crime_bar_charts():
    lower = int(request.args.get('lower'))
    upper = int(request.args.get('upper'))
    swarm = bool(request.args.get('swarm'))
    return v.district_crime_bar_charts(lower, upper, swarm)

if __name__ == '__main__':
    app.run(threaded=True)