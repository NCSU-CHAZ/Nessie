from scipy.io import loadmat
import pandas as pd
import os


# Import .mat files
def create_df(filepath):
    rawdata = loadmat(
        filepath
    )  # Load in filepath, make sure you put an r out front r"placeholder/placeholder/placeholder.mat" so python
    # interprets the backslashes correctly
    del rawdata["__header__"]
    del rawdata["__version__"]
    del rawdata["__globals__"]
    # Delete unnecessary keys that list info about the function
    data = {}  # Initialize data dictionary to place data into
    Info = None  # Initialize info as None
    for (
        i
    ) in (
        rawdata.keys()
    ):  # Run through loop where i is the key to the array in the dictionary
        array = rawdata[i]  # Initialize a a duplicate array to allow for reshaping
        if (
            rawdata[i].ndim == 3
        ):  # Flatten 3d arrays into 2d arrays, this causes an 3577x85x4 array to become 3577x340
            reshaped = array.reshape(array.shape[0], -1)
            data[i] = pd.DataFrame(
                reshaped
            )  # Save the data into the dictionary as a dataframe, dataframes are one of the many ways to
            # store data in python
        elif (
            i == "Info"
        ):  # The info structure does not transfer well between MATLAB and Python but contains relevant data so we just
            # make a 1 to 1 copy
            Info = array
        elif (
            i == "config"
        ):  # The info structure does not transfer well between MATLAB and Python but contains relevant data so we just
            # make a 1 to 1 copy
            Info = array
        else:  # All 2d arrays get stored as a dataframe, this is the majority of data arrays in the structure
            data[i] = pd.DataFrame(array)
    return data, Info


# This funciton will combine all the different sessions into one large session
def combine_sessions(filepath):
    LastData = pd.DataFrame([])
    i = 0
    for name in os.listdir(filepath):
        Data, info = create_df(filepath + "\\" + str(name))
        if i == 0:
            CombinedData = Data.copy()
        if i == 1:
            for key in Data.keys():
                CombinedData[key] = pd.concat([LastData[key], Data[key]])
        LastData = Data
        i = 1
    return CombinedData, info


# Function that uses the previous readin function to acquire the data, and then any further processing to store the variables in a favorable way
def vector_df(filepath):
    if (
        os.path.isdir(filepath) == True
    ):  # Detect if there is a directory containing sessions to be combined
        data, Info = combine_sessions(filepath)
    if os.path.isdir(filepath) == False:
        data, Info = create_df(filepath)
    # Acquire individual direction dataframes
    number_vertical_cells = int(
        data["WaterVelEnu_m_s"].shape[1] / 4
    )  # Get the number of vertical cells by dividing the number of clumns by number of beams
    WaterEastVel = data["WaterVelEnu_m_s"].iloc[
        :, 0::4
    ].copy()  # 3557x340 matrix gets sorted for every fourth column,
    WaterEastVel.columns = range(WaterEastVel.columns.size)
    WaterVertVel = data["WaterVelEnu_m_s"].iloc[
        :, 3::4
    ].copy()
    WaterVertVel.columns = range(WaterVertVel.columns.size)
    # this pulls out the individual ENU and Error columns for each of the 85 cells
    WaterNorthVel = data["WaterVelEnu_m_s"].iloc[
        :, 2::4
    ].copy()
    WaterNorthVel.columns = range(WaterNorthVel.columns.size)
    WaterErrVel = data["WaterVelEnu_m_s"].iloc[
        :, 3::4
    ].copy()
    WaterErrVel.columns = range(WaterErrVel.columns.size)
    WaterEastVel.reset_index(drop=True, inplace=True)
    rawdata = data.copy()
    return rawdata, WaterEastVel, WaterNorthVel, WaterVertVel, WaterErrVel, Info
