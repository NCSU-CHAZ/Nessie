from HydroSurveyor.process_file_HydroSurveyor import Hydro_process
import matplotlib.pyplot as plt
from HydroSurveyor.process_session_HydroSurveyor import Hydro_session_process
from scipy.signal import medfilt
from ADCP.process_Sig1k import process
import numpy as np
import pandas as pd

Data = Hydro_process(
    r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\file_data.mat"
)

AutoData = Hydro_session_process(
    r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\session_data.mat"
)

AdcpData = process(r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\S103080A004_ICW_test.mat")

# LayerData = pd.read_csv(
#     r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\vel_vectors.csv",
#     header=0,
# )
# DateTime = pd.to_datetime(LayerData["utc_time"], format="%Y-%m-%d %H:%M:%S.%f")
# tos = dt.timedelta(hours=4)
# DateTime = DateTime - tos

def adcp_comparison(AdcpData, Data, AutoData, LayerData):
    lw = 1
    plt.figure()
    plt.plot(
        (AdcpData["Burst_Time"]),
        np.nanmean(AdcpData["NorthVel"], axis=0),
        label="ADCP Data",
    )
    plt.plot(
        Data["DateTime"],
        medfilt(np.nanmean(Data["NorthVel_interp"], axis=1)),
        color="Red",
        label="File Data",
        linewidth=lw,
    )
    plt.plot(
        AutoData["DateTime"],
        medfilt(np.nanmean(AutoData["NorthVel"], axis=1)),
        label="Session Data",
        color="Green",
        linewidth=lw,
    )
    # plt.plot(DateTime, medfilt(LayerData["average_N"]), label="Layer", linewidth=lw)
    plt.xlim(AutoData["DateTime"][0], AutoData["DateTime"][-1])
    plt.title("Northing Velocities vs Time")
    plt.xlabel("Time (DD HH:MM)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.show()

adcp_comparison(AdcpData, Data, AutoData)