from post_processing.HydroSurveyor.process_file_HydroSurveyor import Hydro_process
import matplotlib.pyplot as plt
from post_processing.HydroSurveyor.old.process_session_HydroSurveyor import Hydro_session_process 
from scipy.signal import medfilt
from post_processing.ADCP.process_Sig1k import process
from post_processing.HydroSurveyor.read_HydroSurveyor import vector_df
import pandas as pd
import datetime as dt
import numpy as np
import pickle as pickle 

#This file is the summary analysis file for the surfzone test, the first few commented lines process and save the data by using
#functions from other scripts. We are using the pickle module in order to write the data as bytes into a txt file. The rest of the
#script then loads the data using pickle and generates some plots.


# Data = Hydro_process(
#     r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\file_data.mat"
# )

# AutoData = Hydro_session_process(
#     r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\session_data.mat"
# )

# AdcpData = process(
#     r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\S103080A004_ICW_test.mat"
# )

# LayerData = pd.read_csv(
#     r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\vel_vectors.csv",
#     header=0,
# )
# with open(r'C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Processed Data\ICWTestFile.txt','wb') as file:
#     pickle.dump(Data, file)
# with open(r'C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Processed Data\ICWTestSig.txt','wb') as file:
#     pickle.dump(AdcpData, file)
# with open(r'C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Processed Data\ICWTestLayer.txt','wb') as file:
#     pickle.dump(LayerData, file)
# with open(r'C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Processed Data\ICWTestSession.txt','wb') as file:
#     pickle.dump(AutoData, file)

with open(r'C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Processed Data\ICWTestFile.txt','rb') as file:
    Data = pickle.load(file)
with open(r'C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Processed Data\ICWTestSig.txt','rb') as file:
    AdcpData = pickle.load(file)
with open(r'C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Processed Data\ICWTestLayer.txt','rb') as file:
    LayerData = pickle.load(file)
with open(r'C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Processed Data\ICWTestSession.txt','rb') as file:
    AutoData = pickle.load(file)

DateTime = pd.to_datetime(LayerData["utc_time"], format="%Y-%m-%d %H:%M:%S.%f")
tos = dt.timedelta(hours=4)
DateTime = DateTime - tos
AbsVel = pd.DataFrame(np.sqrt(LayerData['average_E']**2  + LayerData['average_N']**2 + LayerData['average_U']**2 ))


####

def adcp_comparison_North(AdcpData, Data, AutoData, LayerData):
    lw = 1
    plt.figure()
    plt.plot(
        (AdcpData["Burst_Time"]),
        medfilt(np.nanmean(AdcpData["ENU"][:,:,1], axis=1)),
        label="ADCP Data",
    )
    plt.plot(
        Data["DateTime"],
        medfilt(np.nanmean(Data["NorthVel"], axis=1)),
        color="Red",
        label="File Data",
        linewidth=lw,
    )

    plt.plot(DateTime, medfilt(LayerData["average_N"]), label="Layer Data", linewidth=lw)
    plt.xlim(AutoData["DateTime"][0], AutoData["DateTime"][-1])
    plt.title("Northing Velocities vs Time")
    plt.xlabel("Time (DD HH:MM)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()

    plt.axvline(dt.datetime(2024,6,24,13,54,29),color='green')
    plt.axvline(dt.datetime(2024,6,24,13,55,38),color='red')

    plt.axvline(dt.datetime(2024,6,24,13,57,8),color='green')
    plt.axvline(dt.datetime(2024,6,24,13,58,36),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,1,8),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,2,29),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,3,30),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,4,20),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,9,28),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,10,33),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,15,29),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,16,27),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,25,2),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,28,17),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,35,30),color='green')
    
    plt.show()

def adcp_comparison_East(AdcpData, Data, AutoData, LayerData):
    lw = 1
    plt.figure()
    plt.plot(
        (AdcpData["Burst_Time"]),
        medfilt(np.nanmean(AdcpData["ENU"][:,:,0], axis=1)),
        label="ADCP Data",
    )
    plt.plot(
        Data["DateTime"],
        medfilt(np.nanmean(Data["EastVel"], axis=1)),
        color="Red",
        label="File Data",
        linewidth=lw,
    )

####

    plt.plot(DateTime, medfilt(LayerData["average_E"]), label="Layer Data", linewidth=lw)
    plt.xlim(AutoData["DateTime"][0], AutoData["DateTime"][-1])
    plt.title("Easting Velocities vs Time")
    plt.xlabel("Time (DD HH:MM)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()

    plt.axvline(dt.datetime(2024,6,24,13,54,29),color='green')
    plt.axvline(dt.datetime(2024,6,24,13,55,38),color='red')

    plt.axvline(dt.datetime(2024,6,24,13,57,8),color='green')
    plt.axvline(dt.datetime(2024,6,24,13,58,36),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,1,8),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,2,29),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,3,30),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,4,20),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,9,28),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,10,33),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,15,29),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,16,27),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,25,2),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,28,17),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,35,30),color='green')
    
    plt.show()

####

def adcp_comparison_Vert(AdcpData, Data, AutoData, LayerData):
    lw = 1
    plt.figure()
    plt.plot(
        (AdcpData["Burst_Time"]),
        medfilt(np.nanmean(AdcpData["ENU"][:,:,3], axis=1)),
        label="ADCP Data",
    )
    plt.plot(
        Data["DateTime"],
        medfilt(np.nanmean(Data["VertVel"], axis=1)),
        color="Red",
        label="File Data",
        linewidth=lw,
    )

    plt.plot(DateTime, medfilt(LayerData["average_U"]), label="Layer Data", linewidth=lw)
    plt.xlim(AutoData["DateTime"][0], AutoData["DateTime"][-1])
    plt.title("Vertical Velocities vs Time")
    plt.xlabel("Time (DD HH:MM)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()

    plt.axvline(dt.datetime(2024,6,24,13,54,29),color='green')
    plt.axvline(dt.datetime(2024,6,24,13,55,38),color='red')

    plt.axvline(dt.datetime(2024,6,24,13,57,8),color='green')
    plt.axvline(dt.datetime(2024,6,24,13,58,36),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,1,8),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,2,29),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,3,30),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,4,20),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,9,28),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,10,33),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,15,29),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,16,27),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,25,2),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,28,17),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,35,30),color='green')
    
    plt.show()

###

def adcp_comparison_Abs(AdcpData, Data, AutoData, LayerData):

    lw = 1
    plt.figure()
    plt.plot(
        (AdcpData["Burst_Time"]),
        (pd.DataFrame(np.nanmean(AdcpData["AbsVel"], axis=1))),
        label="ADCP Data",
    )
    plt.plot(
        Data["DateTime"],
        (pd.DataFrame(np.nanmean(Data["AbsVel"], axis=1))),
        color="Red",
        label="File Data",
        linewidth=lw,
    )

    plt.plot(DateTime, AbsVel, label="Layer Data", linewidth=lw)
    plt.xlim(AutoData["DateTime"][0], AutoData["DateTime"][-1])
    plt.title("Absolute Velocities vs Time")
    plt.xlabel("Time (DD HH:MM)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()

    plt.axvline(dt.datetime(2024,6,24,13,54,29),color='green')
    plt.axvline(dt.datetime(2024,6,24,13,55,38),color='red')

    plt.axvline(dt.datetime(2024,6,24,13,57,8),color='green')
    plt.axvline(dt.datetime(2024,6,24,13,58,36),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,1,8),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,2,29),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,3,30),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,4,20),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,9,28),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,10,33),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,15,29),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,16,27),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,25,2),color='green')
    plt.axvline(dt.datetime(2024,6,24,14,28,17),color='red')

    plt.axvline(dt.datetime(2024,6,24,14,35,30),color='green')
    
    plt.show()

def Vel_subplots(AdcpData, Data):
    fig, ax = plt.subplots(4)
    lw = 1
    ax[0].plot(
            (AdcpData["Burst_Time"]),
            (pd.DataFrame(np.nanmean(AdcpData["AbsVel"], axis=1))),
            label="ADCP Data",
        )
    ax[0].plot(
            Data["DateTime"],
            (pd.DataFrame(np.nanmean(Data["AbsVel"], axis=1))),
            color="Red",
            label="File Data",
            linewidth=lw,)
    ax[0].plot(DateTime, AbsVel, label="Layer Data", linewidth=lw)
    ax[0].set_xlim(dt.datetime(2024,6,24,14,9,28),(dt.datetime(2024,6,24,14,10,33)))

    ax[1].plot(
            (AdcpData["Burst_Time"]),
            (pd.DataFrame(np.nanmean(AdcpData["AbsVel"], axis=1))),
            label="ADCP Data",
        )
    ax[1].plot(
            Data["DateTime"],
            (pd.DataFrame(np.nanmean(Data["AbsVel"], axis=1))),
            color="Red",
            label="File Data",
            linewidth=lw,)
    ax[1].plot(DateTime, AbsVel, label="Layer Data", linewidth=lw)
    ax[1].set_xlim(dt.datetime(2024,6,24,14,15,29),(dt.datetime(2024,6,24,14,16,27)))


    ax[2].plot(
            (AdcpData["Burst_Time"]),
            (pd.DataFrame(np.nanmean(AdcpData["AbsVel"], axis=1))),
            label="ADCP Data",
        )
    ax[2].plot(
            Data["DateTime"],
            (pd.DataFrame(np.nanmean(Data["AbsVel"], axis=1))),
            color="Red",
            label="File Data",
            linewidth=lw,)
    ax[2].plot(DateTime, AbsVel, label="Layer Data", linewidth=lw)
    ax[2].set_xlim(dt.datetime(2024,6,24,14,25,2),(dt.datetime(2024,6,24,14,28,17)))

    ax[3].plot(
            (AdcpData["Burst_Time"]),
            (pd.DataFrame(np.nanmean(AdcpData["AbsVel"], axis=1))),
            label="ADCP Data",
        )
    ax[3].plot(
            Data["DateTime"],
            (pd.DataFrame(np.nanmean(Data["AbsVel"], axis=1))),
            color="Red",
            label="File Data",
            linewidth=lw,)
    ax[3].plot(DateTime, AbsVel, label="Layer Data", linewidth=lw)
    ax[3].set_xlim(dt.datetime(2024,6,24,14,35,30),DateTime.iloc[-1])

    for i in range(len(ax)):
            ax[i].set_ylim(top=1, bottom=.4)
            ax[i].legend()
    fig.suptitle("Different Velocities versus Time")
    fig.supxlabel("Time (DD HH:MM)")
    fig.supylabel("Velocity (m/s)")
    fig.tight_layout()
    plt.show()

###

def raw_process_comp(AdcpData, Data):
    raw, EastVel, NorthVel, VertVel, D, I = vector_df(r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\file_data.mat"); del I, raw, D
    dim = EastVel.shape

    nan_mask = (np.full(dim, False))

    for i in range(dim[1]):
        nan_mask[:,i] = np.isfinite(NorthVel.iloc[:,i]) & np.isfinite(EastVel.iloc[:,i]) & np.isfinite(VertVel.iloc[:,i])

    # Replace NaNs with zeroes for the calculation
    NorthVel_no_nan = np.nan_to_num(NorthVel, nan=0.0)
    EastVel_no_nan = np.nan_to_num(EastVel, nan=0.0)
    VertVel_no_nan = np.nan_to_num(VertVel, nan=0.0)
    BtVel = np.nan_to_num(Data['BtVel'], nan=0.0)

    # Sum the squared velocities
    AbsVel = np.sqrt(NorthVel_no_nan**2 + EastVel_no_nan**2 + VertVel_no_nan**2)
    BtVel = np.sqrt(BtVel[:,0]**2 + BtVel[:,1]**2 + BtVel[:,2]**2)

    # Reapply the mask to set positions with any original NaNs back to NaN
    AbsVel[~nan_mask] = np.nan

    fig, axs = plt.subplots(2)
    axs[0].plot(Data['DateTime'],np.nanmean(Data['AbsVel'], axis = 1), label = 'Corrected')
    axs[0].plot(Data['DateTime'],np.nanmean(AbsVel, axis = 1), label = 'Uncorrected')
    axs[0].legend()

    axs[1].plot(Data['DateTime'], BtVel, label = 'BottomTrackVel')
    axs[1].legend()

    fig.suptitle("Looking at the BT influence on velocities")
    fig.supxlabel("Time (DD HH:MM)")
    fig.supylabel("Velocity (m/s)")
    fig.tight_layout()

    plt.show()




#4adcp_comparison_North(AdcpData, Data, AutoData, LayerData)

# adcp_comparison_East(AdcpData, Data, AutoData, LayerData)

# adcp_comparison_Vert(AdcpData, Data, AutoData, LayerData)

# adcp_comparison_Abs(AdcpData, Data, AutoData, LayerData)

# Vel_subplots(AdcpData,Data)

#raw_process_comp(AdcpData, Data)
