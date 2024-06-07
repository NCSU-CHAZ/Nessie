import numpy as np
from scipy.interpolate import interp1d
import pandas as pd
import datetime as dt
from read_HydroSurveyor import create_df
from math import floor

""" Important Keys in AutoData(There are more)
    ---'HydroSurveyor_WaterVelocityXyz_Corrected_m_s'
    ---'HydroSurveyor_WaterVelocityXyz_Corrected_DateTime'
    ---'HydroSurveyor_BottomTrack_m_s'
    ---'HydroSurveyor_BottomTrack_DateTime'
    ---'HydroSurveyor_VerticalBeamRange_Corrected_m'
    ---'HydroSurveyor_VerticalBeamSnr_dB'
    ---'HydroSurveyor_MagneticHeading_deg'
    ---'Boat_Heading_deg'
    ---'HydroSurveyor_WaterSpeed_Corrected_m_s'
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
        mat_correction = dt.timedelta(days=366)
        full = date + time - mat_correction
        dates.append(full)
    return dates, DT


def Hydro_session_qc(VelArray, Snr, Fs, SnrThresh):
    # CorrThresh = .3 +.4*((Fs/25)**.5) #Minimum correlation threshold used in Elgar 2001
    Snr
    return

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

    # Correct the velocites for bottomtrack motion

    XVel = AutoData["HydroSurveyor_WaterVelocityXyz_Corrected_m_s"].iloc[:, 0::4].T
    YVel = AutoData["HydroSurveyor_WaterVelocityXyz_Corrected_m_s"].iloc[:, 1::4].T
    ZVel = AutoData["HydroSurveyor_WaterVelocityXyz_Corrected_m_s"].iloc[:, 2::4].T
    BtVelXyz = AutoData["HydroSurveyor_BottomTrack_m_s"]

    XVel.reset_index(drop=True, inplace=True)
    YVel.reset_index(drop=True, inplace=True)
    ZVel.reset_index(drop=True, inplace=True)

    heading_rad = np.deg2rad(AutoData["HydroSurveyor_MagneticHeading_deg"] - 180)
    heading_rad = heading_rad.values.reshape(-1, 1)

    EastVel = XVel * np.sin(heading_rad) - YVel * np.cos(heading_rad)
    NorthVel = XVel * np.cos(heading_rad) + YVel * np.sin(heading_rad)
    VertVel = ZVel

    EastVel = EastVel.subtract(BtInterpedE, axis=0)
    NorthVel = NorthVel.subtract(BtInterpedN, axis=0)
    VertVel = VertVel.subtract(BtInterpedU, axis=0)

    #Create Mask that cuts off all measurements below the ocean floor
    #This is done by taking the spike in SnR that occurs when the signal gets to the floor
    Beam1 = AutoData['HydroSurveyor_AdpSnr_dB'].iloc[:, 0::4]
    Beam1.reset_index(drop=True, inplace=True)
    Beam2 = AutoData['HydroSurveyor_AdpSnr_dB'].iloc[:, 1::4]
    Beam2.reset_index(drop=True, inplace=True)
    Beam3 = AutoData['HydroSurveyor_AdpSnr_dB'].iloc[:, 2::4]
    Beam3.reset_index(drop=True, inplace=True)
    Beam4 = AutoData['HydroSurveyor_AdpSnr_dB'].iloc[:, 3::4]
    Beam4.reset_index(drop=True, inplace=True)
    Beams = [Beam1, Beam2,Beam3,Beam4]

    Cutoffs = []
    for WhichBeam in Beams :
        for gg in np.arange(0,np.shape(WhichBeam)[1]) :
            Vals = WhichBeam.iloc[:,gg]   
            nanids, x = nanhelp(Vals)
            floorid = np.argmax(Vals[~nanids])
            Cutoffs.append(floorid)
    print(Cutoffs)

    dates, DT = dtnum_dttime(
        AutoData["HydroSurveyor_WaterVelocityXyz_Corrected_DateTime"]
    )
    
    Fs = np.diff(1 / (DT * 86400))

    #EastVel = Hydro_session_qc(EastVel,AutoData['HydroSurveyor_AdpSnr_dB'],Fs,8)

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
        "ADP_snr": AutoData['HydroSurveyor_AdpSnr_dB'],
        "VertBeam_snr":AutoData["HydroSurveyor_VerticalBeamSnr_dB"],
        "VertDepth":AutoData['HydroSurveyor_VerticalBeamRange_Corrected_m'],
        "UncorrectedVel": AutoData["HydroSurveyor_WaterVelocityXyz_Corrected_m_s"],
    }
    return Data


