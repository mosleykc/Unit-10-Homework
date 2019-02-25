# design a Flask API based on the queries that you have just developed.
# Use FLASK to create your routes.

# Import Dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
# setup app engine, create app engine and where launched
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#Homepage - base end point
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii Climate Analysis API!"
        f"Available Routes:<br><br>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end<br/>"
            )
#########################################################################################

# Query for the dates and precipitation observations from the last year.
## Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
## Return the json representation of your dictionary.

# Precipitation end point
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the JSON representation of your dictionary."""
    # query dates and precip
    precip_scores = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()

#  Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.

    precip_totals = []
    for precip_scores in precip_scores:
        precip_dict = {}
        precip_dict["date"] = precip_scores.date
        precip_dict["prcp"] = precip_scores.prcp
        precip_totals.append(precip_dict)

    return jsonify(precip_totals)

#########################################################################################
# Return a JSON list of stations from the dataset

# Stations end point
@app.route("/api/v1.0/stations")
def stations():
    # Query all sations
    station_list = session.query(Station.name).all()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(station_list))

    return jsonify(station_names)
    
    
#########################################################################################
# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.

# tobs end point
@app.route("/api/v1.0/tobs")
def tobs():

    """Return a list of all temperature observations for the previous year"""
    # Query all tobs values
    results = session.query(Measurement.tobs).all()

    # Convert list of tuples into normal list
    tobs = list(np.ravel(results))

    return jsonify(tobs)


#########################################################################################

# Return a JSON list of the minimum temperature, the average temperature, and the max \
# temperature for a given start or start-end range.
# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for \
# dates between the start and end date inclusive.

# Start/End end point
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    """Return minimum temperature, the average temperature, and the max temperature"""
    # Perform query
    temp_min_max_avg = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), \
        func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    # convert lists of tuples into normal list
    temps_list = list(np.ravel(temp_min_max_avg))

    return jsonify(temps_list)


#########################################################################################
# Code to ensure app is run as app server instead of library
if __name__ == '__main__':
    app.run(debug=True)
