from post_processing.HydroSurveyor.process_file_HydroSurveyor import Hydro_process
import matplotlib.pyplot as plt
from post_processing.HydroSurveyor.process_session_HydroSurveyor import Hydro_session_process 
from scipy.signal import medfilt
from post_processing.ADCP.process_Sig1k import process
import numpy as np
import pandas as pd
import datetime as dt

Data = Hydro_process(
    r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\file_data.mat"
)

AutoData = Hydro_session_process(
    r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\session_data.mat"
)

AdcpData = process(
    r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\S103080A004_ICW_test.mat"
)

LayerData = pd.read_csv(
    r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\vel_vectors.csv",
    header=0,
)
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
        (pd.DataFrame(np.nanmean(AdcpData["AbsVel"], axis=1)).rolling(window = 4).mean()),
        label="ADCP Data",
    )
    plt.plot(
        Data["DateTime"],
        (pd.DataFrame(np.nanmean(Data["AbsVel"], axis=1)).rolling(window = 4).mean()),
        color="Red",
        label="File Data",
        linewidth=lw,
    )

    plt.plot(DateTime, AbsVel.rolling(window = 4).mean(), label="Layer Data", linewidth=lw)
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

# adcp_comparison_North(AdcpData, Data, AutoData, LayerData)

# adcp_comparison_East(AdcpData, Data, AutoData, LayerData)

# adcp_comparison_Vert(AdcpData, Data, AutoData, LayerData)

# adcp_comparison_Abs(AdcpData, Data, AutoData, LayerData)

# fig, ax = plt.subplots(4)
# lw = 1
# ax[0].plot(
#         (AdcpData["Burst_Time"]),
#         (pd.DataFrame(np.nanmean(AdcpData["AbsVel"], axis=1))),
#         label="ADCP Data",
#     )
# ax[0].plot(
#         Data["DateTime"],
#         (pd.DataFrame(np.nanmean(Data["AbsVel"], axis=1))),
#         color="Red",
#         label="File Data",
#         linewidth=lw,)
# ax[0].plot(DateTime, AbsVel, label="Layer Data", linewidth=lw)
# ax[0].set_xlim(dt.datetime(2024,6,24,14,9,28),(dt.datetime(2024,6,24,14,10,33)))

# ax[1].plot(
#         (AdcpData["Burst_Time"]),
#         (pd.DataFrame(np.nanmean(AdcpData["AbsVel"], axis=1))),
#         label="ADCP Data",
#     )
# ax[1].plot(
#         Data["DateTime"],
#         (pd.DataFrame(np.nanmean(Data["AbsVel"], axis=1))),
#         color="Red",
#         label="File Data",
#         linewidth=lw,)
# ax[1].plot(DateTime, AbsVel, label="Layer Data", linewidth=lw)
# ax[1].set_xlim(dt.datetime(2024,6,24,14,15,29),(dt.datetime(2024,6,24,14,16,27)))


# ax[2].plot(
#         (AdcpData["Burst_Time"]),
#         (pd.DataFrame(np.nanmean(AdcpData["AbsVel"], axis=1))),
#         label="ADCP Data",
#     )
# ax[2].plot(
#         Data["DateTime"],
#         (pd.DataFrame(np.nanmean(Data["AbsVel"], axis=1))),
#         color="Red",
#         label="File Data",
#         linewidth=lw,)
# ax[2].plot(DateTime, AbsVel, label="Layer Data", linewidth=lw)
# ax[2].set_xlim(dt.datetime(2024,6,24,14,25,2),(dt.datetime(2024,6,24,14,28,17)))

# ax[3].plot(
#         (AdcpData["Burst_Time"]),
#         (pd.DataFrame(np.nanmean(AdcpData["AbsVel"], axis=1))),
#         label="ADCP Data",
#     )
# ax[3].plot(
#         Data["DateTime"],
#         (pd.DataFrame(np.nanmean(Data["AbsVel"], axis=1))),
#         color="Red",
#         label="File Data",
#         linewidth=lw,)
# ax[3].plot(DateTime, AbsVel, label="Layer Data", linewidth=lw)
# ax[3].set_xlim(dt.datetime(2024,6,24,14,35,30),DateTime.iloc[-1])

# for i in range(len(ax)):
#         ax[i].set_ylim(top=1, bottom=.4)
#         ax[i].legend()
# fig.suptitle("Different Velocities versus Time")
# fig.supxlabel("Time (DD HH:MM)")
# fig.supylabel("Velocity (m/s)")
# fig.tight_layout()
# plt.show()