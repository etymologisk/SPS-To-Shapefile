#Get the tools required
import glob
import pandas as pd
import matplotlib.pyplot as plt
import time

from geopandas import GeoDataFrame
from shapely.geometry import Point
from shapely.geometry import LineString

print(time.asctime())
#Grab filenames
sps_files = glob.glob("S_inputs/*.s01")
rps_files = glob.glob("R_inputs/*.r01")


#Set column widths
colspecs=[[0,9], [14,21], [23,27], [31,34], [37,38], [41,46], [47,55],[55,65], [68,71], [71,87]]
names=['Line Number', 'Shot Number', 'Attempt', 'Gun Depth', 'Num', 'Depth', 'Easting', 'Northing', 'Geodetic Height', 'Time']


#Create a dataframe for the SPS
all_sps = pd.DataFrame()

for i in sps_files:
    df = pd.read_fwf(i,colspecs=colspecs,names=names)
    
    df = df.loc[df["Line Number"].str.startswith("S")]
    all_sps = all_sps.append(df) 

#Convert E/N/D to numbers    
all_sps["Easting"] = pd.to_numeric(all_sps["Easting"])
all_sps["Northing"] = pd.to_numeric(all_sps["Northing"])
all_sps["Depth"] = pd.to_numeric(all_sps["Depth"])


#Check
all_sps.head()


#Set column widths for RPS
colspecs=[[0,14], [21,26], [46,55], [55,66]]
names=['Line Number', 'GS Number', 'Easting', 'Northing']


#Create a dataframe for the RPS
all_rps = pd.DataFrame()

for i in rps_files:
    df = pd.read_fwf(i,colspecs=colspecs,names=names)
    
    df = df.loc[df["Line Number"].str.startswith("R")]
    all_rps = all_rps.append(df) 

	
#Convert E/N to numbers 
all_rps["Easting"] = pd.to_numeric(all_rps["Easting"])
all_rps["Northing"] = pd.to_numeric(all_rps["Northing"])


#Check
all_rps.head()


#Create geometries for sps
geometry = [Point(xy) for xy in zip(all_sps.Easting, all_sps.Northing)]
crs = {'init': 'epsg:23031'}


#Create points for sps
all_sps_points = GeoDataFrame(all_sps, crs=crs, geometry=geometry)


#Create lines for sps
all_sps_lines = all_sps_points.groupby(['Line Number'])['geometry'].apply(lambda x: LineString(x.tolist()))
all_sps_lines = GeoDataFrame(all_sps_lines, geometry='geometry')


#Check
all_sps_points.head()
all_sps_lines.head()


#Create shapefiles for sps
all_sps_points.to_file(driver = 'ESRI Shapefile', filename= "result_SPS_points.shp")
all_sps_lines.to_file(driver = 'ESRI Shapefile', filename= "result_SPS_lines.shp")


#Create geometries for rps
geometry = [Point(xy) for xy in zip(all_rps.Easting, all_rps.Northing)]
crs = {'init': 'epsg:23031'}

#Create points for rps
all_rps_points = GeoDataFrame(all_rps, crs=crs, geometry=geometry)

#Create lines for rps
all_rps_lines = all_rps_points.groupby(['Line Number'])['geometry'].apply(lambda x: LineString(x.tolist()))
all_rps_lines = GeoDataFrame(all_rps_lines, geometry='geometry')

#Check
all_rps_points.head()
all_rps_lines.head()


#Create shapefiles for rps
all_rps_points.to_file(driver = 'ESRI Shapefile', filename= "result_RPS_points.shp")
all_rps_lines.to_file(driver = 'ESRI Shapefile', filename= "result_RPS_lines.shp")

print(time.asctime())
