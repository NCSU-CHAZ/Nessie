from post_processing.HydroSurveyor.process_file_HydroSurveyor import Hydro_process
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import pickle as pickle
from scipy.stats import binned_statistic_2d
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# This file is the summary analysis file for the surfzone test, the first few commented lines process and save the data by using
# functions from other scripts. We are using the pickle module in order to write the data as bytes into a txt file. The rest of the
# script then loads the data using pickle and generates some plots. Some of the plots require other individual data streams to work.
# To get these other data streams simple run hydroprocess on the raw data for whatever it needs to process.

interpsize = 2 #This would be .05m for the interpolated cell size

CombinedData = Hydro_process(
    r"Z:\BHI_NearshoreJetskiSurvey_Data\2025_05_01\2025_05_01_BHI_unprocessed.mat", interpsize
)
# with open(r"Z:\BHI_NearshoreJetskiSurvey_Data\2025_05_01\2025_05_01_processed.txt",'wb') as file:
#     pickle.dump(CombinedData, file)

# with open(
#     r"Z:\BHI_NearshoreJetskiSurvey_Data\2025_05_01\2025_05_01_processed.txt",
#     "rb",
# ) as file:
#     CombinedData = pickle.load(file)

#Plot Longshore, Crosshore, and Vertical Components

date_format = mdates.DateFormatter('%m/%d %H:%M')

def adcp_comparison_Abs(CombinedData):

    lw = 1
    fig, axs = plt.subplots(3, sharex=True)
    axs[0].plot(
        (CombinedData["DateTime"]),
        (pd.DataFrame(np.nanmean(CombinedData["LSVel"], axis=1))),
        label="Longshore",
    )
    axs[0].legend()
    axs[1].plot(
        CombinedData["DateTime"],
        (pd.DataFrame(np.nanmean(CombinedData["CSVel"], axis=1))),
        color="Red",
        label="Cross Shore",
        linewidth=lw,
    )
    axs[1].legend()
    axs[2].plot(
        CombinedData["DateTime"],
        (pd.DataFrame(np.nanmean(CombinedData["VertVel"], axis=1))),
        color="Green",
        label="Vertical",
        linewidth=lw,
    )

    axs[0].set_ylim(-1.5,1.5)
    axs[1].set_ylim(-1.5,1.5)
    axs[2].set_ylim(-1.5,1.5)

    fig.suptitle("Velocity Components versus Time")
    fig.supxlabel("Time (DD HH:MM)")
    fig.supylabel("Velocity (m/s)")
    plt.xlim(CombinedData['DateTime'][0],CombinedData['DateTime'][-1])
    axs[0].xaxis.set_major_formatter(date_format)
    axs[2].legend()
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
    im1 = ax.scatter(x, y, z, c=z, cmap="viridis_r") # Color by depth
    cbar = plt.colorbar(im1, ax=ax, shrink=0.5, aspect=5)
    cbar.set_label("Depth (meters)")
    # Set labels and title
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_zlabel("Depth")
    # ax.invert_zaxis()
    plt.title("3D Bathymetry Survey")

    plt.show()

def mesh_plot(CombinedData):
    #Assign data and choose number of bins for 3d grid
    x = np.ravel(CombinedData["Longitude"])
    y = np.ravel(CombinedData["Latitude"])
    z = np.ravel(CombinedData["VbDepth"])

    bins = 50
    
    #Bins x, y, z into a 2D grid and averages z in each bin.
    Z, xedges, yedges, binnumber = binned_statistic_2d(
        x, y, z, statistic='mean', bins=bins)
    # Grid centers for plotting
    xcenters = (xedges[:-1] + xedges[1:]) / 2
    ycenters = (yedges[:-1] + yedges[1:]) / 2
    X, Y = np.meshgrid(xcenters, ycenters)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z.T, cmap='viridis_r', edgecolor='none')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Depth')
    ax.invert_zaxis()
    ax.set_title('Interpolated Bathymetry Mesh Plot')
    plt.show()

def depth_velocity_plot(Data):
    fig, axs = plt.subplots(3)

    im1 = axs[0].pcolormesh(
        Data["DateTime"],
        Data["interpCellDepth"],
        Data["LSVel_interp"].T,
        shading="auto",
    )
    im2 = axs[1].pcolormesh(
        Data["DateTime"],
        Data["interpCellDepth"],
        Data["CSVel_interp"].T,
        shading="auto",
    )
    im3 = axs[2].pcolormesh(
        Data["DateTime"],
        Data["interpCellDepth"],
        Data["VertVel_interp"].T,
        shading="auto",
    )
    axs[0].plot(Data["DateTime"], Data["VbDepth_m"])
    axs[1].plot(Data["DateTime"], Data["VbDepth_m"])
    axs[2].plot(Data["DateTime"], Data["VbDepth_m"])

    axs[0].set_title("Longshore Velocity")
    axs[1].set_title("Cross Shore Velocity")
    axs[2].set_title("Vertical Velocity")

    axs[0].set_ylim(0,np.max(Data["VbDepth_m"]))
    axs[1].set_ylim(0,np.max(Data["VbDepth_m"]))
    axs[2].set_ylim(0,np.max(Data["VbDepth_m"]))

    cb1 = fig.colorbar(im1, ax=axs[0])
    cb2 = fig.colorbar(im2, ax=axs[1])
    cb3 = fig.colorbar(im3, ax=axs[2])
    cb1.ax.set_ylabel("Velocity (m/s)")
    cb2.ax.set_ylabel("Velocity (m/s)")
    cb3.ax.set_ylabel("Velocity (m/s)")
    fig.tight_layout()
    fig.supxlabel("DateTime (DD HH:MM)")
    fig.supylabel("Depth (m)")
    
    plt.show()

def vel_plot_no_interp(Data):
     #This plotter will create a similar graph as the last one however it will not use the interpolated cell size,
     #to do this it will give pcolor mesh the edges of the bins it has velocity data for in both time and depth space.
     DateTime =  Data["DateTime"]
     CS =  Data['CSVel']
     LS =  Data['LSVel']
     Depths = Data['CellGrid']
     dim = np.shape(Data['CSVel'])
     
     time_deltas = np.diff(DateTime).astype('timedelta64[ns]')
     dt = np.median(time_deltas)

     #Time edges
     time_edges = []
     for i in range(dim[0]-1):
         middle = DateTime[i] + +(DateTime[i+1]-DateTime[i])/2
         time_edges.append(middle)
     
     #Add in first and last edges
     time_edges = [DateTime[0] - (DateTime[1]-DateTime[0])/2] + time_edges + [DateTime[-1] - (DateTime[-1]-DateTime[-2])/2]
     time_edges = np.array(time_edges)
     fig, ax = plt.subplots(figsize = (12,6))
     for i in range(dim[0]):
        #Depth edges
        row = Depths[i]
        row_edges = np.zeros((dim[1]+1))
        row_edges[1:-1] = (row[:-1] + row[1:])/2
        row_edges[0] = row[0] - (row[0] - row[1])/2
        row_edges[-1] = row[-1] + (row[-1] - row[-2])/2
        
        # Time edges for this row
        t0 = time_edges[i]
        t1 = time_edges[i + 1]
        t_edges = [t0, t1]

        #Create meshgrids that pcolormesh can use
        T,D = np.meshgrid(t_edges, row_edges, indexing='ij')
        
        #Plot
        pcm = ax.pcolormesh(T,D,LS[i][np.newaxis, :], shading='auto',cmap='viridis')

     ax.set_xlabel('Time')
     ax.set_ylabel('Depth (m)')
     ax.set_title('Velocity over Time and Depth')
     ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d\n%H:%M'))
     ax.set_ylim(0,10)
     fig.autofmt_xdate()
     plt.colorbar(ax.collections[0], ax=ax, label='Velocity (m/s)')
    
     plt.show()


adcp_comparison_Abs(CombinedData)

# bathy_plot(CombinedData)

# mesh_plot(CombinedData)

# depth_velocity_plot(CombinedData)

#vel_plot_no_interp(CombinedData)