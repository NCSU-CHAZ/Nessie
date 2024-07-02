from process_Sig1k import process
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

Data = process(
    r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\S103080A004_ICW_test.mat"
)


def RawVel_plotter(Data):

    plt.figure()
    plt.plot(
        Data["Burst_Time"],
        np.nanmean(Data["EastVel"], axis=1),
        color="green",
        label="East",
    )
    plt.plot(
        Data["Burst_Time"],
        np.nanmean(Data["NorthVel"], axis=1),
        color="red",
        label="North",
    )
    plt.plot(
        Data["Burst_Time"],
        np.nanmean(Data["VertVel1"], axis=1),
        color="blue",
        label="VertVel1",
    )
    plt.plot(
        Data["Burst_Time"],
        np.nanmean(Data["VertVel2"], axis=1),
        color="gray",
        label="VertVel2",
    )
    plt.xlim(
        left=dt.datetime(2024, 6, 24, 13, 25), right=dt.datetime(2024, 6, 24, 13, 26)
    )
    plt.ylim(top=1, bottom=-1)
    plt.legend()
    plt.title("Different Velocities versus Time")
    plt.xlabel("Time (DD HH:MM)")
    plt.ylabel("Velocity (m/s)")
    plt.show()


def DepthAvg_plotter(Data):
    plt.figure()
    plt.pcolormesh(
        Data["Burst_Time"],
        Data["CellDepth"],
        Data["NorthVel"].T,
        vmin=0.3 * np.nanmin(Data["NorthVel"]),
        vmax=0.3 * np.nanmax(Data["NorthVel"]),
        shading="nearest",
        cmap="inferno",
    )
    plt.xlim(
        left=dt.datetime(2024, 6, 24, 12, 25), right=dt.datetime(2024, 6, 24, 15, 00)
    )
    plt.xlabel("Date (DD HH:MM)")
    plt.ylabel("Depth m")
    im1 = plt.colorbar()
    im1.ax.set_ylabel("Velocity (m/s)")
    plt.show()


def hist_plotter(Data):
    plt.figure()
    plt.hist(Data["Burst_VelBeam1"][18000:18100])
    plt.show()


# RawVel_plotter(Data)

# DepthAvg_plotter(Data)

# hist_plotter(Data)
