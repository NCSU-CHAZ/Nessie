%% Hyrdosurveyor Analysis


% Cory Toburen 


clear;clc;close all


%% Load in Data
% need full path to the "exported" .mat file from
% hydrosurveyor software (we need to modify this
% workflow to use the "session" data instead).
 load("C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Survey_ICW_20240520_raw.mat") % --- Exported File


%% Edit DateTime Variable
% time base uses a Julien date of: 
t0 = datenum('Jan 01 2000');

% Convert from Hydrosurveyor time (micro-seconds since t0)
% to matlab datetime format
DateTime = t0 + DateTime/1e6/86400;
DateTime = datetime(DateTime,'ConvertFrom','datenum');
% Convert from UTC to EDT (we may want to keep UTC)
DateTime = DateTime - hours(4);


%% Account for Bottom Tracking Velocity

dim = size(WaterVelEnu_m_s); % Size of the variables 


% Creates Velocity and Bottom Track ENU/error variables 

BtVelE = repmat(BtVelEnu_m_s(:,1),1,dim(2));
BtVelN = repmat(BtVelEnu_m_s(:,2),1,dim(2));
BtVelU = repmat(BtVelEnu_m_s(:,3),1,dim(2));
BtVelErr = repmat(BtVelEnu_m_s(:,4),1,dim(2));


% Subtract Bottom Track from Velocity

Vel_East = WaterVelEnu_m_s(:,:,1) - BtVelE;
Vel_North = WaterVelEnu_m_s(:,:,2) - BtVelN;
Vel_Vert = WaterVelEnu_m_s(:,:,3)- BtVelU;
Vel_Err = WaterVelEnu_m_s(:,:,4)- BtVelErr;


%% Remove data below Vertical Beam Range

% Creates a matrix with increasing depth based on cell size at each time,
% starting with the cell start distance
ii = 1:length(CellSize_m);
CellGrid = (CellStart_m+[0:dim(2)-1].*CellSize_m);
CellGrid = CellGrid+0.1651; % Add transducer depth to cell matrix

dim = size(WaterVelEnu_m_s); % Size of the variables 


% Remove data below VB range
isbad = (CellGrid > repmat(VbDepth_m,1,dim(2)));

Vel_East(isbad) = nan;
Vel_North(isbad) = nan;
Vel_Vert(isbad) = nan;
Vel_Err(isbad) = nan;


%% Interpolate to a Uniform Grid

varCellSize = unique(CellSize_m);

[vel_interp_e,interpCellDepth] = cellsize_interp(Vel_East,CellSize_m,CellGrid,2);
[vel_interp_n,interpCellDepth] = cellsize_interp(Vel_North,CellSize_m,CellGrid,2);
[vel_interp_u,interpCellDepth] = cellsize_interp(Vel_Vert,CellSize_m,CellGrid,2);

Vel_East = vel_interp_e;
Vel_North = vel_interp_n;
Vel_Vert = vel_interp_u;

%%

% $$$ return



save('HydroAnalysisExp')




