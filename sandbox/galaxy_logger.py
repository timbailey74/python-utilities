# Analyse data logged by my Galaxy Tab.

import pandas
import numpy as np
import matplotlib.pyplot as plt
from fileio import join_path

def get_data(path, fname):
    fullname = join_path(path, fname)
    return pandas.read_csv(fullname, header=1, delimiter=';')

def latlong2metres():
    #http://stackoverflow.com/questions/639695/how-to-convert-latitude-or-longitude-to-meters
    R = 6378.137  # radius of earth in km


function measure(lat1, lon1, lat2, lon2){  // generally used geo measurement function
    var R = 6378.137; // Radius of earth in KM
    var dLat = (lat2 - lat1) * Math.PI / 180;
    var dLon = (lon2 - lon1) * Math.PI / 180;
    var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon/2) * Math.sin(dLon/2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    var d = R * c;
    return d * 1000; // meters
}

def extract_sql(fname):
    https://docs.python.org/2/library/sqlite3.html
    http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html
    http://stackoverflow.com/questions/305378/get-list-of-tables-db-schema-dump-etc-in-sqlite-databases

#
# TESTS ----------------------------------------------
#

# KEYS:
# 'LOCATION Latitude : ', 'LOCATION Longitude : ', 'LOCATION Altitude ( m)',
# 'LOCATION Speed ( Kmh)', 'LOCATION Accuracy ( m)', 'Temperature (C)',
# 'Level (%)', 'Voltage (Volt)', 'Time since start in ms ', 'YYYY-MO-DD HH-MI-SS_SSS'

def test1():
    path = 'C:/Users/tbailey/Documents/GitHub/python-utilities/tests/data'
    fnames = ['Sensor_record_20150828_141657_AndroSensor.csv', 'Sensor_record_20150828_151150_AndroSensor.csv']
    data = get_data(path, fnames[1])
    #print(data.keys())
    x, y, z = data['LOCATION Latitude : '], data['LOCATION Longitude : '], data['LOCATION Altitude ( m)']
    t, v = data['Time since start in ms '], data['LOCATION Speed ( Kmh)']
    Factor = 100 # FIXME: do conversion properly
    y, x, z, t = Factor*(x-x[0])*1000, Factor*(y-y[0])*1000, z-z[0], t/1000.
    plt.plot(t, x, t, y, t, z), plt.grid()
    plt.figure()
    plt.plot(t, np.sqrt(x**2 + y**2)), plt.grid()
    plt.figure()
    plt.plot(t, v), plt.grid()
    plt.figure()
#    plt.plot(t[:-1], abs(np.diff(np.sqrt(x**2 + y**2))) / np.diff(t))
#    plt.plot(t[1:-1:2], abs(np.diff(np.sqrt(x[::2]**2 + y[::2]**2))) / np.diff(t[::2]))
#    plt.plot(t[2:-1:3], abs(np.diff(np.sqrt(x[::3]**2 + y[::3]**2))) / np.diff(t[::3]))
    plt.plot(t[2:-2:4], abs(np.diff(np.sqrt(x[::4]**2 + y[::4]**2))) / np.diff(t[::4]))
    plt.figure()
    plt.plot(x, y, '.-'), plt.axis('equal'), plt.grid()
    plt.show()

#
#
#

test1()
