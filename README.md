# 10-SQLAlchemy_challenge

completed by Li Chen 2/13/2024

decription:
data analyze: use given sqlite database of rain and temperature data in Honolulu, Hawai, run a few queries in SQLAlchemey.
design climate app: use flask, design static or dynamic query for precipitation and temperature data

steps:

Part 1: Analyze and Explore the Climate Data
1) Analyze and Explore the Climate Data
   
create_engine() to connect to SQLite database
automap_base() reflect tables into classes
create session to link Python and database

Precipitation Analysis
  get most recent date in the dataset
  get 12 months precipitation data before last date
  add data into Pandas DataFrame, plot image
  get summary statistics of precipitation data

Station Analysis
  get count of stations
  identify most active station, i.e.station with most measurements
  list station name and measurement counts in descending order
  get the lowest, highest, and average temperatures at the most-active station
  get temperatures in last 12 months at the most-active station
  plot results as histogram
  
close session 

Part 2: Design Your Climate App
1) use Flask to create routes:
  start at the homepage, list all the available routes
   /api/v1.0/precipitation
   /api/v1.0/stations
   /api/v1.0/tobs
   /api/v1.0/<start> and /api/v1.0/<start>
   /api/v1.0/<start> and /api/v1.0/<start>/<end>

2) define function in every route, returnn data as requested
  /api/v1.0/precipitation
  Convert 12 months rain data into dictionary, date-key: prcp-value
  return JSON representation of your dictionary.

  /api/v1.0/stations
  return JSON list of stations

  /api/v1.0/tobs
  get date and temp from the most-active station in last 12 months
  return JSON list

  /api/v1.0/<start> 
  /api/v1.0/<start>/<end>
  get min, avg, max temp from a given date range
  return JSON list

