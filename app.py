from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import create_engine, inspect, func

import datetime as dt
import pandas as pd
import numpy as np

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")


app = Flask(__name__)

Base = automap_base()
Base.prepare(engine, reflect=True)

station = Base.classes.Station
Measurement = Base.classes.Measurement
session = Session(engine)

@app.route("/")
def welcome():
   """List all available api routes."""
   return (
       f"Available Routes:<br/>"
       f"/api/v1.0/precipitation<br/>"
       f"/api/v1.0/stations<br/>"
       f"/api/v1.0/tobs<br/>"
       f"/api/v1.0/start<br/>"
       f"/api/v1.0/startend"
   )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    measure_dict = {}
    measure_dict["date"] = session.query(Measurement.date).all()
    measure_dict["tobs"] = session.query(Measurement.tobs).all()
    
    return jsonify(measure_dict)

@app.route("/api/v1.0/stations")
def station_temp():
    
    station_dict = {}
    station_dict["station"] = session.query(Measurement.station).all()
    
    return jsonify(station_dict)

@app.route("/api/v1.0/tobs")
def temp_obs():
    

    temp_dict = {}
    temp_dict["tobs"] = session.query(Measurement.tobs,Measurement.date).\
    filter(Measurement.date >= (dt.date.today() - dt.timedelta(days=365))).all()
    
    return jsonify(temp_dict)


@app.route("/api/v1.0/start")
def recent_temp():
    
    start_date = '2017-01-01'
    
    recent_dict = {}
    recent_dict["Min"] = session.query(func.min(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()
    
    recent_dict["Avg"] = session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()
    
    recent_dict["Max"] = session.query(func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()
    
    return jsonify(recent_dict)

@app.route("/api/v1.0/startend")
def range_temp():
    
    start_date = '2017-01-01'
    end_date = '2017-12-31'
    
    startend_dict = {}
    startend_dict["Min"] = session.query(func.min(Measurement.tobs)).\
    filter(Measurement.date >= start_date).\
    filter(Measurement.date <= end_date).all()
    
    startend_dict["Avg"] = session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start_date).\
    filter(Measurement.date <= end_date).all()
    
    startend_dict["Max"] = session.query(func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).\
    filter(Measurement.date <= end_date).all()
    
    return jsonify(startend_dict)


if __name__ == '__main__':
    app.run(debug=True)