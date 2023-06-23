%% Hydrosurvyeor Flume Test
%% Cory Toburen
clear;clc;

%% Load in Data from Excel


trial1 = readtable('Trial1data.xlsx');
trial2 = readtable('Trial2data.xlsx');
trial3 = readtable('Trial3data.xlsx');
trial4 = readtable('Trial4data.xlsx');

% Create a vertical beam range variable which includes the range collected 
% over the four minute timespan for each of the three trials (cm)
VB_range{1} = trial1.VBDepth_m_(1:241)*100; 

VB_range{2} = trial2.VBDepth_m_(1:241)*100;

VB_range{3} = trial3.VBDepth_m_(1:241)*100;


%Exclude 4th trial due to bottom being out of range of ADCP measurement 
% (too shallow)
% % % %VB_range{4} = trial4.VBDepth_m_(1:328);
% % % 
% % % %VB_range{4}(isnan(VB_range{4}))=[]

% Water Depth measured with tape measure in cm 
meas_wdepth = [1.01 .97 .84 NaN]*100; 

%Distance from the wave maker in cm
x_dist = [10 11.4 12.4 13.3]*100; 

% Depth measured from the bottom of the ADCP with tape measure
meas_depth = [0.648 0.608 0.478]*100; %cm

% Create variable including the mean depths measured from the ADCP vertical
% beam
for i = 1:3
    VB_mean(i) = mean(VB_range{i});
end


 


% Depth measured vs x distance (not super useful)
% % % % figure(1);clf;
% % % % plot(x_dist(1:3),VB_mean(1:3),'k*','MarkerSize',15)
% % % % hold on
% % % % plot(x_dist(4),VB_mean(4),'r*','MarkerSize',15)
% % % % 
% % % % set(gca, 'YDir','reverse')
% % % % xlim([9.5 13.5])
% % % % grid on





%% STD and mean of Vertical Beam

% Calculate the Vertical beam STD for each of the trials 

for i = 1:3
    VB_STD(i) = std(VB_range{i});
    VB_meanSTD{i} = [VB_mean(i)-VB_STD(i),VB_mean(i)+VB_STD(i)];
end

% Linear regression performed--> decided to use a 1:1 line as oppposed to
% linear regression to compare data
 p = polyfit(VB_mean(1:3),meas_depth,1); % least squares regression
% x = [0.45:0.01:0.7];
% y = .9716*x+0.0137;


% Figure including the recorded avg depth vs the measuered depth in m,
% also inlcuides line of y=x and the STD range
figure(22);clf;
plot([45 70],[45 70],'r--','LineWidth',2.2)
hold on
plot(VB_mean(1:3),meas_depth,'ko','markersize',10,'linewidth',2.5)
grid on

for i = 1:3
    plot([VB_meanSTD{i}(1) VB_meanSTD{i}(2)],[meas_depth(i) meas_depth(i)],'k-')
end

xlabel('Recorded Average Depth (cm)','FontSize',18)
ylabel('Measured Depth (cm)','FontSize',18)
legend('y = x','Recorded Average vs Measured Depth','STD Range','Location','Northwest','FontSize',18)
title('Wave Flume Test','FontSize',18)


%% Slanted Beams 1-4 water depth analysis (3 MHz)

%-------------------------------------------
% Trial 1

% Creates a variable including the trial ONE depth for all four slanted
% beams accounting for 25 degree tilt of beams (*cosd(25) to yield depth as
% opposed to beam range)

t1beamranges = {trial1.BTBeam1Range_m_*cosd(25)*100,trial1.BTBeam2Range_m_*cosd(25)*100,...
    trial1.BTBeam3Range_m_*cosd(25)*100,trial1.BTBeam4Range_m_*cosd(25)*100}; %cm

% Take the MEDIAN value for each of the trials 
mediant1b1 = nanmedian(t1beamranges{1}); 
mediant1b2 = nanmedian(t1beamranges{2});
mediant1b3 = nanmedian(t1beamranges{3});
mediant1b4 = nanmedian(t1beamranges{4});

mediant1beamranges = [mediant1b1 mediant1b2 mediant1b3 mediant1b4]'; % 
% rows 1-4 = beams 1-4

% Calculate the standard deviation of each beam (rows 1-4 = beams 1-4)
trial1beamSTD = [nanstd(t1beamranges{1}),nanstd(t1beamranges{2}), ...
    nanstd(t1beamranges{3}), nanstd(t1beamranges{4})]';



%-------------------------------------------
% Trial 2 

% Creates a variable including the trial TWO depth for all four slanted
% beams accounting for 25 degree tilt of beams (*cosd(25) to yield depth as
% opposed to beam range)

t2beamranges = {trial2.BTBeam1Range_m_*cosd(25)*100,trial2.BTBeam2Range_m_*cosd(25)*100,...
    trial2.BTBeam3Range_m_*cosd(25)*100,trial2.BTBeam4Range_m_*cosd(25)*100}; %cm

% Take the MEDIAN value for each of the trials
mediant2b1 = nanmedian(t2beamranges{1}); 
mediant2b2 = nanmedian(t2beamranges{2});
mediant2b3 = nanmedian(t2beamranges{3});
mediant2b4 = nanmedian(t2beamranges{4});
mediant2beamranges = [mediant2b1 mediant2b2 mediant2b3 mediant2b4]';
% rows 1-4 = beams 1-4

% Calculate the standard deviation of each beam (rows 1-4 = beams 1-4)
trial2beamSTD = [nanstd(t2beamranges{1}),nanstd(t2beamranges{2}), ...
    nanstd(t2beamranges{3}), nanstd(t2beamranges{4})]';



%-------------------------------------------
% Trial 3

% Creates a variable including the trial THREE depth for all four slanted
% beams accounting for 25 degree tilt of beams (*cosd(25) to yield depth as
% opposed to beam range)

t3beamranges = {trial3.BTBeam1Range_m_*cosd(25)*100,trial3.BTBeam2Range_m_*cosd(25)*100,...
    trial3.BTBeam3Range_m_*cosd(25)*100,trial3.BTBeam4Range_m_*cosd(25)*100}; %cm

% Take the MEDIAN value for each of the trials
mediant3b1 = nanmedian(t3beamranges{1}); 
mediant3b2 = nanmedian(t3beamranges{2});
mediant3b3 = nanmedian(t3beamranges{3});
mediant3b4 = nanmedian(t3beamranges{4});
mediant3beamranges = [mediant3b1 mediant3b2 mediant3b3 mediant3b4]';
% rows 1-4 = beams 1-4

% Calculate the standard deviation of each beam (rows 1-4 = beams 1-4)
trial3beamSTD = [nanstd(t3beamranges{1}),nanstd(t3beamranges{2}), ...
    nanstd(t3beamranges{3}), nanstd(t3beamranges{4})]';



%Add the median beam ranges and beam ranges into a cell array useful in 
% the following for loop
medianbeamranges = {mediant1beamranges;mediant2beamranges;mediant3beamranges};
beamranges = {t1beamranges',t2beamranges',t3beamranges'};




% Plot four subplots (one per beam) on each figure (one per trial) 
% including:

% 1. Each trial's Vertical beam range
% 2. Each slanted beam's range for the specified trial
% 3. Each slanted beam's median range value for the specified trial
for j = 1:3
    figure(j);clf;
    for i = 1:4
        subplot(2,2,i)
        plot(VB_range{j},'LineWidth',3) % VB depth
        hold on
        plot(beamranges{j}{i},'.')
        yline(medianbeamranges{j}(i),'LineWidth',3)
 
    end
end


% Alter axis limits/add axis titles/legend
%--------------------------------------------------

figure(1)
sgtitle('Wave Flume Trial 1')
for i = 1:4
    subplot(2,2,i)
    ylim([50 250])
    xlim([1 240])
    ylabel('Depth Range (cm)')
    xlabel('Time (s)')

    std1 = [48.5 44.5 37.1 82.0];
    leg2 = ['BT beam ',num2str(i),' Range (STD = ',num2str(std1(i)),' cm)'];
    leg3 = ['Median beam ',num2str(i),' Range'];
    legend('Vertical Beam Range',leg2,leg3)
    grid on
end

subplot(224)
ylim([50 350])
%--------------------------------------------------

figure(2)
sgtitle('Wave Flume Trial 2')
for i = 1:4
    subplot(2,2,i)
    ylim([50 175])
    xlim([1 240])
    ylabel('Depth Range (cm)')
    xlabel('Time (s)')

    std2 = [34.5 39.0 35.7 93.7];
    leg2 = ['BT beam ',num2str(i),' Range (STD = ',num2str(std2(i)),' cm)'];
    leg3 = ['Median beam ',num2str(i),' Range'];
    legend('Vertical Beam Range',leg2,leg3)
    grid on
end

subplot(224)
ylim([50 400])
%--------------------------------------------------

figure(3)
sgtitle('Wave Flume Trial 3')
for i = 1:4
    subplot(2,2,i)
    ylim([40 100])
    xlim([1 240])
    ylabel('Depth Range (cm)')
    xlabel('Time (s)')

    std3 = [9.37 19.6 19.3 62.8];
    leg2 = ['BT beam ',num2str(i),' Range (STD = ',num2str(std3(i)),' cm)'];
    leg3 = ['Median beam ',num2str(i),' Range',];
    legend('Vertical Beam Range',leg2,leg3)
    grid on
end

subplot(224)
ylim([30 250])







