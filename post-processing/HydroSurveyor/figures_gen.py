from data_process import post_process
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

EastVel, NorthVel, VertVel, rawdata = post_process(r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Survey_ICW_20240520_raw.mat")

python_datetime = datetime.fromordinal(int()) + timedelta(days=rawdata['DateTime'].to_string()%1) - timedelta(days = 366)

plt.figure()
plt.plot(python_datetime,EastVel)
plt.show()
