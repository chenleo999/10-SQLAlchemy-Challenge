# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# 1. Start at the homepage. List all the available routes.
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# 2. convert rain data in to dict and return json 
@app.route("/api/v1.0/precipitation")
def prep():
    rain_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= dt.date(2016,8,23)).all()

    rain_dict = {}
    for date, prcp in rain_data:
        rain_dict[date] = prcp
        
    return rain_dict

# 3. return all stations in json list
@app.route("/api/v1.0/stations")
def stat():
    station_data = session.query(Station.name, Station.station).all()
    
    station_list = []
    for stat in station_data:
        station_list.append(stat)
        
    return jsonify(station_list)

# 4. most active station USC00519281 measurements in 1 year
@app.route("/api/v1.0/tobs")
def actstat():
    temperature_data = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= dt.date(2016,8,18)).\
    filter(Measurement.station == 'USC00519281').all()
    
    act_stat_measure = []
    for measure in temperature_data:
        act_stat_measure.append(measure)
        
    return jsonify(act_stat_measure)


# 5. min/avg/max temperature from given start date to end of data
@app.route("/api/v1.0/<start>")
def startfrom(startdate):
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]    
    measurement = session.query(*sel).filter(Measurement >= startdate).\
    group_by(Measurement.date).order_by(Measurement.date).all()
    
    temp = []
    for data in measurement:
        temp.append(data)
    
    if len(temp) > 0:
        return jsonify(temp)
    else:
        return jsonify({"error": f"no data from given start date {startdate}"}), 404
    
    
 # 6 min/avg/max temperature between given start and end date, inclusive
@app.route("/api/v1.0/<start>/<end>")
def startfrom(startdate, enddate):
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]    
    measurement = session.query(*sel).filter(Measurement >= startdate).filter(Measurement <= enddate).\
    group_by(Measurement.date).order_by(Measurement.date).all()
    
    temp = []
    for data in measurement:
        temp.append(data)
    
    if len(temp) > 0:
        return jsonify(temp)
    else:
        return jsonify({"error": f"no data in given date range {startdate} - {enddate}"}), 404
 

if __name__ == '__main__':
    app.run(debug=True)