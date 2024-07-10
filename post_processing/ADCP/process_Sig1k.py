from .read_Sig1k import read_Sig1k
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

    # Get the dimensions of the matrices
    row, col = Data["Burst_VelBeam1"].to_numpy().shape

    # Create cell depth vector

    vector = np.arange(1, Data["Burst_NCells"][0][0] + 1)

    Data["CellDepth"] = (
        Data["Config"]["Burst_BlankingDistance"][0]
        + vector * Data["Config"]["Burst_CellSize"][0]
    )

    # QC the data based on correlation values based on the info in Elgar 2001
    Sr = 2  # Hz
    CorrThresh = 0.3 + 0.4 * (Sr / 25) ** 0.5

    #Remove data thats collected over the surface of water
    isbad = np.zeros((row,col))

    for i in range(len(isbad)):
        isbad[i,:] = Data['CellDepth'] >= Data['Burst_Pressure'].iloc[i][0]
    isbad = isbad.astype(np.bool_)   
  
    for jj in range(1, 5):
            isbad2 = Data[f"Burst_CorBeam{jj}"] * 0.01 <= CorrThresh
            Data[f"Burst_VelBeam{jj}"][isbad] = np.nan
            Data[f"Burst_VelBeam{jj}"][isbad2] = np.nan        

   
    # Convert the data from beam coords to ENU (This is all done according to the steps found here
    # https://support.nortekgroup.com/hc/en-us/articles/360029820971-How-is-a-coordinate-transformation-done

    # Load the transformation matrix
    T = pd.DataFrame(Data["Config"]["Burst_Beam2xyz"]).to_numpy()

    # Transform attitude data to radians
    hh = np.pi * (Data["Burst_Heading"].to_numpy() - 90) / 180
    pp = np.pi * Data["Burst_Pitch"].to_numpy() / 180
    rr = np.pi * Data["Burst_Roll"].to_numpy() / 180

    # Create the tiled transformation matrix, this is for applyinh the transformation later to each data point
    Tmat = np.tile(T, (row, 1, 1))

    # Initialize heading and tilt matrices
    Hmat = np.zeros((3, 3, row))
    Pmat = np.zeros((3, 3, row))

    # Using vector mat populate the heading matrix and pitch/roll matrix with the appropriate values
    # The 3x3xrow matrix is the spatial dimensios at each measurement 
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

    #Combine the Hmat and Pmat vectors into one rotation matrix, this conversion matrix is organized with beams in the columns
    # and the rotation values on the rows (for each data point). The original Hmat and Pmat matrices are only made with the one Z
    # value in mind so we duplicate the 4 row of the transform matirx to create the fourth, same process for fourht column. 
    #                     Beam1   Beam2   Beam3   Beam4       
    #                X   [                               ]        
    #                Y   [                               ]             (at nth data point)
    #               Z1   [                          0    ]        
    #               Z2   [                  0            ]
    #                                
    R1Mat = np.zeros((4, 4, row)) #initialize rotation matrix

    for i in range(row):
        R1Mat[0:3, 0:3, i] = Hmat[:, :, i] @ Pmat[:, :, i] #Matrix multiplication 
        R1Mat[3, 0:4, i] = R1Mat[2, 0:4, i] #Create fourth row
        R1Mat[0:4, 3, i] = R1Mat[0:4, 2, i] #Create fourth column

    ### We zero out these value since Beams 3 and 4 can't measure both Z's
    R1Mat[2, 3, :] = 0
    R1Mat[3, 2, :] = 0

    Rmat = np.zeros((4, 4, row))

    Tmat = np.swapaxes(Tmat, 0, -1)
    Tmat = np.swapaxes(Tmat, 0, 1)

    for i in range(row):
        Rmat[:, :, i] = R1Mat[:, :, i] @ Tmat[:, :, i]

    Velocities = np.squeeze(np.array([[Data['Burst_VelBeam1']], [Data['Burst_VelBeam2']], [Data['Burst_VelBeam3']], [Data['Burst_VelBeam4']]]))
    
    # Convert to ENU
    ENU = np.einsum('ijk,jkl->ikl', Rmat, Velocities)
    ENU = np.transpose(ENU, (1,2,0))
    Data['ENU'] = ENU; del ENU

    # Add matrices with NaN values together without getting nans from the whole thing
    nan_mask = (np.full((row,col), False))

    for i in range(col):
        nan_mask[:,i] = np.isfinite(Data['ENU'][:,i,0]) & np.isfinite(Data['ENU'][:,i,1]) & np.isfinite(Data['ENU'][:,i,2])
    
    # Replace NaNs with zeroes for the calculation
    NorthVel_no_nan = np.nan_to_num(Data['ENU'][:,:,0], nan=0.0)
    EastVel_no_nan = np.nan_to_num(Data['ENU'][:,:,1], nan=0.0)
    VertVel_no_nan = np.nan_to_num(Data['ENU'][:,:,2], nan=0.0)

    # Sum the squared velocities
    Data['AbsVel'] = pd.DataFrame(np.sqrt(NorthVel_no_nan**2 + EastVel_no_nan**2 + VertVel_no_nan**2))

    # Reapply the mask to set positions with any original NaNs back to NaN
    Data['AbsVel'][~nan_mask] = np.nan

    return Data

