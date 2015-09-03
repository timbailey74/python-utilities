# Analyse data logged by my Galaxy Tab.

import pandas
import numpy as np
import matplotlib.pyplot as plt
from fileio import join_path

def get_data(path, fname):
    fullname = join_path(path, fname)
    return pandas.read_csv(fullname, header=1, delimiter=';')

#
# TESTS ----------------------------------------------
#

# KEYS:
# 'LOCATION Latitude : ', 'LOCATION Longitude : ', 'LOCATION Altitude ( m)',
# 'LOCATION Speed ( Kmh)', 'LOCATION Accuracy ( m)', 'Temperature (C)',
# 'Level (%)', 'Voltage (Volt)', 'Time since start in ms ', 'YYYY-MO-DD HH-MI-SS_SSS'

def test1():
    path = 'C:/Users/tbailey/Documents/GitHub/python-utilities/tests'
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
