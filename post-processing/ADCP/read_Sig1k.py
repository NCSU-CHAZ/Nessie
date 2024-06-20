from scipy.io import loadmat
import pandas as pd
import numpy as np

# This code generates a dicionary containing all of the quantitative data exported by the Nortek Signature Deployment,

""""The keys for the dictionary are 
'BurstRawAltimeter_Time', 'BurstRawAltimeter_Status', 'BurstRawAltimeter_ExtStatus', 'BurstRawAltimeter_Error', 
'BurstRawAltimeter_EnsembleCount', 'BurstRawAltimeter_NBeams', 'BurstRawAltimeter_NCells', 'BurstRawAltimeter_BeamToChannelMapping',
'BurstRawAltimeter_AmbiguityVel', 'BurstRawAltimeter_AltimeterDistanceLE', 'BurstRawAltimeter_AltimeterQualityLE',
'BurstRawAltimeter_AltimeterStatus', 'BurstRawAltimeter_AltimeterDistanceAST', 'BurstRawAltimeter_AltimeterQualityAST', 
'BurstRawAltimeter_AltimeterTimeOffsetAST', 'BurstRawAltimeter_AltimeterPressure', 'BurstRawAltimeter_AmpBeam5', 
'BurstRawAltimeter_Battery', 'BurstRawAltimeter_Heading', 'BurstRawAltimeter_Pitch', 'BurstRawAltimeter_Roll', 
'BurstRawAltimeter_Temperature', 'BurstRawAltimeter_Soundspeed', 'BurstRawAltimeter_Pressure',
'BurstRawAltimeter_PressureSensorTemperature', 'BurstRawAltimeter_RTCTemperature', 'BurstRawAltimeter_MagnetometerTemperature', 
'BurstRawAltimeter_TransmitEnergy', 'BurstRawAltimeter_Magnetometer', 'BurstRawAltimeter_Accelerometer',
'BurstRawAltimeter_NominalCorrelation', 

'IBurst_Time', 'IBurst_Status', 'IBurst_ExtStatus', 'IBurst_Error', 
'IBurst_EnsembleCount', 'IBurst_NBeams', 'IBurst_NCells', 'IBurst_BeamToChannelMapping', 'IBurst_AmbiguityVel', 
'IBurst_VelBeam5', 'IBurst_AmpBeam5', 'IBurst_CorBeam5', 'IBurst_Battery', 'IBurst_Heading', 'IBurst_Pitch', 'IBurst_Roll',
'IBurst_Temperature', 'IBurst_Soundspeed', 'IBurst_Pressure', 'IBurst_PressureSensorTemperature', 'IBurst_RTCTemperature', 
'IBurst_MagnetometerTemperature', 'IBurst_TransmitEnergy', 'IBurst_Magnetometer', 'IBurst_Accelerometer','IBurst_NominalCorrelation', 

'Burst_Time', 'Burst_Status', 'Burst_ExtStatus', 'Burst_Error', 'Burst_EnsembleCount',
'Burst_NBeams', 'Burst_NCells', 'Burst_BeamToChannelMapping', 'Burst_AmbiguityVel', 'Burst_VelBeam1', 'Burst_VelBeam2', 
'Burst_VelBeam3', 'Burst_VelBeam4', 'Burst_AmpBeam1', 'Burst_AmpBeam2', 'Burst_AmpBeam3', 'Burst_AmpBeam4', 'Burst_CorBeam1', 'Burst_CorBeam2', 'Burst_CorBeam3', 'Burst_CorBeam4',
'Burst_AltimeterDistanceLE', 'Burst_AltimeterQualityLE', 'Burst_AltimeterStatus', 'Burst_AltimeterDistanceAST', 'Burst_AltimeterQualityAST', 
'Burst_AltimeterTimeOffsetAST','Burst_AltimeterPressure', 'Burst_Battery', 'Burst_Heading', 'Burst_Pitch', 'Burst_Roll',
'Burst_Temperature', 'Burst_Soundspeed','Burst_Pressure', 'Burst_PressureSensorTemperature', 'Burst_RTCTemperature', 'Burst_MagnetometerTemperature',
'Burst_TransmitEnergy', 'Burst_Magnetometer', 'Burst_Accelerometer', 'Burst_NominalCorrelation',

'Echo1Bin1_1000kHz_Time', 'Echo1Bin1_1000kHz_Status', 'Echo1Bin1_1000kHz_ExtStatus', 'Echo1Bin1_1000kHz_Error', 'Echo1Bin1_1000kHz_EnsembleCount', 
'Echo1Bin1_1000kHz_NBeams', 'Echo1Bin1_1000kHz_NCells', 'Echo1Bin1_1000kHz_BeamToChannelMapping', 'Echo1Bin1_1000kHz_Frequency', 
'Echo1Bin1_1000kHz_Echo', 'Echo1Bin1_1000kHz_Battery', 'Echo1Bin1_1000kHz_Heading', 'Echo1Bin1_1000kHz_Pitch', 
'Echo1Bin1_1000kHz_Roll', 'Echo1Bin1_1000kHz_Temperature', 'Echo1Bin1_1000kHz_Soundspeed', 'Echo1Bin1_1000kHz_Pressure', 
'Echo1Bin1_1000kHz_PressureSensorTemperature', 'Echo1Bin1_1000kHz_RTCTemperature', 'Echo1Bin1_1000kHz_MagnetometerTemperature', 
'Echo1Bin1_1000kHz_TransmitEnergy', 'Echo1Bin1_1000kHz_Magnetometer', 'Echo1Bin1_1000kHz_Accelerometer', 
'Echo1Bin1_1000kHz_NominalCorrelation', 'Echo2Bin1_1000kHz_Time', 'Echo2Bin1_1000kHz_Status', 'Echo2Bin1_1000kHz_ExtStatus', 
'Echo2Bin1_1000kHz_Error', 'Echo2Bin1_1000kHz_EnsembleCount', 'Echo2Bin1_1000kHz_NBeams', 'Echo2Bin1_1000kHz_NCells', 
'Echo2Bin1_1000kHz_BeamToChannelMapping', 'Echo2Bin1_1000kHz_Frequency', 'Echo2Bin1_1000kHz_Echo', 'Echo2Bin1_1000kHz_Battery', 
'Echo2Bin1_1000kHz_Heading', 'Echo2Bin1_1000kHz_Pitch', 'Echo2Bin1_1000kHz_Roll', 'Echo2Bin1_1000kHz_Temperature',
'Echo2Bin1_1000kHz_Soundspeed', 'Echo2Bin1_1000kHz_Pressure', 'Echo2Bin1_1000kHz_PressureSensorTemperature', 
'Echo2Bin1_1000kHz_RTCTemperature', 'Echo2Bin1_1000kHz_MagnetometerTemperature', 'Echo2Bin1_1000kHz_TransmitEnergy', 
'Echo2Bin1_1000kHz_Magnetometer', 'Echo2Bin1_1000kHz_Accelerometer', 'Echo2Bin1_1000kHz_NominalCorrelation'"""


def read_Sig1k(filepath):  # Create read function
    Data = loadmat(
        filepath
    )  # Load mat oragnizes the 4 different data structures of the .mat file (Units, Config, Data, Description) as a
       #dictionary with four nested numpy arrays with dtypes as data field titles 
    ADCPData = {} #Initialize the dictionary we'll use
    DTypes = Data["Data"][0, 0].dtype #Acquire the dtypes for the data field keys
    keys = DTypes.names #Initialize the keys
    for i in range(0, len(Data["Data"][0, 0])):
        ADCPData[str(keys[i])] = pd.DataFrame(Data["Data"][0, 0][i]) #Iterate through the nested numpy arrays turning each 
                                                                     #individual array into a dataframe and saving it to it's key
    return ADCPData
