from read_Sig1k import read_Sig1k
from math import floor
import datetime as dt
import numpy as np
import pandas as pd


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
    Data = read_Sig1k(filepath)  # Load in file

    Data["IBurst_Time"] = dtnum_dttime_adcp(Data["IBurst_Time"])
    Data["Burst_Time"] = dtnum_dttime_adcp(Data["Burst_Time"])
    Data["BurstRawAltimeter_Time"] = dtnum_dttime_adcp(Data["BurstRawAltimeter_Time"])
    Data["Echo1Bin1_1000kHz_Time"] = dtnum_dttime_adcp(Data["Echo1Bin1_1000kHz_Time"])
    Data["Echo2Bin1_1000kHz_Time"] = dtnum_dttime_adcp(Data["Echo2Bin1_1000kHz_Time"])

    # QC the data based on correlation values based on the info in Elgar 2001
    Sr = 2  # Hz
    CorrThresh = 0.3 + 0.4 * (Sr / 25) ** 0.5

    for i in range(1, 5):
        isbad = Data[f"Burst_CorBeam{i}"] * 0.01 <= CorrThresh
        Data[f"Burst_VelBeam{i}"][isbad] = np.nan

    # Convert the data from beam coords to ENU (This is all done according to the steps found here
    # https://support.nortekgroup.com/hc/en-us/articles/360029820971-How-is-a-coordinate-transformation-done

    # Load the transformation matrix
    T = pd.DataFrame(Data["Config"]["Burst_Beam2xyz"]).to_numpy()

    # Transform attitude data to radians
    hh = np.pi * (Data["Burst_Heading"].to_numpy() - 90) / 180
    pp = np.pi * Data["Burst_Pitch"].to_numpy() / 180
    rr = np.pi * Data["Burst_Roll"].to_numpy() / 180

    # Get the dimensions of v1
    row, col = Data["Burst_VelBeam1"].to_numpy().shape

    # Create the tiled transformation matrix
    Tmat = np.tile(T, (row, 1, 1))

    # Initialize heading and tilt matrices
    Hmat = np.zeros((3, 3, row))
    Pmat = np.zeros((3, 3, row))

    # Populate the heading and tilt matrices
    for i in range(row):
        Hmat[:, :, i] = [
            [np.cos(hh[i][0]), np.sin(hh[i][0]), 0],
            [-np.sin(hh[i][0]), np.cos(hh[i][0]), 0],
            [0, 0, 1],
        ]

        Pmat[:, :, i] = [
            [
                np.cos(pp[i][0]),
                -np.sin(pp[i][0]) * np.sin(rr[i][0]),
                -np.cos(rr[i][0]) * np.sin(pp[i][0]),
            ],
            [0, np.cos(rr[i][0]), -np.sin(rr[i][0])],
            [
                np.sin(pp[i][0]),
                np.sin(rr[i][0]) * np.cos(pp[i][0]),
                np.cos(pp[i][0]) * np.cos(rr[i][0]),
            ],
        ]

    R1Mat = np.zeros((4, 4, row))

    for i in range(row):
        R1Mat[0:3, 0:3, i] = np.matmul(Hmat[:, :, i], Pmat[:, :, i])
        R1Mat[3, 0:4, i] = R1Mat[2, 0:4, i]
        R1Mat[0:4, 3, i] = R1Mat[0:4, 2, i]

    R1Mat[2, 3, :] = 0
    R1Mat[3, 2, :] = 0

    Rmat = np.zeros((4, 4, row))

    Tmat = np.swapaxes(Tmat, 0, -1)
    Tmat = np.swapaxes(Tmat, 0, 1)

    for i in range(row):
        Rmat[:, :, i] = R1Mat[:, :, i] @ Tmat[:, :, i]

    # Convert to ENU
    ENU = np.einsum('ijk,ijl->ilk', Rmat, Data["Burst_VelBeam1"])

    print(ENU[0,:])

    # Create cell depth vector

    vector = np.arange(1, Data["Burst_NCells"][0][0] + 1)

    Data["CellDepth"] = (
        Data["Config"]["Burst_BlankingDistance"][0]
        + vector * Data["Config"]["Burst_CellSize"][0]
    )

    return Data
