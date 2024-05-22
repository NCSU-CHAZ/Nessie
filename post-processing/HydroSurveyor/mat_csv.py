import numpy as np 
from scipy.io import loadmat
import pandas as pd
import datetime as time
import pytest
import matplotlib.pyplot as plt

#Import .mat files 
test = loadmat(r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Survey_ICW_20240520_raw.mat")

print(test['Info'].view)