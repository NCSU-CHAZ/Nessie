from process_HydroSurveyor import Hydro_process
import matplotlib.pyplot as plt
from read_HydroSurveyor import create_df
import numpy as np
from process_HydroSurveyor import dtnum_dttime
import pandas as pd

Data = Hydro_process(r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Survey_ICW_20240520_raw.mat")

AutoData, gg = create_df(r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Survey_ICW_20240520.mat")

AdcpData, gg = create_df(r"c:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\CMS52002_L0.mat")

#MatVel,info = create_df(r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\HydroAnalysisExp.mat"); del info

def raw_comparison_plot(Data):
    raw_velE = np.nanmean(Data['EastVel'],axis = 1)
    raw_velN = np.nanmean(Data['NorthVel'], axis = 1)
    raw_velU = np.nanmean(Data['VertVel'], axis =1)

    plt.figure()
    plt.plot(Data['DateTime'], raw_velE, label = 'Easting')
    plt.plot(Data['DateTime'], raw_velN, label = 'Northing')
    plt.plot(Data['DateTime'], raw_velU, label = 'Vertical')
    plt.xlabel("Time (DD HH:MM)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Raw Velocities vs Time")
    plt.legend()
    plt.show()

def interpolated_comparison_plot(Data):
    int_velE = np.nanmean(Data['EastVel_interp'],axis = 1)
    int_velN = np.nanmean(Data['NorthVel_interp'], axis = 1)
    int_velU = np.nanmean(Data['VertVel_interp'], axis =1)
    
    plt.figure()
    plt.plot(Data['DateTime'], int_velE, label = 'Easting')
    plt.plot(Data['DateTime'], int_velN, label = 'Northing')
    plt.plot(Data['DateTime'], int_velU, label = 'Vertical')
    plt.xlabel("Time (DD HH:MM)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Interpolated Velocities vs Time")
    plt.legend()
    plt.show()

def auto_manual_comparison(AutoData, Data):
    auto_velN = np.nanmean(AutoData['HydroSurveyor_WaterVelocityXyz_Corrected_m_s'].iloc[:, 1::4], axis=0)
    int_velN = np.nanmean(Data['NorthVel_interp'], axis =1)
    DT = dtnum_dttime(AutoData['HydroSurveyor_WaterVelocityXyz_Corrected_DateTime'])
    fig, axs = plt.subplots(2)
    axs[0].plot(Data['DateTime'], int_velN,color = 'green', label = 'CHAZ Processing')
    axs[1].plot(DT, auto_velN, label = 'HydroSurveyors Processing')
    fig.supxlabel("Time (DD HH:MM)")
    fig.supylabel("Velocity (m/s)")
    fig.suptitle("Interpolated Velocities vs Time")
    fig.legend()
    plt.show()

def error_plots(AutoData, Data) :
    DT = dtnum_dttime(AutoData['HydroSurveyor_WaterVelocityXyz_Corrected_DateTime'])
    WaterErr = np.nanmean(Data['WaterErrVal'],axis=1)
    HydroErr = np.nanmean(AutoData['HydroSurveyor_WaterVelocityXyz_Corrected_m_s'].iloc[:, 3::4], axis = 0)
    plt.figure()
    plt.plot(Data['DateTime'], WaterErr,color = 'Green', label = 'WaterVelocity Error')
    plt.plot(Data['DateTime'], Data['BtErrVal'], color = 'Blue', label = 'Bottom Track Error')
    plt.plot(DT, HydroErr, label = 'HydroSurveyor Error')
    plt.legend()
    plt.show()

def depth_velocity_plot(Data) :
    fig, axs = plt.subplots(3)
    
    im1 = axs[0].pcolormesh(Data['DateTime'],Data['interpCellDepth'],Data['EastVel_interp'].T, vmin=np.nanmin(Data['EastVel_interp']),
                   vmax=np.nanmax(Data['EastVel_interp']),shading = 'auto')
    im2 = axs[1].pcolormesh(Data['DateTime'],Data['interpCellDepth'],Data['NorthVel_interp'].T, vmin=np.nanmin(Data['NorthVel_interp']),
                   vmax=np.nanmax(Data['NorthVel_interp']),shading = 'auto')
    im3 = axs[2].pcolormesh(Data['DateTime'],Data['interpCellDepth'],Data['VertVel_interp'].T, vmin=np.nanmin(Data['VertVel_interp']),
                   vmax=np.nanmax(Data['VertVel_interp']),shading = 'auto')
    axs[0].plot(Data['DateTime'],Data['VbDepth_m'])
    axs[1].plot(Data['DateTime'],Data['VbDepth_m'])
    axs[2].plot(Data['DateTime'],Data['VbDepth_m'])

    axs[0].set_title('Easting Velocity'); axs[1].set_title('Northing Velocity'); axs[2].set_title('Vertical Velocity')
    cb1 = fig.colorbar(im1,ax = axs[0]); cb2 = fig.colorbar(im2,ax = axs[1]); cb3 = fig.colorbar(im3,ax = axs[2])
    cb1.ax.set_ylabel('Velocity (m/s)'); cb2.ax.set_ylabel('Velocity (m/s)'); cb3.ax.set_ylabel('Velocity (m/s)')
    fig.tight_layout()
    fig.supxlabel('DateTime (DD HH:MM)')
    fig.supylabel('Depth (m)')
    plt.show()

def adcp_comparison(AdcpData,Data) :
    plt.figure()
    plt.plot(np.nanmean(AdcpData['VelNorth'], axis =0))
    plt.plot(np.nanmean(Data['NorthVel'], axis=0))
    plt.show()
#raw_comparison_plot(Data)

#interpolated_comparison_plot(Data)

#auto_manual_comparison(AutoData, Data)

#error_plots(AutoData, Data)

depth_velocity_plot(Data)

#adcp_comparison(AdcpData,Data)