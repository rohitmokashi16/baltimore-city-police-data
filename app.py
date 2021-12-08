from Include.visualizations.CentroidBalt import CentroidBaltimore
from flask import Flask, jsonify, request
from flask_cors import CORS
from Include.visualizations.CrimeVisualizations import CrimeVisualizations
from Include.visualizations.CrimeCalendar import CrimeCalendar
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

sqlEngine = create_engine('mysql+pymysql://root:iNsq4A4ECHNwfn0C@34.134.10.145/crime_data', pool_recycle=3600)
connection = sqlEngine.connect()
print(connection)

prepros_obj = Preprocessing()
data = prepros_obj.final_dataset

v = CrimeVisualizations(prepros_obj)
c = CrimeCalendar(prepros_obj)

def queryDB(lower, upper, neighborhood, crime_type):
    return prepros_obj.dataset_read_all_params(lower, upper, neighborhood, crime_type);

j = CentroidBaltimore(prepros_obj.df_all_params)

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
    lower = request.args.get('lower')
    upper = request.args.get('upper')
    swarm = request.args.get('swarm')
    crime_type = request.args.get('crime_type')
    neighborhood = request.args.get('neighborhood')
    return v.day_of_the_week_boxplot(year_or_month, lower, upper, swarm, neighborhood, crime_type)

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
    lower = request.args.get('lower')
    upper = request.args.get('upper')
    neighborhood = request.args.get('neighborhood')
    crime_type = request.args.get('crime_type')
    return v.indoor_outdoor_crimes_trends(year_or_month, lower, upper, neighborhood, crime_type)

@app.route('/d/crime_calendar', methods=['GET'])
def crime_calendar():
    lower = request.args.get('lower')
    upper = request.args.get('upper')
    neighborhood = request.args.get('neighborhood')
    crime_type = request.args.get('crime_type')
    return c.yearCalendar(lower, upper, neighborhood, crime_type)

@app.route('/r/map_data', methods=['GET'])
def queryDB1():
    lower = request.args.get('lower')
    upper = request.args.get('upper')
    neighborhood = request.args.get('neighborhood')
    crime_type = request.args.get('crime_type')
    return queryDB(lower, upper, neighborhood, crime_type)


@app.route('/v/district_crime_bar_charts', methods=['GET'])
def district_crime_bar_charts():
    lower = int(request.args.get('lower'))
    upper = int(request.args.get('upper'))
    swarm = bool(request.args.get('swarm'))
    return v.district_crime_bar_charts(lower, upper, swarm)

@app.route('/j/crime_centroid', methods=['GET'])
def crime_centroid():
    lower = request.args.get('lower')
    upper = request.args.get('upper')
    neighborhood = request.args.get('neighborhood')
    crime_type = request.args.get('crime_type')
    return j.getCentroidForParams(lower, upper, neighborhood, crime_type)


if __name__ == '__main__':
    app.run(threaded=True)