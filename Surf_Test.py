from post_processing.HydroSurveyor.process_file_HydroSurveyor import Hydro_process
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

Data3 = Hydro_process(
    r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\2024_08_30_Surfzone\File\2024_08_30_SurfzoneFile3.mat"
)

Data4 = Hydro_process(
    r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\2024_08_30_Surfzone\File\2024_08_30_SurfzoneFile4.mat"
)

CombinedData = Hydro_process(
    r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\2024_08_30_Surfzone\File"
)


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
    x = CombinedData['Longitude']  # Longitude
    y = CombinedData['Latitude']  # Latitude
    z = CombinedData['VbDepth']     # Depth (negative for bathymetry)

    # Create 3D figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plotting options:
    # 1. Scatter Plot
    im1 = ax.scatter(x, y, z, c=z, cmap='viridis')  # Color by depth
    ax.invert_zaxis()
    cbar = plt.colorbar(im1, ax=ax, shrink=0.5, aspect=5)
    cbar.set_label('Depth (meters)')
    # Set labels and title
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Depth')
    plt.title('3D Bathymetry Survey')

    plt.show()

def pitch_roll_comp(CombinedData):
    
    fig, ax = plt.subplots(2, sharex= True)

    ax[0].plot(CombinedData['DateTime'],CombinedData['Pitch'])
    ax[1].plot(CombinedData['DateTime'],CombinedData['Roll'])
    ax[0].set_title('Pitch vs Time')
    ax[1].set_title('Roll vs Time')
    ax[0].set_ylabel('Pitch (rad)')
    ax[1].set_ylabel('Roll (rad)')

    fig.supxlabel("Time (DD HH:MM)")
    plt.show()

def Vb_Plot(CombinedData):
    plt.plot(CombinedData['DateTime'],CombinedData['VbDepth'])
    plt.title('Vertical Beam Depth vs Time')
    plt.xlabel('Time')
    plt.ylabel('Depth (m)')
    plt.show()


#adcp_comparison_Abs(Data3, Data4, CombinedData)

#bathy_plot(CombinedData)

#pitch_roll_comp(CombinedData)

#Vb_Plot(CombinedData)