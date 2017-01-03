###########################################################################
# Program:  region_map.py
# Author:   Sarah Sparrow
# Date:     03/01/2017
# Purpose:  To plot weather@home regions
###########################################################################
import sys
import os
import numpy as np
import math
import datetime
import fnmatch
import matplotlib
import glob
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

from scipy.io import netcdf


# Dictionary detailing region names, colour and whether to display the outline as dotted
region_dict={'afr50':('Sienna',False),'nawa25':('HotPink',False),'anz50':('Gold',False),'eas50':('Red',False),'eu25':('SpringGreen',False),'eu50r':('RoyalBlue',False),'cam50':('DarkOrange',False),'cam25':('DeepSkyBlue',False),'pnw25':('ForestGreen',False),'sas50':('BlueViolet',False),'wus25':('YellowGreen',False),'sam50':('LemonChiffon',False),'cafr25':('LightSalmon',False)}

def get_rot_global_coords(region_file):
    f=netcdf.netcdf_file('data/'+region_file,'r')
    glat=f.variables['global_latitude0']
    glon=f.variables['global_longitude0']
    f.close()
    return glat,glon   

def get_global_coords(region_file):
    f=netcdf.netcdf_file('data/'+region_file,'r')
    lat=f.variables['latitude0']
    lon=f.variables['longitude0']
    f.close()
    return lat,lon
 
def map_plot():
    # Plot a map of the seasonal ocean climatology
    # Set the plot font size
    font = {'family' : 'sans-serif',
            'size'   : 14}
    matplotlib.rc('font', **font)

    # Produce the map plot
    fig = plt.figure()
    m = Basemap(projection='robin',lon_0=35,resolution='c')
    m.bluemarble()
    m.drawmapboundary()
    for region,region_style in region_dict.iteritems():
    	region_file=region+"_region.nc"
	region_col=region_style[0]
	region_line=region_style[1]
	print region_file
	if region=="afr50" or region=="nawa25" or region=="cafr25":
	    lat,lon=get_global_coords(region_file)
            for i in range(0,4):
               if i==0:
                   longitude=np.repeat(lon[0],lat.shape)
		   latitude=lat[:]
               elif i==1:
                   longitude=lon[:]
                   latitude=np.repeat(lat[0],lon.shape)
               elif i==2:
                   longitude=np.repeat(lon[-1],lat.shape)
                   latitude=lat[:]
               elif i==3:
                   longitude=lon[:]
                   latitude=np.repeat(lat[-1],lon.shape)
               x, y = m(longitude, latitude)
	       if region_line==True:
	           plt.scatter(x[::5],y[::5],lw=1,s=2, c=region_col,edgecolor=region_col,zorder=1)
               else:
	           plt.scatter(x,y,lw=1,s=2, c=region_col,edgecolor=region_col,zorder=1)	
	else:
            glat,glon=get_rot_global_coords(region_file)
            for i in range(0,4):
    	       if i==0:
	           longitude=glon[0,:]
	           latitude=glat[0,:]
	       elif i==1:
	           longitude=glon[:,0]
                   latitude=glat[:,0]
               elif i==2:
	           longitude=glon[-1,:]
                   latitude=glat[-1,:]
               elif i==3:
                   longitude=glon[:,-1]
                   latitude=glat[:,-1]
           #Convert latitude and longitude to coordinates X and Y
	       x, y = m(longitude, latitude)
	       if region_line==True:
			plt.scatter(x[::5],y[::5],lw=1,s=2, c=region_col,edgecolor=region_col,zorder=1)
	       else:
    	       		plt.scatter(x,y,lw=1,s=2, c=region_col,edgecolor=region_col,zorder=1)
    plt.tight_layout()
    plt.title("weather@home Regions")
    fig.savefig("region_plot.png")

#Main controling function
def main():
    map_plot()
    print 'Finished!'

#Washerboard function that allows main() to run on running this file
if __name__=="__main__":
  main()
