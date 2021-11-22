## Database Manager Block
# Write to and Read from Influxdb

from flask import Flask, request
from flask_restful import Api, Resource
from influxdb import InfluxDBClient


app = Flask(__name__)
api = Api(app)

# influxdb details
"""Instantiate a connection to the InfluxDB."""
dbhost = 'localhost'
dbport = 8086
dbuser = 'root'
dbpassword = 'root'
dbname = 'sensordataDB'  #name of the database created

# creating client instance
dbclient = InfluxDBClient(dbhost, dbport, dbuser, dbpassword, dbname)
dbclient.create_database(dbname)



class DatabaseManager(Resource):

	def post(self):
		data_write = request.get_json()
		dbclient.write_points(data_write)
		

	def get(self):
		return list(dbclient.query('select last(*) from sensordata'))[0][0]



api.add_resource(DatabaseManager,"/iotpoc")

if __name__ == "__main__":
	app.run(debug=False,port = 8080)
