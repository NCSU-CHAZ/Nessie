from post_processing.HydroSurveyor.process_file_HydroSurveyor import Hydro_process
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import pickle as pickle

# This file is the summary analysis file for the surfzone test, the first few commented lines process and save the data by using
# functions from other scripts. We are using the pickle module in order to write the data as bytes into a txt file. The rest of the
# script then loads the data using pickle and generates some plots. Some of the plots require other individual data streams to work.
# To get these other data streams simple run hydroprocess on the raw data for whatever it needs to process.

# CombinedData = Hydro_process(
#     r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\2024_08_30_Surfzone\File"
# )
# with open(r'C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Processed Data\SurfTest.txt','wb') as file:
#     pickle.dump(CombinedData, file)

with open(
    r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Processed Data\SurfTest.txt",
    "rb",
) as file:
    CombinedData = pickle.load(file)


def time_comparison(Data1, Data2, Data3, Data4):
    fig, axs = plt.subplots(4, sharex=True)
    axs[0].plot(Data1["DateTime"], Data1["SampleNumber"], label="Session 1")
    axs[1].plot(Data2["DateTime"], Data2["SampleNumber"], label="Session 2")
    axs[2].plot(Data3["DateTime"], Data3["SampleNumber"], label="Session 3")
    axs[3].plot(Data4["DateTime"], Data4["SampleNumber"], label="Session 4")

    for i in range(len(axs)):
        axs[i].legend()
    fig.suptitle("DateTimes versus Sample Number")
    fig.supxlabel("Time (DD HH:MM)")
    fig.supylabel("Sample Number")
    fig.tight_layout()
    plt.show()


def adcp_comparison_Abs(Data3, Data4, CombinedData):

    lw = 1
    fig, axs = plt.subplots(2, sharex=True)
    axs[0].plot(
        (CombinedData["DateTime"]),
        (pd.DataFrame(np.nanmean(CombinedData["AbsVel"], axis=1))),
        label="Combined Data",
    )
    plt.legend()
    axs[1].plot(
        Data4["DateTime"],
        (pd.DataFrame(np.nanmean(Data4["AbsVel"], axis=1))),
        color="Red",
        label="Session 4",
        linewidth=lw,
    )
    axs[1].plot(
        Data3["DateTime"],
        (pd.DataFrame(np.nanmean(Data3["AbsVel"], axis=1))),
        color="Blue",
        label="Session 3",
        linewidth=lw,
    )
    fig.suptitle("Absolute Velocity versus Time")
    fig.supxlabel("Time (DD HH:MM)")
    fig.supylabel("Velocity (m/s)")
    plt.legend()
    plt.show()


def bathy_plot(CombinedData):
    # Sample data: Replace with your actual longitude, latitude, and depth values
    x = CombinedData["Longitude"]  # Longitude
    y = CombinedData["Latitude"]  # Latitude
    z = CombinedData["VbDepth"]  # Depth (negative for bathymetry)

    # Create 3D figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Plotting options:
    # 1. Scatter Plot
    im1 = ax.scatter(x, y, z, c=z, cmap="viridis")  # Color by depth
    ax.invert_zaxis()
    cbar = plt.colorbar(im1, ax=ax, shrink=0.5, aspect=5)
    cbar.set_label("Depth (meters)")
    # Set labels and title
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_zlabel("Depth")
    plt.title("3D Bathymetry Survey")

    plt.show()


def pitch_roll_comp(CombinedData):

    fig, ax = plt.subplots(2, sharex=True)

    ax[0].plot(CombinedData["DateTime"], CombinedData["Pitch"])
    ax[1].plot(CombinedData["DateTime"], CombinedData["Roll"])
    ax[0].set_title("Pitch vs Time")
    ax[1].set_title("Roll vs Time")
    ax[0].set_ylabel("Pitch (rad)")
    ax[1].set_ylabel("Roll (rad)")

    fig.supxlabel("Time (DD HH:MM)")
    plt.show()


def Vb_Plot(CombinedData):
    plt.plot(CombinedData["DateTime"], CombinedData["VbDepth"])
    plt.title("Vertical Beam Depth vs Time")
    plt.xlabel("Time")
    plt.ylabel("Depth (m)")
    plt.show()


def variance_inspection(CombinedData):

    #This function is designed to split the velocity field up into the four different directions of travel in order to
    #analyze the variance dependent on the whether or not the transect was traveling E->W, W->E,N->S,S->N.

    NMask = (CombinedData["HeadingRad"] >= 7 * np.pi / 4) | (
        CombinedData["HeadingRad"] < np.pi / 4
    )
    EMask = (CombinedData["HeadingRad"] >= np.pi / 4) & (
        CombinedData["HeadingRad"] < 3 * np.pi / 4
    )
    SMask = (CombinedData["HeadingRad"] >= 3 * np.pi / 4) & (
        CombinedData["HeadingRad"] < 5 * np.pi / 4
    )
    WMask = (CombinedData["HeadingRad"] >= 5 * np.pi / 4) & (
        CombinedData["HeadingRad"] < 7 * np.pi / 4
    )
  
    dim = CombinedData["AbsVel"].shape
    NMask = np.tile(NMask, (1, dim[1]))
    EMask = np.tile(EMask, (1, dim[1]))
    SMask = np.tile(SMask, (1, dim[1]))
    WMask = np.tile(WMask, (1, dim[1]))

    NorthingVel = CombinedData["AbsVel"].copy()
    EastingVel = CombinedData["AbsVel"].copy()
    SouthingVel = CombinedData["AbsVel"].copy()
    WestingVel = CombinedData["AbsVel"].copy()

    NorthingVel[~NMask]= float('NaN')
    EastingVel[~EMask]= float('NaN')
    SouthingVel[~SMask]= float('NaN')
    WestingVel[~WMask]= float('NaN')

    plt.plot(CombinedData['DateTime'],np.nanmean(NorthingVel,axis=1), label = 'Northing')
    plt.plot(CombinedData['DateTime'],np.nanmean(EastingVel,axis=1), label = 'Easting')
    plt.plot(CombinedData['DateTime'],np.nanmean(SouthingVel,axis=1), label = 'Southing')
    plt.plot(CombinedData['DateTime'],np.nanmean(WestingVel,axis=1), label = 'Westing')
    plt.legend()
    plt.show()

    #After seeing the data field has been split up appropriately, analyze the variance of the data.

    # Northing velocities
    plt.subplot(2, 2, 1)
    plt.hist(NorthingVel[~np.isnan(NorthingVel)].values.ravel(),bins=100)
    plt.title('Northing Velocity Distribution')
    plt.xlabel('Velocity')
    plt.ylabel('Samples')

    # Easting velocities
    plt.subplot(2, 2, 2)
    plt.hist(EastingVel[~np.isnan(EastingVel)].values.ravel(),bins=100)
    plt.title('Easting Velocity Distribution')
    plt.xlabel('Velocity')
    plt.ylabel('Samples')

    # Southing velocities
    plt.subplot(2, 2, 3)
    plt.hist(SouthingVel[~np.isnan(SouthingVel)].values.ravel(),bins=100)
    plt.title('Southing Velocity Distribution')
    plt.xlabel('Velocity')
    plt.ylabel('Samples')

    # Westing velocities
    plt.subplot(2, 2, 4)
    plt.hist(WestingVel[~np.isnan(WestingVel)].values.ravel(),bins=100)
    plt.title('Westing Velocity Distribution')
    plt.xlabel('Velocity')
    plt.ylabel('Samples')

    plt.tight_layout()
    plt.show()

    #Now we can look at the distribution for the average velocities

    # Northing velocities
    plt.subplot(2, 2, 1)
    plt.hist(np.nanmean(NorthingVel,axis=1),bins=100)
    plt.title('Northing Average Velocity Distribution')
    plt.xlabel('Velocity')
    plt.ylabel('Samples')

    # Easting velocities
    plt.subplot(2, 2, 2)
    plt.hist(np.nanmean(EastingVel,axis=1),bins=100)
    plt.title('Eastingn Average Velocity Distribution')
    plt.xlabel('Velocity')
    plt.ylabel('Samples')

    # Southing velocities
    plt.subplot(2, 2, 3)
    plt.hist(np.nanmean(SouthingVel,axis=1),bins=100)
    plt.title('Southing Average Velocity Distribution')
    plt.xlabel('Velocity')
    plt.ylabel('Samples')

    # Westing velocities
    plt.subplot(2, 2, 4)
    plt.hist(np.nanmean(WestingVel,axis=1),bins=100)
    plt.title('Westing Average Velocity Distribution')
    plt.xlabel('Velocity')
    plt.ylabel('Samples')

    plt.tight_layout()
    plt.show()
# adcp_comparison_Abs(Data3, Data4, CombinedData)

# bathy_plot(CombinedData)

# pitch_roll_comp(CombinedData)

# Vb_Plot(CombinedData)

variance_inspection(CombinedData)
