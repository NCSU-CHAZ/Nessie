from post_processing.HydroSurveyor.process_file_HydroSurveyor import Hydro_process
import matplotlib.pyplot as plt
from post_processing.HydroSurveyor.process_session_HydroSurveyor import Hydro_session_process 
from scipy.signal import medfilt
from post_processing.HydroSurveyor.read_HydroSurveyor import vector_df
import pandas as pd
import datetime as dt
import numpy as np

Data = Hydro_process(
    r'C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\2024_08_30_Surfzone\File'
)

AutoData = Hydro_session_process(
    r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\2024_08_30_Surfzone\Session"
)

plt.figure()
plt.plot(Data['DateTime'])
plt.show()

plt.figure()
plt.plot(AutoData["DateTime"])
plt.show()

