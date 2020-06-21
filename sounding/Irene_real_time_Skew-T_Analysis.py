# Import all necessary modules
from datetime import datetime
import matplotlib.pyplot as plt
from metpy.plots import SkewT
from metpy.units import pandas_dataframe_to_unit_arrays, units
import numpy as np
from siphon.simplewebservice.wyoming import WyomingUpperAir

# Set time using a datetime object and station as variables
# Plan to soft code these variables in future updates, 

# to make it easy to access any station in South Africa for any given time
dt = datetime(2020, 6, 21, 12)
station = 'FAIR'

# Grab remote data from server at the University of Wyoming. This requires internet connection.
# Read remote sounding data based on time (dt) and station
df = WyomingUpperAir.request_data(dt, station)

# Create dictionary of united arrays
data = pandas_dataframe_to_unit_arrays(df)

# Isolate united arrays from dictionary to individual variables and attach units.
p = data['pressure']
T = data['temperature']
Td = data['dewpoint']
u = data['u_wind']
v = data['v_wind']

# The code below makes a basic skew-T plot using the MetPy plot module that contains a SkewT class.

# Change default to be better for skew-T
fig = plt.figure(figsize=(9, 11))

# Initiate the skew-T plot type from MetPy class loaded earlier
skew = SkewT(fig, rotation=45)

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot
skew.plot(p, T, 'r')
skew.plot(p, Td, 'g')
skew.plot_barbs(p[::3], u[::3], v[::3], y_clip_radius=0.03)

# Set some appropriate axes limits for x and y
skew.ax.set_xlim(-40, 40)
skew.ax.set_ylim(1020, 100)

# Add the relevant special lines to plot throughout the figure
skew.plot_dry_adiabats(t0=np.arange(233, 533, 10) * units.K,
                       alpha=0.25, color='orangered')
skew.plot_moist_adiabats(t0=np.arange(233, 400, 5) * units.K,
                         alpha=0.25, color='tab:green')
skew.plot_mixing_lines(p=np.arange(1000, 99, -20) * units.hPa,
                       linestyle='dotted', color='tab:blue')

# Add some descriptive titles. For 'exact' station name as from the server pull, use {}.
plt.title('IRENE Sounding'.format(station), loc='left')
plt.title('Date & Time: {} UTC'.format(dt), loc='center')

# Use plt.show() if you want a pop up image when you run the script

# Save the figure in current folder
fig.savefig('Irene_real_time_Skew-T_Analysis.png',dpi=100,bbox_inches='tight')
