import numpy as np 
from scipy.io import loadmat
import pandas as pd
import datetime as time
import pytest
import matplotlib.pyplot as plt

#Import .mat files 
def readin(filepath) :
        rawdata = loadmat(filepath)
        del rawdata['__header__'] ; del rawdata['__version__'] ; del rawdata['__globals__']; #Delete unnecessary keys
        data = {}
        for i in rawdata.keys() :
                array = rawdata[i]
                if rawdata[i].ndim == 3 :      #Flatten 3d arrays into 2d arrays
                        reshaped = array.reshape(array.shape[0],-1)   
                        data[i] = pd.DataFrame(reshaped)
                elif i == 'Info':
                        Info = rawdata[i]
                else :
                        data[i] = pd.DataFrame(array)
        return data , Info


rawdata, Info = readin(r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Survey_ICW_20240520_raw.mat")

#Acquire individual direction dataframes
WaterEastVel = rawdata['WaterVelEnu_m_s'].iloc[:, 0::4] # 3557x#340 matrix 
WaterNorthVel = rawdata['WaterVelEnu_m_s'].iloc[:,1::4] 
WaterVertVel = rawdata['WaterVelEnu_m_s'].iloc[:, 2::4] 
WaterErrVel = rawdata['WaterVelEnu_m_s'].iloc[:, 3::4] 

#Reinsert Datetime vectors back in to dataframes
# WaterEastVel.insert(0, 'DateTime', rawdata['DateTime']) 
# WaterNorthVel.insert(0, 'DateTime', rawdata['DateTime']) 
# WaterVertVel.insert(0, 'DateTime', rawdata['DateTime']) 

#Correct by subtracting bottom track velocities, these are not the same length so be sure to revisit 
EastVel = WaterEastVel.subtract(rawdata['BtVelEnu_m_s'].iloc[:, 0],axis=0)
NorthVel = WaterNorthVel.subtract(rawdata['BtVelEnu_m_s'].iloc[:, 1],axis=0)
VertVel = WaterVertVel.subtract(rawdata['BtVelEnu_m_s'].iloc[:, 2],axis=0)
ErrVel = np.sqrt(1/(1/(WaterErrVel**2) + (1/(rawdata['BtVelEnu_m_s'].iloc[:, 3]**2)))) #This might not be the best way to perserve error values

# Report Error don't worry so much in compounding them 

#Correct for vertical beam ranges
cellnum = np.linspace(0,len(rawdata['CellSize_m']),(len(rawdata['CellSize_m'])))
CellGrid = (rawdata['CellStart_m'] + (cellnum.reshape(3577,1)*rawdata['CellSize_m']))
CellGrid = CellGrid + .1651 

#Remove Data below vertical beam range
print(CellGrid.astype)
dim = WaterEastVel.shape 
mask = np.tile(rawdata['VbDepth_m'],dim[1])
isbad = (CellGrid > mask)

EastVel[isbad] = float('nan')
NorthVel[isbad] = float('nan')
VertVel[isbad] = float('nan')
ErrVel[isbad] = float('nan')

