from scipy.io import loadmat
import pandas as pd

#Import .mat files 
def create_df(filepath) :
        rawdata = loadmat(filepath)            #Load in filepath, make sure you put an r out front r"placeholder/placeholder/placeholder.mat" so python
                                               # interprets the backslashes correctly
        del rawdata['__header__'] ; del rawdata['__version__'] ; del rawdata['__globals__']; #Delete unnecessary keys that list info about the function
        data = {} #Initialize data dictionary to place data into 
        Info = None #Initialize info as None
        for i in rawdata.keys() : #Run through loop where i is the key to the array in the dictionary
                array = rawdata[i]  #Initialize a a duplicate array to allow for reshaping 
                if rawdata[i].ndim == 3 :      #Flatten 3d arrays into 2d arrays, this causes an 3577x85x4 array to become 3577x340
                        reshaped = array.reshape(array.shape[0],-1)   
                        data[i] = pd.DataFrame(reshaped)       #Save the data into the dictionary as a dataframe, dataframes are one of the many ways to 
                                                               #store data in python
                elif i == 'Info' :             #The info structure does not transfer well between MATLAB and Python but contains relevant data so we just 
                                                          #make a 1 to 1 copy
                        Info = array     
                elif i == 'config':             #The info structure does not transfer well between MATLAB and Python but contains relevant data so we just 
                                                          #make a 1 to 1 copy
                        Info = array  
                else :                         #All 2d arrays get stored as a dataframe, this is the majority of data arrays in the structure
                        data[i] = pd.DataFrame(array)
        return data , Info

#Function that uses the previous readin function to acquire the data, and then any further processing to store the variables in a favorable way 
def vector_df(filepath) :                     
        data, Info = create_df(filepath)
        #Acquire individual direction dataframes
        WaterEastVel = data['WaterVelEnu_m_s'].iloc[:, 0::4] #3557x340 matrix gets sorted for every fourth column, 
        WaterVertVel = data['WaterVelEnu_m_s'].iloc[:, 2::4] #this pulls out the individual ENU and Error columns for each of the 85 cells
        WaterNorthVel = data['WaterVelEnu_m_s'].iloc[:,1::4] 
        WaterErrVel = data['WaterVelEnu_m_s'].iloc[:, 3::4] 
        rawdata = data  
        return rawdata, WaterEastVel, WaterNorthVel, WaterVertVel, WaterErrVel, Info
