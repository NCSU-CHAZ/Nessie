import numpy as np 
from scipy.interpolate import interp1d
import pandas as pd
import datetime as dt
from read_HydroSurveyor import create_df
from math import floor
import matplotlib.pyplot as plt

""" Important Keys in AutoData
    ---'HydroSurveyor_WaterVelocityXyz_Corrected_m_s'
    ---'HydroSurveyor_WaterVelocityXyz_Corrected_DateTime'
    ---'HydroSurveyor_BottomTrack_m_s'
    ---'HydroSurveyor_BottomTrack_DateTime'
"""

def nanhelp(y):
    """ Helper function to help determine indices of nan values, this is helpful for interpolation
    y: 1d numpy array containing nan values
    
    nans: logical indices of nans
    ids: indices of nan values
    """
    nans = np.isnan(y)
    return nans, lambda z: z.nonzero()[0]

def freq_interp(SizeLike, values, timeseries):
    interp_array = []
    nanlocs, x = nanhelp(values); del x
    whichlocs = np.squeeze(timeseries)                # whichlocs represents x and values represents f(x)
    f = interp1d(whichlocs[~nanlocs], values[~nanlocs], bounds_error=False, fill_value=np.nan)
    interp_array = f(SizeLike)
    return interp_array

def dtnum_dttime(time_array) :
         dates = []
         DT = time_array.to_numpy()
         DT = DT/(1*10**6)/(86400) #Convert from microseconds 
         for ordinal in DT :
                 integer = floor(ordinal[0])
                 frac = ordinal - integer
                 date = dt.datetime.fromordinal(integer)
                 time = dt.timedelta(days=frac[0])
                 mat_correction = dt.timedelta(days=366)
                 full = date + time - mat_correction
                 dates.append(full)
         return dates

def Hydro_session_process(filepath) :
    AutoData, Info = create_df(filepath)

    BtInterpedE = freq_interp(AutoData['HydroSurveyor_WaterVelocityXyz_Corrected_DateTime'],AutoData['HydroSurveyor_BottomTrack_m_s'].iloc[:,0],AutoData['HydroSurveyor_BottomTrack_DateTime'])
    BtInterpedN = freq_interp(AutoData['HydroSurveyor_WaterVelocityXyz_Corrected_DateTime'],AutoData['HydroSurveyor_BottomTrack_m_s'].iloc[:,1],AutoData['HydroSurveyor_BottomTrack_DateTime'])
    BtInterpedU= freq_interp(AutoData['HydroSurveyor_WaterVelocityXyz_Corrected_DateTime'],AutoData['HydroSurveyor_BottomTrack_m_s'].iloc[:,2],AutoData['HydroSurveyor_BottomTrack_DateTime'])

    EastVel = AutoData['HydroSurveyor_WaterVelocityXyz_Corrected_m_s'].iloc[:,0::4].subtract(BtInterpedE,axis=0)
    NorthVel = AutoData['HydroSurveyor_WaterVelocityXyz_Corrected_m_s'].iloc[:,1::4].subtract(BtInterpedN,axis=0)
    VertVel = AutoData['HydroSurveyor_WaterVelocityXyz_Corrected_m_s'].iloc[:,2::4].subtract(BtInterpedU,axis=0)
    BtVel = AutoData['HydroSurveyor_BottomTrack_m_s']

    #Remove Data below vertical beam range
    dim = EastVel.shape 
    mask = np.tile(rawdata['VbDepth_m'],(1, dim[1]))
    isbad = (CellGrid > mask)

    EastVel[isbad] = float('NaN')
    NorthVel[isbad] = float('NaN')
    VertVel[isbad] = float('NaN')

    EastVel_interp, interpCellDepth = cellsize_interp(EastVel,rawdata['CellSize_m'],CellGrid,2)
    NorthVel_interp, interpCellDepth = cellsize_interp(NorthVel,rawdata['CellSize_m'],CellGrid,2)
    VertVel_interp, interpCellDepth = cellsize_interp(VertVel,rawdata['CellSize_m'],CellGrid,2)

    dates = dtnum_dttime(AutoData['HydroSurveyor_WaterVelocityXyz_Corrected_DateTime'])

    Data = {'EastVel_interp':EastVel_interp, 'NorthVel_interp':NorthVel_interp, 'VertVel_interp':VertVel_interp, 'interpCellDepth':interpCellDepth, 
            'EastVel':EastVel, 'NorthVel':NorthVel, 'VertVel':VertVel, 'BtVel':BtVel, 'DateNum':AutoData['HydroSurveyor_WaterVelocityXyz_Corrected_DateTime'],'DateTime':dates, 'Info':Info}
    return Data 