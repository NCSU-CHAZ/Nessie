%% Hydrosurveyor Analysis Figs

% Cory Toburen

%% Load in mat file 
% make this the full path of file saved by "HydrosurveyorProcessing.m"
load('HydroAnalysisExp.mat'); 



%% Note: To Save Figures




% exportgraphics(gcf,'/Users/corytoburen/OneDrive - UNC-Wilmington/2023 Summer Internship/HydrosurveyorTests/HydrosurveyorVSadcp.png')






%% Plot HS vs ADCP (Raw, BT, ADCP)


% Raw
RawVeast = WaterVelEnu_m_s(:,:,1);
RawVnorth = WaterVelEnu_m_s(:,:,2);
RawVup = WaterVelEnu_m_s(:,:,3);
RawVerr = WaterVelEnu_m_s(:,:,4);

RawVeast(isbad) = nan;
RawVnorth(isbad) = nan;
RawVup(isbad) = nan;
RawVerr(isbad) = nan;

DA_u = nanmean(RawVeast');
DA_v = nanmean(RawVnorth');


% BT accounted


DepAvgVel_East = nanmean(Vel_East');
DepAvgVel_North = nanmean(Vel_North');



%% Load in ADCP stuff
% needs to be the full path to the aquadopp data. 
load('CMS52002_L0.mat')

ADCP_vel_east_DA = nanmean(v1');
ADCP_vel_east_DA(5000:end) = nan;


ADCP_vel_north_DA = nanmean(v2');
ADCP_vel_north_DA(5000:end) = nan;

DATE = datetime(date,'ConvertFrom','datenum');
figure(1);clf;

subplot(311)
plot(DateTime,DA_u,'k',LineWidth=2)
ylabel('Depth Avg Vel E',FontSize=14)
hold on;plot(DateTime,DepAvgVel_East,'r',LineWidth=2.5)
plot(DATE,ADCP_vel_east_DA,'b',LineWidth=1)
grid on
title('Velocity East',FontSize=14)
legend('Raw','BT Corrected','ADCP Measured','FontSize',14,'Location','Northwest')

subplot(312)
plot(DateTime,DA_v,'k',LineWidth=2)
ylabel('Depth Avg Vel N',FontSize=14)
hold on;plot(DateTime,DepAvgVel_North','r',LineWidth=2.5)
plot(DATE,ADCP_vel_north_DA,'b',LineWidth=1)
title('Velocity North',FontSize=14)
grid on
legend('Raw','BT Corrected','ADCP Measured','FontSize',14,'Location','Northwest')


subplot(313)
ylabel('Depth Avg Vel N',FontSize=14)
plot(DateTime,DepAvgVel_North','r',LineWidth=2.5)
hold on;plot(DATE,ADCP_vel_north_DA,'b',LineWidth=1)
title('Velocity North (Zoomed in Section)',FontSize=14)
grid on
legend('BT Corrected','ADCP Measured','FontSize',14,'Location','Northwest')






%% Plot time series curtain


figure(2);clf;
sgtitle('Velocity Profile Time Series')

cm = cmocean('balance');
subplot(311)

a = pcolor(DateTime,interpCellDepth,Vel_East');

hold on
floor = plot(DateTime,VbDepth_m,'k','LineWidth',3);
set(a,'EdgeColor','none')
set(gca, 'YDir','reverse')
colorbar
colormap(cm)
caxis([-0.45 0.45])
% caxis([min(min(vel_east)), max(max(vel_east))])
ylabel('Water Depth (m)',FontSize=14)
ylabel(colorbar,'E. Velocity (m/s)',FontSize=14)
ylim([0 max(VbDepth_m)+0.5])
title('East',FontSize=14)
grid on

subplot(312)
b = pcolor(DateTime,interpCellDepth,Vel_North');
hold on
floor = plot(DateTime,VbDepth_m,'k','LineWidth',3);
set(b,'EdgeColor','none')
set(gca, 'YDir','reverse')
colorbar
colormap(cm)
caxis([-0.5 0.5])
%caxis([min(min(vel_north)), max(max(vel_north))])
ylabel('Water Depth (m)',FontSize=14)
ylabel(colorbar,'N. Velocity (m/s)',FontSize=14)
%xlabel('Time (s)')
title('North',FontSize=14)
%legend('Velocity Profile','Bottom Depth','location','southeast')
grid on
ylim([0 max(VbDepth_m)+0.5])





subplot(313)
c = pcolor(DateTime,interpCellDepth,Vel_Vert');
hold on
floor = plot(DateTime,VbDepth_m,'k','LineWidth',3);
set(c,'EdgeColor','none')
set(gca, 'YDir','reverse')
colorbar
colormap(cm)
caxis([-0.2 0.2])
ylabel('Water Depth (m)',FontSize=14)
ylabel(colorbar,'Vert. Velocity (m/s)',FontSize=14)
ylim([0 max(VbDepth_m)+0.5])
%xlabel('DateTime (s)')
title('Vertical',FontSize=14)
%legend('Velocity Profile','Bottom Depth','location','southeast')
grid on






%% Rotate for cross channel analysis

UtmNorthing_m(find(UtmNorthing_m == 0)) = nan;
UtmNorthing_m(find(UtmEasting_m == 0)) = nan;

UtmEasting_m(find(UtmNorthing_m == 0)) = nan;
UtmEasting_m(find(UtmEasting_m == 0)) = nan;



Easting = UtmEasting_m;
Northing = UtmNorthing_m;




EastingZero = Easting - nanmean(Easting);
NorthingZero = Northing - nanmean(Northing);

rot_theta = 15.5368; % degrees

Easting_rot = EastingZero*cosd(rot_theta)-NorthingZero*sind(rot_theta);
Northing_rot = EastingZero*sind(rot_theta)+NorthingZero*cosd(rot_theta);



% figure(3);clf;
% plot(EastingZero,NorthingZero,'k.')
% 
% hold on
% plot(Easting_rot,Northing_rot,'.r')
% xlim([-500 500])
% ylim([-500 500])

%% Ski/adcp correlation
% INclude data within this range
% % % % Time(1);
% % % % DATE(5000);

% DepAVGInterp = interp1(DATE,ADCP_vel_north_DA,DateTime)

cross_Time = DateTime(19:2910);
cross_DepAVG = DepAVGInterp(19:2910);

cross_DATE = DATE(2090:4981);
cross_ADCP = ADCP_vel_north_DA(2090:4981)';



figure(5);clf;
% % % plot(Time(1:2910),DepAVGInterp(1:2910),'-r')
% % % hold on
% % % plot(DATE(2090:5000),ADCP_vel_north_DA(2090:5000),'b')
% % % 


plot(cross_ADCP,cross_DepAVG,'.r',MarkerSize=8)
xlabel('ADCP',FontSize=17)
ylabel('Hydrosurveyor',FontSize=17)
legend('Correlation: 0.915','Fontsize',17,'location','northwest')
grid on
axis equal
title('Measured Velocities Comparison',Fontsize=18)


figure(6);clf;
subplot(131)
plot(Vel_North(433,:),interpCellDepth,'r',LineWidth=2)
hold on
plot(VelNorth(:,2504),[0.058148148148148:0.058148148148148:3.14],'k',LineWidth=2)
title('10:26:52',FontSize=17)
ylabel('depth (m)',FontSize=17)
xlabel('Velocity North',FontSize=17)

subplot(132)
plot(Vel_North(619,:),interpCellDepth,'r',LineWidth=2)
hold on
plot(VelNorth(:,2690),[0.058148148148148:0.058148148148148:3.14],'k',LineWidth=2)
title('10:29:58',FontSize=17)
%ylabel('depth (m)')
xlabel('Velocity North',FontSize=17)

subplot(133)
plot(Vel_North(883,:),interpCellDepth,'r',LineWidth=2)
hold on 
plot(VelNorth(:,2764),[0.058148148148148:0.058148148148148:3.14],'k',LineWidth=2)
title('10:31:12',FontSize=17)
%ylabel('depth (m)')
xlabel('Velocity North',FontSize=17)
legend('Hydrosurveyor','ADCP')

% % 
% % plot(Vel_North(958,:),interpCellDepth,'r',LineWidth=2)
% % plot(Vel_North(1131,:),interpCellDepth,'r',LineWidth=2)
% % plot(Vel_North(1191,:),interpCellDepth,'r',LineWidth=2)




return
%%

% exportgraphics(gcf,'/Users/corytoburen/OneDrive - UNC-Wilmington/2023 Summer Internship/HydrosurveyorTests/HydrosurveyorVSadcp.png')
% % figure(2);clf;
% % subplot(211)
% % plot(Time,BtVelE,'m',LineWidth=2)
% % hold on
% % plot(Time,BtVelN,'b',LineWidth=2)
% % grid on
% % ylabel('Bottom Track Velocity (m/s)','FontSize',14)
% % 
% % subplot(212)
% % plot(Time,DepAvgVel_East','m',LineWidth=2)
% % hold on
% % plot(Time,DepAvgVel_North','b',LineWidth=2)
% % legend('East','North','FontSize',14,'Location','Northwest')
% % ylabel('Water Velocity (m/s)','FontSize',14)
% % grid on



