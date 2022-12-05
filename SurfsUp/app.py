#########################################################################
# Part 2: Design Your Climate App
#########################################################################
# Now that you’ve completed your initial analysis, you’ll design a Flask API based on the queries that you just developed. To do so, use Flask to create your routes as follows:

### 1.  /
# Start at the homepage.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///titanic.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Passenger = Base.classes.passenger

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# List all the available routes.

@app.route("/")
def welcome():
    return(
        f"Available Routes:<br/>":
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/holiday<br/>"
    )


### 2. /api/v1.0/precipitation
# Convert the query results to a dictionary by using date as the key and prcp as the value.

@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)
    date_prcp_results = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date > '2016-08-23').all()
    
    session.close()
    
    date_prcp = list(np.ravel(date_prcp_results))

# Return the JSON representation of your dictionary.

    return jsonify = list(date_prcp)

### 3. /api/v1.0/stations

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    station_results = session.query(Measurement.station).distinct().all()
    
    session.close()
    
    stations = list(np.ravel(station_results))
    # return json representation of dict
     return jsonify(stations)


### 4. /api/v1.0/tobs

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobs_results = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.date > '2016-08-23').\
        filter(Measurement.station == "USC00519281").all()
    session.close()

# Query the dates and temperature observations of the most-active station for the previous year of data.

    tobs_date_station = list(np.ravel(tobs_results))
    
# Return a JSON list of temperature observations for the previous year.
    
    return jsonify(tobs_date_station)

### 5. /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

@app.route(f"/api/v1.0/holiday")
def holiday(start_date = '2017-07-23', end_date='2017-08-23'):

 # For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
    
    session = Session(engine)
    holiday_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()

    holiday_tobs = []
    for min, avg, max in holiday_results:
        hol_dict = {}
        hol_dict["Min"] = min
        hol_dict["Average"] = avg
        hol_dict["Max"] = max
        holday_tobs.append(hol_dict)

    return jsonify(holiday_tobs)


if __name__ == '__main__':
    app.run(debug=True)
