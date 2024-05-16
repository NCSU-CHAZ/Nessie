import numpy as np 
import scipy as sp
import pandas as pd
import datetime as time

velpath = r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\M9Hydro_csvData\M9_HydroSurveyor - WaterVelocityXyz_m_s.csv" 
        # r in front of the filepath lets PYTHON know the string is raw, this means it will interpret the \ literally
data = pd.read_csv(velpath, header=0)   #Pandas library reads in data, identifies first row as column titles i.e. Header
WaterVelXYZ = pd.DataFrame(data)   # m/s                   

# Pandas converts data into workable datastructure with the headers as 
# [Date/Time, Cell1_HydroSurveyor - WaterVelocityXyz_1, Cell1_HydroSurveyor - WaterVelocityXyz_2, Cell1_HydroSurveyor - WaterVelocityXyz_3,
#  Cell1_HydroSurveyor - WaterVelocityXyz_4,  Cell2_HydroSurveyor - WaterVelocityXyz_1 ... Cell85_HydroSurveyor - WaterVelocityxyz_4]  
# This can be viewed with print(velXYZ.keys())
# It is my current understanding that for each cell WaterVelocityXyz_1 is east,  WaterVelocityXyz_2 is North
# WaterVelocityXyz_3 is vertical,  WaterVelocityXyz_4 is error

pd.to_datetime(WaterVelXYZ["Date/Time"], format='%Y-%m-%d %H:%M:%S.%f') #Converts the string of date times into datetime objects

trackpath = r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\M9Hydro_csvData\M9_HydroSurveyor - BottomTrack_m_s.csv"
btTrackXYZ = pd.DataFrame(pd.read_csv(trackpath,header=0)) # Headers are [Date/Time, HydroSurveyor - BottomTrack_1, ..., HydroSurveyor - BottomTrack_4]
pd.to_datetime(btTrackXYZ["Date/Time"], format='%Y-%m-%d %H:%M:%S.%f')

#Acquire individual direction dataframes
WaterEastVel = WaterVelXYZ[WaterVelXYZ.columns[1::4]] 
WaterNorthVel = WaterVelXYZ[WaterVelXYZ.columns[2::4]]
WaterVertVel = WaterVelXYZ[WaterVelXYZ.columns[3::4]]
WaterErrVel = WaterVelXYZ[WaterVelXYZ.columns[::4]]

#Reinsert Datetime vectors back in to dataframes
WaterEastVel.insert(0, 'Date/Time', WaterVelXYZ['Date/Time']) 
WaterNorthVel.insert(0, 'Date/Time', WaterVelXYZ['Date/Time']) 
WaterVertVel.insert(0, 'Date/Time', WaterVelXYZ['Date/Time']) 

#Correct by subtracting bottom track velocities, these are not the same length so be sure to revisit 
EastVel = WaterEastVel - btTrackXYZ['HydroSurveyor - BottomTrack_1']
NorthVel = WaterNorthVel - btTrackXYZ['HydroSurveyor - BottomTrack_2']
VertVel = WaterVertVel -  btTrackXYZ['HydroSurveyor - BottomTrack_3']
ErrVel = WaterErrVel - btTrackXYZ['HydroSurveyor - BottomTrack_4']

