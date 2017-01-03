# cpdn_regions

The purpose of this code is to plot CPDN region boundaries on a map and animation

To add a new region:

1. Add a new region to the regions dictionary specifying the region colour and whether it is to be displayed as a dotted line
2. Add an example regional output netcdf file to the data directory using the filename convention:
      
      {region_abbreviation}_region.nc

**For animations:**

Converting jpg files to animated gif

convert -loop 0 *.jpg regions_globe.gif

Convertion jpg files to mp4 file

ffmpeg -framerate 10 -i globe_plot_%03d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p wah_regions.mp4

