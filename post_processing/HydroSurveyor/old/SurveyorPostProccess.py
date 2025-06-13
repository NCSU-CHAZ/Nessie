import numpy as np
from scipy.io import loadmat
from scipy.interpolate import interp1d
import pandas as pd
import datetime as dt
import math
import matplotlib.pyplot as plt


def nanhelp(y):
    """Helper function to help determine indices of nan values, this is helpful for interpolation
    y: 1d numpy array containing nan values

    nans: logical indices of nans
    ids: indices of nan values
    """
    nans = np.isnan(y)
    return nans, lambda z: z.nonzero()[0]


# Import .mat files
def readin(filepath):
    rawdata = loadmat(filepath)
    del rawdata["__header__"]
    del rawdata["__version__"]
    del rawdata["__globals__"]
    # Delete unnecessary keys
    data = {}
    for i in rawdata.keys():
        array = rawdata[i]
        if rawdata[i].ndim == 3:  # Flatten 3d arrays into 2d arrays
            reshaped = array.reshape(array.shape[0], -1)
            data[i] = pd.DataFrame(reshaped)
        elif i == "Info":
            Info = rawdata[i]
        else:
            data[i] = pd.DataFrame(array)
    return data, Info


rawdata, Info = readin(
    r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Survey_ICW_20240520_raw.mat"
)

# Acquire individual direction dataframes
WaterEastVel = rawdata["WaterVelEnu_m_s"].iloc[:, 0::4]  # 3557x#340 matrix
WaterNorthVel = rawdata["WaterVelEnu_m_s"].iloc[:, 1::4]
WaterVertVel = rawdata["WaterVelEnu_m_s"].iloc[:, 2::4]
WaterErrVel = rawdata["WaterVelEnu_m_s"].iloc[:, 3::4]

# Reinsert Datetime vectors back in to dataframes
# WaterEastVel.insert(0, 'DateTime', rawdata['DateTime'])
# WaterNorthVel.insert(0, 'DateTime', rawdata['DateTime'])
# WaterVertVel.insert(0, 'DateTime', rawdata['DateTime'])

# Correct by subtracting bottom track velocities, these are not the same length so be sure to revisit
EastVel = WaterEastVel.subtract(rawdata["BtVelEnu_m_s"].iloc[:, 0], axis=0)
NorthVel = WaterNorthVel.subtract(rawdata["BtVelEnu_m_s"].iloc[:, 1], axis=0)
VertVel = WaterVertVel.subtract(rawdata["BtVelEnu_m_s"].iloc[:, 2], axis=0)
ErrVel = np.sqrt(
    1 / (1 / (WaterErrVel**2) + (1 / (rawdata["BtVelEnu_m_s"].iloc[:, 3] ** 2)))
)  # This might not be the best way to perserve error values


# Report Error don't worry so much in compounding them

# Correct for vertical beam ranges
cellnum = np.arange(0, WaterEastVel.shape[1])
CellGrid = np.outer(cellnum, rawdata["CellSize_m"])
CellGrid = np.add(rawdata["CellStart_m"].to_numpy(), (CellGrid.swapaxes(0, 1)))
CellGrid = CellGrid + 0.1651

# Remove Data below vertical beam range
dim = WaterEastVel.shape
mask = np.tile(rawdata["VbDepth_m"], (1, dim[1]))
isbad = CellGrid > mask

EastVel[isbad] = np.nan
NorthVel[isbad] = np.nan
VertVel[isbad] = np.nan


def cellsize_interp(vel_array, CellSize_m, CellGrid, Interpsize):

    # vel_array = Velocity array, size [Number of sample points]x[number of cells multiplied by four] four beams per cell
    # CellSize_m = Vector telling the depth of the cells for each data measurement as HydroSurveyor changes cellsize depending on depth
    # CellGrid = Matrix of cell depths, same size as vel_array
    # Interpsize = This number decides which cell size to interpolate to i.e. if you have 6 cell sizes [.05 .1 .3 .5 .65 2] you
    #             pick which cell size to interpolate to.

    # Determine dimensions and unique cell sizes
    dimension = CellGrid.shape[1]
    varCellSize = np.unique(CellSize_m)
    targetCellSize = varCellSize[
        Interpsize - 1
    ]  # Pick out the cell size you interpolate to (-1 because of python indexing)
    varCellSize = np.delete(
        varCellSize, Interpsize - 1
    )  # Remove the target cell size from the variables list
    cellinds = np.where(CellSize_m == targetCellSize)[
        0
    ]  # Indexes for which data points where measured at the target cell size
    interpCellDepth = CellGrid[
        cellinds[0], :
    ]  # Acquires the cells from the grid that used the targeted cell size

    # Initialize the interpolated velocity array

    vel_interp = np.copy(vel_array)
    # Perform interpolation

    # Perform interpolation
    for jj in varCellSize:
        inds = np.where(CellSize_m == jj)[
            0
        ]  # Get the indices for which data points are at one of the cell sizes
        for i in inds:
            value = vel_interp[i, :]  # Gets the velocity points in the row
            loc, x = nanhelp(value)
            if np.any(~loc):
                f = interp1d(
                    x(~loc), value[~loc], bounds_error=False, fill_value=np.nan
                )
                vel_interp[i, :] = f(np.arange(len(value)))

    return vel_interp, interpCellDepth


# EastVel_interp, interpCellDepth = cellsize_interp(EastVel,rawdata['CellSize_m'],CellGrid,1)
# NorthVel_interp, interpCellDepth = cellsize_interp(NorthVel,rawdata['CellSize_m'],CellGrid,2)
# VertVel_interp, interpCellDepth = cellsize_interp(VertVel,rawdata['CellSize_m'],CellGrid,2)
from math import floor


def dtnum_dttime(time_array):
    dates = []
    DT = time_array.to_numpy()
    DT = (
        DT / (1 * 10**6) / (86400) + 730486
    )  # Convert fron hydrosurveyor time which is microseconds since Jan 01 2000 (or in datenum 730486)
    for ordinal in DT:
        integer = floor(ordinal[0])
        frac = ordinal - integer
        date = dt.datetime.fromordinal(integer)
        time = dt.timedelta(days=frac[0])
        mat_correction = dt.timedelta(days=366)
        full = date + time - mat_correction
        dates.append(full)
    return dates


# print(rawdata.keys())

# qcVel = qc_check(Vel_East, ,rawdata['Frequency'],)


varCellSize = np.unique(rawdata["CellSize_m"])
varCellSize = np.delete(varCellSize, 0)
targetCellSize = varCellSize[
    2 - 1
]  # Pick out the cell size you interpolate to (-1 because of python indexing)
varCellSize = np.delete(
    varCellSize, 2 - 1
)  # Remove the target cell size from the variables list
cellinds = np.where(rawdata["CellSize_m"] == targetCellSize)[
    0
]  # Indexes for which data points where measured at the target cell size
interpCellDepth = CellGrid[cellinds[0], :]

vel_interp = np.copy(EastVel)
# Perform interpolation

# Perform interpolation
for jj in varCellSize:
    inds = np.where(rawdata["CellSize_m"] == jj)[
        0
    ]  # Get the indices for which data points are at one of the cell sizes
    for i in inds:
        value = vel_interp[i, :]  # Gets the velocity points in the row
        whichlocs = CellGrid[i, :]
        nanloc, x = nanhelp(value)
        if np.any(~nanloc):
            f = interp1d(
                whichlocs[~nanloc],
                value[~nanloc],
                bounds_error=False,
                fill_value=np.nan,
            )
            vel_interp[i, :] = f(interpCellDepth)

DateTime = dtnum_dttime(rawdata["DateTime"])

print(rawdata.keys())
