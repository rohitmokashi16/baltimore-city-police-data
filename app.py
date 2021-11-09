from flask import Flask, jsonify, request
from flask_cors import CORS
from env.Include.visualizations.CrimeVisualizations import CrimeVisualizations
from env.Include.util.Preprocessing import Preprocessing
from env.Include.visualizations.ImageReturn import returnImage
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__, static_folder='../client/dist/', static_url_path='/')
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

prepros_obj = Preprocessing()
prepros_obj.dataset_path = "./env/Include/sample/Part1_Crime_data.csv"
prepros_obj.dataset_read('csv')
prepros_obj.dataset_all_updations()
data = prepros_obj.final_dataset

v = CrimeVisualizations()


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
    return v.day_of_the_week_boxplot(prepros_obj.final_dataset, year_or_month, lower, upper, swarm)

@app.route('/v/district_wise_boxplot', methods=['GET'])
def v_district_wise_boxplot():
    year_or_month = request.args.get('ym')
    lower = int(request.args.get('lower'))
    upper = int(request.args.get('upper'))
    swarm = bool(request.args.get('swarm'))
    return v.district_wise_boxplot(data, year_or_month, lower, upper, swarm)

@app.route('/v/indoor_outdoor_crimes_trends', methods=['GET'])
def indoor_outdoor_crimes_trends():
    year_or_month = request.args.get('ym')
    lower = int(request.args.get('lower'))
    upper = int(request.args.get('upper'))
    return v.indoor_outdoor_crimes_trends(data, year_or_month, lower, upper)

@app.route('/v/district_crime_bar_charts', methods=['GET'])
def district_crime_bar_charts():
    lower = int(request.args.get('lower'))
    upper = int(request.args.get('upper'))
    swarm = bool(request.args.get('swarm'))
    return v.district_crime_bar_charts(data, lower, upper, swarm)

if __name__ == '__main__':
    app.run()