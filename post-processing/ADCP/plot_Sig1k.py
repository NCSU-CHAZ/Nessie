from process_Sig1k import process
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

Data = process(r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\S103080A004_ICW_test.mat")

def RawVel_plotter(Data):
    
    plt.figure()
    plt.plot(Data['Burst_Time'],np.nanmean(Data['EastVel'], axis = 1), color = 'green')
    plt.plot(Data['Burst_Time'],np.nanmean(Data['NorthVel'], axis = 1), color = 'red')
    plt.plot(Data['Burst_Time'],np.nanmean(Data['VertVel1'], axis = 1), color = 'blue')
    plt.plot(Data['Burst_Time'],np.nanmean(Data['VertVel2'], axis = 1), color ='gray')
    plt.xlim(left = dt.datetime(2024,6,24,12,25),right = dt.datetime(2024,6,24,15,00))
    plt.ylim(top = 2, bottom = -2)
    plt.show()

RawVel_plotter(Data)

