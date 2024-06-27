from read_Sig1k import read_Sig1k
from math import floor
import datetime as dt
import numpy as np


def dtnum_dttime_adcp(
    time_array,
):  # Create a function to convert from matlabs datenum format to python datetime
    dates = []  # Initialize dates#Convert the awkward structure intoa matlab array
    DT = time_array.to_numpy()  # Dataframes behave strangely for some reason
    for ordinal in DT:
        integer = floor(
            ordinal[0]
        )  # Round down to the nearest whole number on the datetime
        frac = ordinal - integer  # Get just the decimal points
        date = dt.datetime.fromordinal(
            integer
        )  # This function only takes integer values so we must add the decimal on after the conversion
        time = dt.timedelta(
            days=frac[0]
        )  # Convert the decimals into hours, min, seconds, microseconds, ect.
        mat_correction = dt.timedelta(
            days=366
        )  # Matlab datenum starts from Jan 1 0000AD, this year is 366 days long,
        # while ordinal time which is what we are converting from starts Jan 1 0001AD
        full = (
            date + time - mat_correction
        )  # Recombine the fractional precision and correct fro the year difference between ordinal and dateum
        dates.append(full)  # Append the correct datetime back into the dates array
    return dates
    """This entire loop is very inefficient, while take time for large data sets
                     but this is the best I have figured out at the time of creating this"""


def process(filepath):
    Data, T = read_Sig1k(filepath)  # Load in file

    Data["IBurst_Time"] = dtnum_dttime_adcp(Data["IBurst_Time"])
    Data["Burst_Time"] = dtnum_dttime_adcp(Data["Burst_Time"])
    Data["BurstRawAltimeter_Time"] = dtnum_dttime_adcp(Data["BurstRawAltimeter_Time"])
    Data["Echo1Bin1_1000kHz_Time"] = dtnum_dttime_adcp(Data["Echo1Bin1_1000kHz_Time"])
    Data["Echo2Bin1_1000kHz_Time"] = dtnum_dttime_adcp(Data["Echo2Bin1_1000kHz_Time"])

    # QC the data based on correlation values based on the info in Elgar 2001
    Sr = 2 #Hz
    CorrThresh = .3 +.4*(Sr/25)**.5

    for i in range(1,5) :
        isbad = Data[f'Burst_CorBeam{i}']*.01 <= CorrThresh
        Data[f'Burst_VelBeam{i}'][isbad] = np.nan
    
    # Convert the data from beam coords to ENU (This is all done according to the steps found here
    # https://support.nortekgroup.com/hc/en-us/articles/360029820971-How-is-a-coordinate-transformation-done


    X = ((Data["Burst_VelBeam1"] - Data["Burst_VelBeam3"]) / 2) + np.sin(25)
    Y = ((Data["Burst_VelBeam2"] - Data["Burst_VelBeam4"]) / 2) + np.sin(25)
    Z1 = ((Data["Burst_VelBeam1"] + Data["Burst_VelBeam3"]) / 2) + np.cos(25)
    Z2 = ((Data["Burst_VelBeam2"] + Data["Burst_VelBeam4"]) / 2) + np.cos(25)

    heading_rad = np.deg2rad(Data["Burst_Heading"])
    EastVel = X * np.sin(heading_rad) - Y * np.cos(heading_rad)
    NorthVel = X * np.cos(heading_rad) + Y * np.sin(heading_rad)
    VertVel1 = Z1
    VertVel2 = Z2

    Data['EastVel'] = EastVel
    Data['NorthVel'] = NorthVel
    Data['VertVel1'] = VertVel1
    Data['VertVel2'] = VertVel2

    return Data


# Data = process(
#     r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\S103080A004_ICW_test.mat"
# )
