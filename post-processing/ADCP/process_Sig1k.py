from read_Sig1k import read_Sig1k
from math import floor
import datetime as dt 

def dtnum_dttime_adcp(time_array): #Create a function to convert from matlabs datenum format to python datetime
    dates = []  #Initialize dates#Convert the awkward structure intoa matlab array
    DT = time_array.to_numpy() #Dataframes behave strangely for some reason
    for ordinal in DT:
        integer = floor(ordinal[0]) #Round down to the nearest whole number on the datetime 
        frac = ordinal - integer #Get just the decimal points 
        date = dt.datetime.fromordinal(integer) #This function only takes integer values so we must add the decimal on after the conversion
        time = dt.timedelta(days=frac[0]) #Convert the decimals into hours, min, seconds, microseconds, ect.
        mat_correction = dt.timedelta(days=366) #Matlab datenum starts from Jan 1 0000AD, this year is 366 days long,
                                                #while ordinal time which is what we are converting from starts Jan 1 0001AD 
        full = date + time - mat_correction  # Recombine the fractional precision and correct fro the year difference between ordinal and dateum
        dates.append(full) #Append the correct datetime back into the dates array
    return dates; """This entire loop is very inefficient, while take time for large data sets
                     but this is the best I have figured out at the time of creating this"""

def process(filepath):
    Data = read_Sig1k(filepath) #Load in file

    Data['IBurst_Time'] = dtnum_dttime_adcp(Data['IBurst_Time'])

    return Data


Data = process(r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\S103080A002_testtest.mat")