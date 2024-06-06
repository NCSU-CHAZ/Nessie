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
    """Helper function to help determine indices of nan values, this is helpful for interpolation
    y: 1d numpy array containing nan values

    nans: logical indices of nans
    ids: indices of nan values
    """
    nans = np.isnan(y)
    return nans, lambda z: z.nonzero()[0]


def freq_interp(SizeLike, values, timeseries):
    interp_array = []
    nanlocs, x = nanhelp(values)
    del x
    whichlocs = np.squeeze(
        timeseries
    )  # whichlocs represents x and values represents f(x)
    f = interp1d(
        whichlocs[~nanlocs], values[~nanlocs], bounds_error=False, fill_value=np.nan
    )
    interp_array = f(SizeLike)
    return interp_array


def dtnum_dttime(time_array):
    dates = []
    DT = time_array.to_numpy()
    DT = DT / (1 * 10**6) / (86400)  # Convert from microseconds
    for ordinal in DT:
        integer = floor(ordinal[0])
        frac = ordinal - integer
        date = dt.datetime.fromordinal(integer)
        time = dt.timedelta(days=frac[0])
        mat_correction = dt.timedelta(days=366)
        full = date + time - mat_correction
        dates.append(full)
    return dates


def Hydro_session_process(filepath):
    AutoData, Info = create_df(filepath)

    BtInterpedE = freq_interp(
        AutoData["HydroSurveyor_WaterVelocityXyz_Corrected_DateTime"],
        AutoData["HydroSurveyor_BottomTrack_m_s"].iloc[:, 0],
        AutoData["HydroSurveyor_BottomTrack_DateTime"],
    )
    BtInterpedN = freq_interp(
        AutoData["HydroSurveyor_WaterVelocityXyz_Corrected_DateTime"],
        AutoData["HydroSurveyor_BottomTrack_m_s"].iloc[:, 1],
        AutoData["HydroSurveyor_BottomTrack_DateTime"],
    )
    BtInterpedU = freq_interp(
        AutoData["HydroSurveyor_WaterVelocityXyz_Corrected_DateTime"],
        AutoData["HydroSurveyor_BottomTrack_m_s"].iloc[:, 2],
        AutoData["HydroSurveyor_BottomTrack_DateTime"],
    )

    XVel = (
        AutoData["HydroSurveyor_WaterVelocityXyz_Corrected_m_s"]
        .iloc[:, 0::4]
        .T.subtract(BtInterpedE, axis=0)
    )
    YVel = (
        AutoData["HydroSurveyor_WaterVelocityXyz_Corrected_m_s"]
        .iloc[:, 1::4]
        .T.subtract(BtInterpedN, axis=0)
    )
    ZVel = (
        AutoData["HydroSurveyor_WaterVelocityXyz_Corrected_m_s"]
        .iloc[:, 2::4]
        .T.subtract(BtInterpedU, axis=0)
    )
    BtVelXyz = AutoData["HydroSurveyor_BottomTrack_m_s"]

    XVel.reset_index(drop=True, inplace=True)
    YVel.reset_index(drop=True, inplace=True)
    ZVel.reset_index(drop=True, inplace=True)

    heading_rad = np.deg2rad(AutoData["HydroSurveyor_MagneticHeading_deg"] - 180)
    heading_rad = heading_rad.values.reshape(-1, 1)

    EastVel = XVel * np.sin(heading_rad)
    NorthVel = XVel * np.cos(heading_rad)
    VertVel = ZVel

    dates = dtnum_dttime(AutoData["HydroSurveyor_WaterVelocityXyz_Corrected_DateTime"])

    Data = {
        "EastVel": EastVel,
        "NorthVel": NorthVel,
        "VertVel": VertVel,
        "BtVel": BtVelXyz,
        "DateNum": AutoData["HydroSurveyor_WaterVelocityXyz_Corrected_DateTime"],
        "DateTime": dates,
        "Info": Info,
        "XVel": XVel,
        "YVel": YVel,
        "ZVel": ZVel,
        "UncorrectedVel": AutoData["HydroSurveyor_WaterVelocityXyz_Corrected_m_s"],
    }
    return Data


# AutoData['HydroSurveyor_MagneticHeading_deg']
# AutoData['Boat_Heading_deg']
