from scipy.io import loadmat
import pandas as pd
import numpy as np

def read_Sig1k(filepath):
    Data = loadmat(filepath)
    for i in Data.keys():
        if i == Data :
           Data[i][0,0]
    return Data

Data = read_Sig1k(r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\S103080A002_testtest.mat")

print((Data['Units']))
#print(len(Data['Data'][0,0]))