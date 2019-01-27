# import dependencies 
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

###########################################################
# Database Setup
###########################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session (link) from Python to Database
session = Session(engine)

##########################################################
# Flask Setup
##########################################################
app = Flask(__name__)

##########################################################
# Flask Routes
##########################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"- List of prior year rain totals from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"- List of Station numbers and names<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- List of prior year temperatures from all stations<br/>"
        f"<br/>"
    )
########################################################################################

# Query for the dates and precipitation values from the last year.
# Convert the query results to a Dictionary using date as the key and tobs as the value.
# Return the json representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    """ Return a list of measurement date and prcp information from the last year """
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date)
    
    # Create a dictionary from the row data and append to a list
    precipitation_values = []
    for p in results:
        prcp_dict = {}
        prcp_dict["date"] = p.date
        prcp_dict["prcp"] = p.prcp
        precipitation_values.append(prcp_dict)

    return jsonify(precipitation_values)

# Return a json list of stations from the dataset.
#
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all station names"""
    # Query all stations
    results = session.query(Station.name).all()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(results))

    return jsonify(station_names)

# Return a json list of Temperature Observations (tobs) for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all temperature observations for the previous year"""
    # Query all tobs values
    results = session.query(Measurement.tobs).all()

    # Convert list of tuples into normal list
    tobs_values = list(np.ravel(results))

    return jsonify(tobs_values)

########################################################

if __name__ == "__main__":
    app.run(debug=True)