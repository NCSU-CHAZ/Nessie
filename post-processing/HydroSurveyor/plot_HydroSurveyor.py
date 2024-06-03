from process_HydroSurveyor import Hydro_process
import matplotlib.pyplot as plt
from read_HydroSurveyor import create_df
import numpy as np
from process_HydroSurveyor import dtnum_dttime

Data = Hydro_process(r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Survey_ICW_20240520_raw.mat")

AutoData, gg = create_df(r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Survey_ICW_20240520.mat")

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
    err = np.nanmean(AutoData['HydroSurveyor_AdpSnr_dB'])
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


print(AutoData.keys())

#raw_comparison_plot(Data)

#interpolated_comparison_plot(Data)

#auto_manual_comparison(AutoData, Data)

#error_plots(AutoData, Data)

