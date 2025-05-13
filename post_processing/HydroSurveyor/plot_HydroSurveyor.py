from process_file_HydroSurveyor import Hydro_process
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import pandas as pd

datapath = r"Z:\BHI_NearshoreJetskiSurvey_Data\2025_05_01\2025_05_01_BHI_unprocessed.mat"

Data = Hydro_process(
    r"Z:\BHI_NearshoreJetskiSurvey_Data\2025_05_01\2025_05_01_BHI_unprocessed.mat"
)


# # Layer Data
# LayerData = pd.read_csv(
#     r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\vel_vectors.csv",
#     header=0,
# )

# DateTime = pd.to_datetime(LayerData["utc_time"], format="%Y-%m-%d %H:%M:%S.%f")
# tos = dt.timedelta(hours=4)
# LayerData['DateTime']= DateTime - tos


#MatVel,info = create_df(r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\HydroAnalysisExp.mat"); del info


def raw_comparison_plot(Data):
    raw_velE = np.nanmean(Data["EastVel"], axis=1)
    raw_velN = np.nanmean(Data["NorthVel"], axis=1)
    raw_velU = np.nanmean(Data["VertVel"], axis=1)

    plt.figure()
    plt.plot(Data["DateTime"], raw_velE, label="Easting")
    plt.plot(Data["DateTime"], raw_velN, label="Northing")
    plt.plot(Data["DateTime"], raw_velU, label="Vertical")
    plt.xlabel("Time (DD HH:MM)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Raw Velocities vs Time ~~File~~")
    plt.legend()
    plt.show()


def BT_comparison_plot(Data):
    heading_rad = np.deg2rad(AutoData["HydroSurveyor_MagneticHeading_deg"])
    heading_rad = heading_rad.values.reshape(-1, 1)

    BtVelN = AutoData["BtVelX"] * np.cos(heading_rad) + AutoData["BtVelY"] * np.sin(
        heading_rad
    )

    plt.figure()
    plt.plot(Data["DateTime"], Data["BtVel"].iloc[:, 1], label="File")
    plt.plot(AutoData["DateTime"], BtVelN, label="Session")
    plt.xlabel("Time (DD HH:MM)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Bottom Track Velocities vs Time")
    plt.legend()
    plt.show()


def auto_manual_comparison(AutoData, Data):
    auto_velN = np.nanmean(AutoData["NorthVel"], axis=1)
    int_velN = np.nanmean(Data["NorthVel_interp"], axis=1)
    fig, axs = plt.subplots(2)
    axs[0].plot(Data["DateTime"], int_velN, color="green", label="File Processing")
    axs[1].plot(AutoData["DateTime"], auto_velN, label="Session Processing")
    fig.supxlabel("Time (DD HH:MM)")
    fig.supylabel("Velocity (m/s)")
    fig.suptitle("Northing Velocities vs Time")
    fig.legend()
    plt.show()


def depth_velocity_plot(Data):
    fig, axs = plt.subplots(3)

    im1 = axs[0].pcolormesh(
        Data["DateTime"],
        Data["interpCellDepth"],
        Data["EastVel_interp"].T,
        vmin=np.nanmin(Data["EastVel_interp"]),
        vmax=np.nanmax(Data["EastVel_interp"]),
        shading="auto",
    )
    im2 = axs[1].pcolormesh(
        Data["DateTime"],
        Data["interpCellDepth"],
        Data["NorthVel_interp"].T,
        vmin=np.nanmin(Data["NorthVel_interp"]),
        vmax=np.nanmax(Data["NorthVel_interp"]),
        shading="auto",
    )
    im3 = axs[2].pcolormesh(
        Data["DateTime"],
        Data["interpCellDepth"],
        Data["VertVel_interp"].T,
        vmin=np.nanmin(Data["VertVel_interp"]),
        vmax=np.nanmax(Data["VertVel_interp"]),
        shading="auto",
    )
    axs[0].plot(Data["DateTime"], Data["VbDepth_m"])
    axs[1].plot(Data["DateTime"], Data["VbDepth_m"])
    axs[2].plot(Data["DateTime"], Data["VbDepth_m"])

    axs[0].set_title("Easting Velocity")
    axs[1].set_title("Northing Velocity")
    axs[2].set_title("Vertical Velocity")
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



def Snr_plot(AutoData):
    plt.figure()
    plt.plot(AutoData["ADP_snr"][0][100])
    plt.title("ADP Signal to Noise ")
    plt.xlabel("Cell Number")
    plt.ylabel("Signal to Noise Ratio")
    plt.show()


def layer_data(LayerData): 
    plt.figure()
    plt.plot(LayerData["DateTime"], LayerData['average_E'], label="Easting")
    plt.plot(LayerData["DateTime"], LayerData['average_N'], label="Northing")
    plt.plot(LayerData["DateTime"], LayerData['average_U'], label="Vertical")
    plt.xlabel("Time (DD HH:MM)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Raw Velocities vs Time ~~Layer~~")
    plt.legend()
    plt.show()

raw_comparison_plot(Data)

# BT_comparison_plot(Data)

# auto_manual_comparison(AutoData, Data)

depth_velocity_plot(Data)

# Snr_plot(AutoData)

# layer_data(LayerData)
