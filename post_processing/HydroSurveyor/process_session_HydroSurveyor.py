import numpy as np
from scipy.interpolate import interp1d
import pandas as pd
import datetime as dt
from .read_HydroSurveyor import create_df
from math import floor
import matplotlib.pyplot as plt

""" Important Keys in AutoData(There are more)
    ---'HydroSurveyor_WaterVelocityXyz_m_s'
    ---'HydroSurveyor_WaterVelocityXyz_DateTime'
    ---'HydroSurveyor_BottomTrack_m_s'
    ---'HydroSurveyor_BottomTrack_DateTime'
    ---'HydroSurveyor_VerticalBeamRange_m'
    ---'HydroSurveyor_VerticalBeamSnr_dB'
    ---'HydroSurveyor_MagneticHeading_deg'
    ---'Boat_Heading_deg'
    ---'HydroSurveyor_WaterSpeed_m_s'
    ---'HydroSurveyor_WaterDirection_Corrected'
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
    DT = DT / (1 * 10**6) / (86400) + 730486  # Convert from microseconds
    for ordinal in DT:
        integer = floor(ordinal[0])
        frac = ordinal - integer
        date = dt.datetime.fromordinal(integer)
        time = dt.timedelta(days=frac[0])
        tos = dt.timedelta(hours=4)
        mat_correction = dt.timedelta(days=366)
        full = date + time - mat_correction - tos
        dates.append(full)
    return dates, DT


def Hydro_session_qc(VelArray, Snr, SnrThresh):
    isbad = Snr <= SnrThresh
    VelArray[isbad] = np.nan
    return VelArray


def Hydro_session_process(filepath):
    AutoData, Info = create_df(filepath)
    
    BtInterpedX = freq_interp(
        AutoData["HydroSurveyor_WaterVelocityXyz_DateTime"],
        AutoData["HydroSurveyor_BottomTrack_m_s"].iloc[:, 0],
        AutoData["HydroSurveyor_BottomTrack_DateTime"],
    )
    BtInterpedY = freq_interp(
        AutoData["HydroSurveyor_WaterVelocityXyz_DateTime"],
        AutoData["HydroSurveyor_BottomTrack_m_s"].iloc[:, 1],
        AutoData["HydroSurveyor_BottomTrack_DateTime"],
    )
    BtInterpedZ = freq_interp(
        AutoData["HydroSurveyor_WaterVelocityXyz_DateTime"],
        AutoData["HydroSurveyor_BottomTrack_m_s"].iloc[:, 2],
        AutoData["HydroSurveyor_BottomTrack_DateTime"],
    )
    # Acquire each velocity array from the larger array and transpose them to align with other arrays
    XVel = AutoData["HydroSurveyor_WaterVelocityXyz_m_s"].iloc[:, 0::4].T
    YVel = AutoData["HydroSurveyor_WaterVelocityXyz_m_s"].iloc[:, 1::4].T
    ZVel = AutoData["HydroSurveyor_WaterVelocityXyz_m_s"].iloc[:, 2::4].T

    # Reset their indexes from [0, 4 ,8, 12] to [0,1,2,3]
    XVel.reset_index(drop=True, inplace=True)
    YVel.reset_index(drop=True, inplace=True)
    ZVel.reset_index(drop=True, inplace=True)
    # Aqcuire the individual beam SnR
    Beam1 = AutoData["HydroSurveyor_AdpSnr_dB"].iloc[:, 0::4]
    Beam1.reset_index(drop=True, inplace=True)
    Beam2 = AutoData["HydroSurveyor_AdpSnr_dB"].iloc[:, 1::4]
    Beam2.reset_index(drop=True, inplace=True)
    Beam3 = AutoData["HydroSurveyor_AdpSnr_dB"].iloc[:, 2::4]
    Beam3.reset_index(drop=True, inplace=True)
    Beam4 = AutoData["HydroSurveyor_AdpSnr_dB"].iloc[:, 3::4]
    Beam4.reset_index(drop=True, inplace=True)

    # QC the velocities based on the signal to noise ratio
    XVel = Hydro_session_qc(XVel, Beam1, 16)
    YVel = Hydro_session_qc(YVel, Beam2, 16)
    ZVel = Hydro_session_qc(ZVel, Beam3, 16)

    # Acquire Vessel HEading and switch from degrres to radians
    heading_rad = np.deg2rad(AutoData["HydroSurveyor_MagneticHeading_deg"])
    heading_rad = heading_rad.values.reshape(-1, 1)

    # Change from XYZ to ENUD
    EastVel = XVel * np.sin(heading_rad) - YVel * np.cos(heading_rad)
    NorthVel = XVel * np.cos(heading_rad) + YVel * np.sin(heading_rad)
    VertVel = ZVel

    Beams = [Beam1, Beam2, Beam3, Beam4]

    # Use the beam signal to noise rations to find which cell detects the bottom and nan everything below
    i = 0
    for WhichBeam in Beams:
        i += 1
        for gg in np.arange(0, np.shape(WhichBeam)[1]):
            Vals = WhichBeam.iloc[:, gg]
            nanids, x = nanhelp(Vals)
            floorid = np.argmax(np.diff(Vals[~nanids]))
            if i == 1:
                EastVel.iloc[gg, floorid:] = np.nan
            if i == 2:
                NorthVel.iloc[gg, floorid:] = np.nan
            if i == 3:
                VertVel.iloc[gg, floorid:] = np.nan

    dates, DT = dtnum_dttime(
        AutoData["HydroSurveyor_WaterVelocityXyz_DateTime"]
    )

    Fs = np.diff(1 / (DT * 86400))

    # EastVel = Hydro_session_qc(EastVel,AutoData['HydroSurveyor_AdpSnr_dB'],Fs,8)

    Data = {
        "EastVel": EastVel,
        "NorthVel": NorthVel,
        "VertVel": VertVel,
        "BtVelX": BtInterpedX,
        "BtVelZ": BtInterpedZ,
        "BtVelY": BtInterpedY,
        "DateNum": AutoData["HydroSurveyor_WaterVelocityXyz_DateTime"],
        "DateTime": dates,
        "Info": Info,
        "XVel": XVel,
        "YVel": YVel,
        "ZVel": ZVel,
        "ADP_snr": Beams,
        "VertBeam_snr": AutoData["HydroSurveyor_VerticalBeamSnr_dB"],
        "VertDepth": AutoData["HydroSurveyor_VerticalBeamRange_m"],
        "UncorrectedVel": AutoData["HydroSurveyor_WaterVelocityXyz_m_s"],
        "HydroSurveyor_MagneticHeading_deg": AutoData[
            "HydroSurveyor_MagneticHeading_deg"
        ],
    }
    return Data
