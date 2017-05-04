###########################################################################
# Program:  region_map_anim.py
# Author:   Sarah Sparrow
# Date:     03/01/2017
# Purpose:  To plot jpgs for weather@home region animation
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
    for iframe in range(0,360):
	fig = plt.figure()
	fig.set_size_inches(3,3)
        m = Basemap(projection='geos',lon_0=iframe,resolution='c')
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
                       lon1=np.repeat(lon[0],lat.shape)
		       lat1=lat[:]
                   elif i==1:
                       lon1=lon[:]
                       lat1=np.repeat(lat[0],lon.shape)
                   elif i==2:
                       lon1=np.repeat(lon[-1],lat.shape)
                       lat1=lat[:]
                   elif i==3:
                       lon1=lon[:]
                       lat1=np.repeat(lat[-1],lon.shape)
		   x, y = m(lon1, lat1)
		   if region_line==True:
                       m.scatter(x[::5],y[::5],lw=1,s=2, c=region_col,edgecolor=region_col,zorder=1)
                   else:
                       m.scatter(x,y,lw=1,s=2, c=region_col,edgecolor=region_col,zorder=1) 
	    else:
                glat,glon=get_rot_global_coords(region_file)
                for i in range(0,4):
    	           if i==0:
	               lon1=glon[0,:]
	               lat1=glat[0,:]
	           elif i==1:
	               lon1=glon[:,0]
                       lat1=glat[:,0]
                   elif i==2:
	               lon1=glon[-1,:]
                       lat1=glat[-1,:]
                   elif i==3:
                       lon1=glon[:,-1]
                       lat1=glat[:,-1]
           #Convert latitude and longitude to coordinates X and Y
		   x, y = m(lon1, lat1)
		   if region_line==True:
                       m.scatter(x[::5],y[::5],lw=1,s=2, c=region_col,edgecolor=region_col,zorder=1)
                   else:
                       m.scatter(x,y,lw=1,s=2, c=region_col,edgecolor=region_col,zorder=1)  	

	plt.tight_layout()
        print iframe, 360-iframe
    	if 360-iframe<10:
    	    fig.savefig("anim_jpgs/globe_plot_00"+str(360-iframe)+".jpg")
        elif 360-iframe<100:
            fig.savefig("anim_jpgs/globe_plot_0"+str(360-iframe)+".jpg")
        else:
            fig.savefig("anim_jpgs/globe_plot_"+str(360-iframe)+".jpg")
#Main controling function
def main():
    map_plot()
    print 'Now combine jpg files into an animated gif using:'
    print 'convert -loop 0 *.jpg regions_globe.gif'
    print 'Or create an mp4 file using:'
    print 'ffmpeg -framerate 10 -i globe_plot_%03d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p wah_regions.mp4'
    print 'Finished!'

#Washerboard function that allows main() to run on running this file
if __name__=="__main__":
  main()
