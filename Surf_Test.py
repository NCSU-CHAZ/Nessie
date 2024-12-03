from post_processing.HydroSurveyor.process_file_HydroSurveyor import Hydro_process
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import pickle as pickle
import scipy.stats as spy

# This file is the summary analysis file for the surfzone test, the first few commented lines process and save the data by using
# functions from other scripts. We are using the pickle module in order to write the data as bytes into a txt file. The rest of the
# script then loads the data using pickle and generates some plots. Some of the plots require other individual data streams to work.
# To get these other data streams simple run hydroprocess on the raw data for whatever it needs to process.

# CombinedData = Hydro_process(
#     r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\2024_08_30_Surfzone\File"
# )
# with open(r'C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Processed Data\SurfTest.txt','wb') as file:
#     pickle.dump(CombinedData, file)

with open(
    r"C:\Users\lwlav\OneDrive\Documents\Summer 2024 CHAZ\Data\Processed Data\SurfTest.txt",
    "rb",
) as file:
    CombinedData = pickle.load(file)


NMask = (CombinedData["HeadingRad"] >= 7 * np.pi / 4) | (
CombinedData["HeadingRad"] < np.pi / 4
)
EMask = (CombinedData["HeadingRad"] >= np.pi / 4) & (
CombinedData["HeadingRad"] < 3 * np.pi / 4
)
SMask = (CombinedData["HeadingRad"] >= 3 * np.pi / 4) & (
CombinedData["HeadingRad"] < 5 * np.pi / 4
)
WMask = (CombinedData["HeadingRad"] >= 5 * np.pi / 4) & (
CombinedData["HeadingRad"] < 7 * np.pi / 4
)
  
dim = CombinedData["HorizontalVel"].shape
NMask = np.tile(NMask, (1, dim[1]))
EMask = np.tile(EMask, (1, dim[1]))
SMask = np.tile(SMask, (1, dim[1]))
WMask = np.tile(WMask, (1, dim[1]))

NorthingVel = CombinedData["HorizontalVel"].copy()
EastingVel = CombinedData["HorizontalVel"].copy()
SouthingVel = CombinedData["HorizontalVel"].copy()
WestingVel = CombinedData["HorizontalVel"].copy()

NorthingVel[~NMask]= float('NaN')
EastingVel[~EMask]= float('NaN')
SouthingVel[~SMask]= float('NaN')
WestingVel[~WMask]= float('NaN')


def time_comparison(Data1, Data2, Data3, Data4):
    fig, axs = plt.subplots(4, sharex=True)
    axs[0].plot(Data1["DateTime"], Data1["SampleNumber"], label="Session 1")
    axs[1].plot(Data2["DateTime"], Data2["SampleNumber"], label="Session 2")
    axs[2].plot(Data3["DateTime"], Data3["SampleNumber"], label="Session 3")
    axs[3].plot(Data4["DateTime"], Data4["SampleNumber"], label="Session 4")

    for i in range(len(axs)):
        axs[i].legend()
    fig.suptitle("DateTimes versus Sample Number")
    fig.supxlabel("Time (DD HH:MM)")
    fig.supylabel("Sample Number")
    fig.tight_layout()
    plt.show()


def adcp_comparison_Abs(Data3, Data4, CombinedData):

    lw = 1
    fig, axs = plt.subplots(2, sharex=True)
    axs[0].plot(
        (CombinedData["DateTime"]),
        (pd.DataFrame(np.nanmean(CombinedData["AbsVel"], axis=1))),
        label="Combined Data",
    )
    plt.legend()
    axs[1].plot(
        Data4["DateTime"],
        (pd.DataFrame(np.nanmean(Data4["AbsVel"], axis=1))),
        color="Red",
        label="Session 4",
        linewidth=lw,
    )
    axs[1].plot(
        Data3["DateTime"],
        (pd.DataFrame(np.nanmean(Data3["AbsVel"], axis=1))),
        color="Blue",
        label="Session 3",
        linewidth=lw,
    )
    fig.suptitle("Absolute Velocity versus Time")
    fig.supxlabel("Time (DD HH:MM)")
    fig.supylabel("Velocity (m/s)")
    plt.legend()
    plt.show()


def bathy_plot(CombinedData):
    # Sample data: Replace with your actual longitude, latitude, and depth values
    x = CombinedData["Longitude"]  # Longitude
    y = CombinedData["Latitude"]  # Latitude
    z = CombinedData["VbDepth"]  # Depth (negative for bathymetry)

    # Create 3D figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Plotting options:
    # 1. Scatter Plot
    im1 = ax.scatter(x, y, z, c=z, cmap="viridis")  # Color by depth
    ax.invert_zaxis()
    cbar = plt.colorbar(im1, ax=ax, shrink=0.5, aspect=5)
    cbar.set_label("Depth (meters)")
    # Set labels and title
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_zlabel("Depth")
    plt.title("3D Bathymetry Survey")

    plt.show()


def pitch_roll_comp(CombinedData):

    fig, ax = plt.subplots(2, sharex=True)

    ax[0].plot(CombinedData["DateTime"], CombinedData["Pitch"])
    ax[1].plot(CombinedData["DateTime"], CombinedData["Roll"])
    ax[0].set_title("Pitch vs Time")
    ax[1].set_title("Roll vs Time")
    ax[0].set_ylabel("Pitch (rad)")
    ax[1].set_ylabel("Roll (rad)")

    fig.supxlabel("Time (DD HH:MM)")
    plt.show()


def Vb_Plot(CombinedData):
    plt.plot(CombinedData["DateTime"], CombinedData["VbDepth"])
    plt.title("Vertical Beam Depth vs Time")
    plt.xlabel("Time")
    plt.ylabel("Depth (m)")
    plt.show()


def variance_inspection(CombinedData):

    #This function is designed to split the velocity field up into the four different directions of travel in order to
    #analyze the variance dependent on the whether or not the transect was traveling E->W, W->E,N->S,S->N.

    plt.plot(CombinedData['DateTime'],np.nanmean(NorthingVel,axis=1), label = 'Northing')
    plt.plot(CombinedData['DateTime'],np.nanmean(EastingVel,axis=1), label = 'Easting')
    plt.plot(CombinedData['DateTime'],np.nanmean(SouthingVel,axis=1), label = 'Southing')
    plt.plot(CombinedData['DateTime'],np.nanmean(WestingVel,axis=1), label = 'Westing')
    plt.legend()
    plt.show()

    #After seeing the data field has been split up appropriately, analyze the variance of the data.

    # Northing velocities
    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True)

# Northing velocities
    axs[0, 0].hist(NorthingVel[~np.isnan(NorthingVel)].ravel(), bins=100)
    axs[0, 0].set_title('Northing Velocity Distribution')
    axs[0, 0].set_xlabel('Velocity')
    axs[0, 0].set_ylabel('Samples')

    # Easting velocities
    axs[0, 1].hist(EastingVel[~np.isnan(EastingVel)].ravel(), bins=100)
    axs[0, 1].set_title('Easting Velocity Distribution')
    axs[0, 1].set_xlabel('Velocity')
    axs[0, 1].set_ylabel('Samples')

    # Southing velocities
    axs[1, 0].hist(SouthingVel[~np.isnan(SouthingVel)].ravel(), bins=100)
    axs[1, 0].set_title('Southing Velocity Distribution')
    axs[1, 0].set_xlabel('Velocity')
    axs[1, 0].set_ylabel('Samples')

    # Westing velocities
    axs[1, 1].hist(WestingVel[~np.isnan(WestingVel)].ravel(), bins=100)
    axs[1, 1].set_title('Westing Velocity Distribution')
    axs[1, 1].set_xlabel('Velocity')
    axs[1, 1].set_ylabel('Samples')

    plt.tight_layout()
    plt.show()


    # Northing velocities
    fig,axs = plt.subplots(4,sharex=True,sharey=True)
    axs[0].hist(np.nanmean(NorthingVel,axis=1),bins=100)
    axs[0].title('Northing Average Velocity Distribution')
    axs[0].xlabel('Velocity')
    axs[0].ylabel('Samples')

    # Easting velocities
    axs[1].hist(np.nanmean(EastingVel,axis=1),bins=100)
    axs[1].title('Eastingn Average Velocity Distribution')
    axs[1].xlabel('Velocity')
    axs[1].ylabel('Samples')

    # Southing velocities
    axs[2].hist(np.nanmean(SouthingVel,axis=1),bins=100)
    axs[2].title('Southing Average Velocity Distribution')
    axs[2].xlabel('Velocity')
    axs[2].ylabel('Samples')

    # Westing velocities
    axs[3].hist(np.nanmean(WestingVel,axis=1),bins=100)
    axs[3].title('Westing Average Velocity Distribution')
    axs[3].xlabel('Velocity')
    axs[3].ylabel('Samples')

    plt.tight_layout()
    plt.show()

def basic_error_analysis(data):
    #The goal of this function is to perform a basic error analysis and look at measurements such as standard error and standard deviation.
    data = data.values.flatten() #Turn matrix into vector since time and depth coordinates aren't relevant for this analysis
    data = data[~np.isnan(data)] #Remove all nan values to prevent errors when dealing with them
    # Flatten the data into a 1D array
    
    # Remove NaN values
    data = data[~np.isnan(data)]
    
    # Calculate statistics
    confidence = .95 #Confidence level
    n = len(data)
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)  # Sample standard deviation (ddof=1)
    std_error = std_dev / np.sqrt(n)  # Standard error of the mean
    median = np.median(data)
    
    # Calculate the confidence interval
    t_critical = spy.t.ppf((1 + confidence) / 2, df=n-1)  # t critical value
    margin_of_error = t_critical * std_error
    confidence_interval = (mean - margin_of_error, mean + margin_of_error)
    
    # Store results in a dictionary
    results = {
        "mean": mean,
        "std_dev": std_dev,
        "std_error": std_error,
        "confidence_interval": confidence_interval,
        "confidence_level": confidence,
        "median":median
    }
    
    # Print results
    print(f"Mean: {mean:.4f}")
    print(f"Standard Deviation: {std_dev:.4f}")
    print(f"Standard Error: {std_error:.4f}")
    print(f"{confidence*100:.1f}% Confidence Interval: ({confidence_interval[0]:.4f}, {confidence_interval[1]:.4f})")
    print(f"Median: {median:.4f}")
    
    # Plot histogram of the data
    plt.hist(data, bins=50, alpha=0.7, color='blue', density=True)
    plt.title("WestingVel Data Distribution")
    plt.xlabel("Velocity (m/s)")
    plt.ylabel("Density")
    plt.axvline(mean, color='red', linewidth=1, label='Mean')
    plt.axvline(confidence_interval[0], color='black', linestyle='dashed', linewidth=1, label=f'Lower {confidence*100:.1f}% CI')
    plt.axvline(confidence_interval[1], color='black', linestyle='dashed', linewidth=1, label=f'Upper {confidence*100:.1f}% CI')
    plt.axvline(median, color = 'green',label = 'Median')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    return results



def chi_fit(Data, label, bins=100, signifigance = .05):
    # Flatten and remove NaN values
    data_cleaned = Data.flatten()  # Flatten the DataFrame
    data_cleaned = data_cleaned[~np.isnan(data_cleaned)]
    # Fit to a chi-squared distribution
    df, loc, scale = spy.chi2.fit(data_cleaned)
    observed, bin_edges = np.histogram(data_cleaned, bins=bins,)
    
    print(observed, bin_edges)

    expected = []
    for i in range(len(bin_edges) - 1):
        # Integrate PDF over bin range to get expected frequency
        p = spy.chi2.cdf(bin_edges[i + 1], df, loc=loc, scale=scale) - spy.chi2.cdf(bin_edges[i], df, loc=loc, scale=scale)
        expected.append(p * len(data_cleaned))
    expected = np.array(expected)

    #Degrees of freedom and chi sqaured stat
    chi2_stat = np.sum((observed - expected) ** 2 / expected)
    dof = df
    # Critical value and p-value
    critical_value = spy.chi2.ppf(1 - signifigance, dof)
    p_value = 1 - spy.chi2.cdf(chi2_stat, dof)

    # Print results
    print(f"Chi-squared Statistic: {chi2_stat:.2f}")
    print(f"Critical Value (alpha={signifigance}): {critical_value:.2f}")
    print(f"p-value: {p_value:.2e}")

    #This statement will tell you whether this is a valid test or not
    if chi2_stat > critical_value:
        print(f"Result: Reject the null hypothesis. The data does not follow a chi-squared distribution.")
    else:
        print(f"Result: Fail to reject the null hypothesis. The data may follow a chi-squared distribution.")

    # Generate histogram of the data
    plt.hist(data_cleaned, bins=100, density=True, alpha=0.5, label=f'{label} Data')

    # Generate chi-squared probability density (pdf)
    x = np.linspace(data_cleaned.min(), data_cleaned.max(), 100)
    pdf = spy.chi2.pdf(x, df, loc=loc, scale=scale)
    plt.plot(x, pdf, label=f'Chi-squared Fit (df={df:.2f})', color='red')
    
    # Add plot details
    plt.title(f'{label} Velocity Distribution and Chi-squared Fit')
    plt.xlabel('Velocity')
    plt.ylabel('Density')
    plt.legend()
    plt.grid()
    plt.show()

    # Plot observed vs expected
    plt.hist(data_cleaned, bins=bins, alpha=0.5, label="Observed Data", density=True)
    plt.plot(x, pdf * len(data_cleaned) * (bin_edges[1] - bin_edges[0]), label="Expected (Chi-squared Fit)", color="red")
    plt.title(f"Chi-squared Test for {label}")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid()
    plt.show()

def get_best_distribution(data):
    dist_names = ["norm", "exponweib", "weibull_max", "weibull_min", "pareto", "genextreme","chi2"]
    dist_results = []
    params = {}
    data_cleaned = data.ravel()  # Flatten the DataFrame
    data = data_cleaned[~np.isnan(data_cleaned)]
    for dist_name in dist_names:
        dist = getattr(spy, dist_name)
        param = dist.fit(data)

        params[dist_name] = param
        # Applying the Kolmogorov-Smirnov test
        D, p = spy.kstest(data, dist_name, args=param)
        print("p value for "+dist_name+" = "+str(p))
        dist_results.append((dist_name, p))

    # select the best fitted distribution
    best_dist, best_p = (max(dist_results, key=lambda item: item[1]))
    # store the name of the best fit and its p value

    print("Best fitting distribution: "+str(best_dist))
    print("Best p value: "+ str(best_p))
    print("Parameters for the best fit: "+ str(params[best_dist]))

    return best_dist, best_p, params[best_dist]

def depth_vel_comparison(data):
    #This data will plot and compare velocity at different depths that have been arbitrarily decided
    lowmask = data['interpCellDepth'] < 1
    medmask = (data['interpCellDepth'] > 1 ) & (data['interpCellDepth']< 2) 
    deepmask = (data['interpCellDepth'] > 2)

    lowmask = np.tile(lowmask.T, (dim[0],1))
    medmask = np.tile(medmask.T, (dim[0],1))
    deepmask = np.tile(deepmask.T, (dim[0],1))

    shallowVel = data['HorizontalVel'].copy()
    medVel = data['HorizontalVel'].copy()
    deepVel = data['HorizontalVel'].copy()

    print(np.shape(lowmask))
    print(np.shape(shallowVel))

    shallowVel = np.where(lowmask, data['HorizontalVel'], np.nan)
    medVel = np.where(medmask, data['HorizontalVel'], np.nan)
    deepVel = np.where(deepmask, data['HorizontalVel'], np.nan)

    fig, axs = plt.subplots(3, sharex= True, sharey= True)

    axs[0].plot(data["DateTime"], np.nanmean(shallowVel,axis=1), label="Shallow Velocity")
    axs[1].plot(data["DateTime"], np.nanmean(medVel,axis=1), label="Middle Depth Velocity")
    axs[2].plot(data["DateTime"], np.nanmean(deepVel,axis=1), label="Deep Velocity")

    for i in range(len(axs)):
        axs[i].legend()
    fig.suptitle("DateTimes versus Velocity")
    fig.supxlabel("Time (DD HH:MM)")
    fig.supylabel("Velocity (m/s)")
    fig.tight_layout()
    plt.show()

# adcp_comparison_Abs(Data3, Data4, CombinedData)

# bathy_plot(CombinedData)

# pitch_roll_comp(CombinedData)

# Vb_Plot(CombinedData)

variance_inspection(CombinedData)

#basic_error_analysis(WestingVel)

#chi_fit(WestingVel,'Westing', bins=100, signifigance = .05)

#get_best_distribution(EastingVel)

#depth_vel_comparison(CombinedData)

