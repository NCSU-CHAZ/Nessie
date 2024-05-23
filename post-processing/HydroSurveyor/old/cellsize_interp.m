function [vel_interp,interpCellDepth] = cellsize_interp(vel_array,CellSize_m,CellGrid,Interpsize)


% cellsize_interp takes a number of different bin sizes in a particular
% data stream as an input and interpolates them to the SMALLEST bin size

% CellGrid = an array including depths increasing by cell size at each time
% in a survey file
        % ex. for a time in a survey with a cell size of 0.200 m, the row
        % in cell grid would be [0.150 0.350 0.550 0.750 ...] (0.150 as the cell start depth)

% CellSize_m_ = a vector including increasing cell size at each time in
% a given data stream output by the Hydrosurveyor

% Interpsize = a number, 1-5 indicating which cell size the data should be
% interpolated to, 1 indicates the minimum cell size and is the default, 2 indicates the second smallest cell size, etc... 



dimensions = size(CellGrid);
dimension = dimensions(2); %cobtains number of cells
varCellSize = unique(CellSize_m); % Obtains all the unique cell sizes in a data set
varCellSize = varCellSize(2:end); % removes the smallest cell size from the variable

if Interpsize == 1 % interpolate to smallest cell size
    cellinds = find(CellSize_m == min(CellSize_m)); % Finds which times (indicies) crrespond to the minimum cell size
    varCellSize = varCellSize(2:end); % removes the smallest cell size from the variable
    interpCellDepth = CellGrid(cellinds(1),:); % Specifies the column in CellGrid where the data will be interpolated interpolated 
    % to (from the min cell size)


elseif Interpsize == 2
    cellinds = find(CellSize_m == varCellSize(2));
    varCellSize = varCellSize(varCellSize ~= varCellSize(2));
    interpCellDepth = CellGrid(cellinds(1),:); % Specifies the column in CellGrid where the data will be interpolated interpolated 
    % to (from the min cell size)

elseif Interpsize == 3
    cellinds = find(CellSize_m == varCellSize(3));
    varCellSize = varCellSize(varCellSize ~= varCellSize(3));
    interpCellDepth = CellGrid(cellinds(1),:); % Specifies the column in CellGrid where the data will be interpolated interpolated 
    % to (from the min cell size)

elseif Interpsize == 4
    cellinds = find(CellSize_m == varCellSize(4));
    varCellSize = varCellSize(varCellSize ~= varCellSize(4));
    interpCellDepth = CellGrid(cellinds(1),:); % Specifies the column in CellGrid where the data will be interpolated interpolated 
    % to (from the min cell size)

elseif Interpsize == 5
    cellinds = find(CellSize_m == varCellSize(5));
    varCellSize = varCellSize(varCellSize ~= varCellSize(5));
    interpCellDepth = CellGrid(cellinds(1),:); % Specifies the column in CellGrid where the data will be interpolated interpolated 
    % to (from the min cell size)

end


%%%%%%% if there are 2 total bin sizes follow this procedure (minimum and one other)
if length(varCellSize) == 1
    inds2 = find(CellSize_m == varCellSize(1)); % Finds all indicies not corresponding to the minimum bin size
    vel_interp = vel_array;

    for i = 1:length(inds2)
        loc = CellGrid(inds2(i),:);
        value = vel_interp(inds2(i),:);
        newloc = interpCellDepth;
        newval = interp1(loc(1:dimension),value,newloc);
        vel_interp(inds2(i),:) = newval;
    end



% if there are 3 bin sizes follow this procedure
elseif length(varCellSize) == 2
    inds2 = find(CellSize_m == varCellSize(1));
    inds3 = find(CellSize_m == varCellSize(2));
    vel_interp = vel_array;

    for i = 1:length(inds2)
        loc = CellGrid(inds2(i),:);
        value = vel_interp(inds2(i),:);
        newloc = interpCellDepth;
        newval = interp1(loc(1:dimension),value,newloc);
        vel_interp(inds2(i),:) = newval;
    end

    for i = 1:length(inds3);
        loc = CellGrid(inds3(i),:);
        value = vel_interp(inds3(i),:);
        newloc = interpCellDepth;
        newval = interp1(loc(1:dimension),value,newloc);
        vel_interp(inds3(i),:) = newval;
    end




% if there are 4 bin sizes follow this procedure
elseif length(varCellSize) == 3
    inds2 = find(CellSize_m == varCellSize(1));
    inds3 = find(CellSize_m == varCellSize(2));
    inds4 = find(CellSize_m == varCellSize(3));
    vel_interp = vel_array;

    for i = 1:length(inds2)
        loc = CellGrid(inds2(i),:);
        value = vel_interp(inds2(i),:);
        newloc = interpCellDepth;
        newval = interp1(loc(1:dimension),value,newloc);
        vel_interp(inds2(i),:) = newval;
    end

    for i = 1:length(inds3);
        loc = CellGrid(inds3(i),:);
        value = vel_interp(inds3(i),:);
        newloc = interpCellDepth;
        newval = interp1(loc(1:dimension),value,newloc);
        vel_interp(inds3(i),:) = newval;
    end

    for i = 1:length(inds4);
        loc = CellGrid(inds4(i),:);
        value = vel_interp(inds4(i),:);
        newloc = interpCellDepth;
        newval = interp1(loc(1:dimension),value,newloc);
        vel_interp(inds4(i),:) = newval;
    end



%%%%%%%%%%%%%%%  if there are 5 bin sizes follow this procedure  %%%%%%%%

elseif length(varCellSize) == 4
    inds2 = find(CellSize_m == varCellSize(1));
    inds3 = find(CellSize_m == varCellSize(2));
    inds4 = find(CellSize_m == varCellSize(3));
    inds5 = find(CellSize_m == varCellSize(4));
    vel_interp = vel_array;

    for i = 1:length(inds2)
        loc = CellGrid(inds2(i),:);
        value = vel_interp(inds2(i),:);
        newloc = interpCellDepth;
        newval = interp1(loc(1:dimension),value,newloc);
        vel_interp(inds2(i),:) = newval;
    end

    for i = 1:length(inds3);
        loc = CellGrid(inds3(i),:);
        value = vel_interp(inds3(i),:);
        newloc = interpCellDepth;
        newval = interp1(loc(1:dimension),value,newloc);
        vel_interp(inds3(i),:) = newval;
    end

    for i = 1:length(inds4);
        loc = CellGrid(inds4(i),:);
        value = vel_interp(inds4(i),:);
        newloc = interpCellDepth;
        newval = interp1(loc(1:dimension),value,newloc);
        vel_interp(inds4(i),:) = newval;
    end

    for i = 1:length(inds5);
        loc = CellGrid(inds5(i),:);
        value = vel_interp(inds5(i),:);
        newloc = interpCellDepth;
        newval = interp1(loc(1:dimension),value,newloc);
        vel_interp(inds5(i),:) = newval;
    end

    end

    end


