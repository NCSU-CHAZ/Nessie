import numpy as np 
from scipy.interpolate import interp1d
import pandas as pd
import datetime as time
from mat_readin import mat_readin

#Function for interpolating cellsize
def cellsize_interp(vel_array, CellSize_m, CellGrid, Interpsize):
    
    #vel_array = Velocity array, size [Number of sample points]x[number of cells multiplied by four] four beams per cell
    #CellSize_m = Vector telling the depth of the cells for each data measurement as HydroSurveyor changes cellsize depending on depth
    #CellGrid = Matrix of cell depths, same size as vel_array
    #Interpsize = This number decides which cell size to interpolate to i.e. if you have 6 cell sizes [.05 .1 .3 .5 .65 2] you
    #             pick which cell size to interpolate to. 

    # Determine dimensions and unique cell sizes
    dimension = CellGrid.shape[1]
    varCellSize = np.unique(CellSize_m)


    targetCellSize = varCellSize[Interpsize - 1] # Pick out the cell size you interpolate to (-1 because of python indexing)
    cellinds = np.where(CellSize_m == targetCellSize)[0] #Indexes for which data points where measured at the target cell size
    interpCellDepth = CellGrid[cellinds[0], :] # Acquires the cells from the grid that used the targeted cell size

    # Initialize the interpolated velocity array
    vel_interp = np.copy(vel_array)

    # Perform interpolation
    for jj in varCellSize:
        inds = np.where(CellSize_m == jj)[0] #Get the indexes for which datapoints are at one of the cellsizes
        for i in inds:
            loc = CellGrid[i, :] #Gets the depth row of data points 
            value = vel_interp[i, :] #Gets the velocity points in the row
            f = interp1d(loc[:dimension], value, bounds_error=False, fill_value="extrapolate") #Interpolates the depths as a function of velocity
            newval = f(interpCellDepth) #Gets th
            vel_interp[i, :] = newval

    return vel_interp, interpCellDepth

#Main post_processing function
def post_process(filepath) :
    rawdata, WaterEastVel, WaterNorthVel, WaterVertVel, WaterErrVel = mat_readin(filepath)

    EastVel = WaterEastVel.subtract(rawdata['BtVelEnu_m_s'].iloc[:, 0],axis=0)
    NorthVel = WaterNorthVel.subtract(rawdata['BtVelEnu_m_s'].iloc[:, 1],axis=0)
    VertVel = WaterVertVel.subtract(rawdata['BtVelEnu_m_s'].iloc[:, 2],axis=0)

    #Correct for vertical beam ranges
    cellnum = np.linspace(0,len(rawdata['CellSize_m']),(len(rawdata['CellSize_m'])))
    CellGrid = (rawdata['CellStart_m'] + (cellnum.reshape(3577,1)*rawdata['CellSize_m']))
    CellGrid = CellGrid + .1651 

    #Remove Data below vertical beam range
    dim = WaterEastVel.shape 
    CellGrid = np.tile(CellGrid, dim[1])
    mask = np.tile(rawdata['VbDepth_m'],dim[1])
    isbad = (CellGrid > mask)

    EastVel[isbad] = float('nan')
    NorthVel[isbad] = float('nan')
    VertVel[isbad] = float('nan')

    EastVel_interp, interpCellDepth = cellsize_interp(EastVel,rawdata['CellSize_m'],CellGrid,2)
    NorthVel_interp, interpCellDepth = cellsize_interp(NorthVel,rawdata['CellSize_m'],CellGrid,2)
    VertVel_interp, interpCellDepth = cellsize_interp(VertVel,rawdata['CellSize_m'],CellGrid,2)

    EastVel = EastVel_interp
    NorthVel = NorthVel_interp
    VertVel = VertVel_interp

    return EastVel, NorthVel, VertVel, rawdata
