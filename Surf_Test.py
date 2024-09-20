from post_processing.HydroSurveyor.process_file_HydroSurveyor import Hydro_process
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np

Data1 = Hydro_process(
    r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\2024_08_30_Surfzone\File\2024_08_30_SurfzoneFile1.mat"
)
Data2 = Hydro_process(
    r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\2024_08_30_Surfzone\File\2024_08_30_SurfzoneFile2.mat"
)

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
        label="ADCP Data",
    )
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
    plt.title("Absolute Velocities vs Time")
    plt.xlabel("Time (DD HH:MM)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.show()


def bathy_plot(CombinedData):
    fig = plt.figure()
    
    # syntax for 3-D projection
    ax = plt.axes(projection ='3d')
    
    # defining axes
    z = CombinedData['VbDepth']
    x = CombinedData['Latitude']
    y = CombinedData['Longitude']
    c = x + y

    ax.scatter(x, y, z, c = c)
    
    # syntax for plotting
    ax.set_title('3d Scatter plot geeks for geeks')

    # function for z axis
# def bathy_mesh(COmbinedData):
#     # x and y axis
#     Z = CombinedData['VbDepth']
#     x = CombinedData['Latitude']
#     y = CombinedData['Longitude']
    
#     X, Y = np.meshgrid(x, y)
    
    
#     fig = plt.figure()
#     ax = plt.axes(projection ='3d')
#     ax.plot_wireframe(X, Y, Z, color ='green')
#     ax.set_title('wireframe geeks for geeks')

#     plt.show()


# adcp_comparison_Abs(Data3,Data4,CombinedData)

bathy_plot(CombinedData)

bathy_mesh(CombinedData)