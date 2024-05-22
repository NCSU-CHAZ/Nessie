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
                if rawdata[i].ndim == 3 :      #Flatten 3d arrays into 2d arrays, this causes 
                        reshaped = array.reshape(array.shape[0],-1)   
                        data[i] = pd.DataFrame(reshaped)
                elif i == 'Info':              #The info structure does not translate well but contains relevant data
                        Info = rawdata[i]
                else :
                        data[i] = pd.DataFrame(array)
        return data , Info

def mat_readin(filepath) :
        data, Info = readin(filepath)
        #Acquire individual direction dataframes
        WaterEastVel = data['WaterVelEnu_m_s'].iloc[:, 0::4] #3557x340 matrix gets sorted for every fourth column 
        WaterNorthVel = data['WaterVelEnu_m_s'].iloc[:,1::4] 
        WaterVertVel = data['WaterVelEnu_m_s'].iloc[:, 2::4] 
        WaterErrVel = data['WaterVelEnu_m_s'].iloc[:, 3::4] 
        rawdata = data
        return rawdata, WaterEastVel, WaterNorthVel, WaterVertVel, WaterErrVel
