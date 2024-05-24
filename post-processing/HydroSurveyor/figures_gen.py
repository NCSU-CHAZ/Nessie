from data_process import post_process
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

EastVel, NorthVel, VertVel, rawdata = post_process(r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Survey_ICW_20240520_raw.mat")


plt.figure()
plt.plot(NorthVel)
plt.show()
