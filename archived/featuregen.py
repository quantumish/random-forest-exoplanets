# CODE TAKEN FROM BANPEI MODULE AND MODIFIED DUE TO ERRORS
import statistics as stat
from scipy import stats
import numpy as np
def detect(data, threshold):
    data2 = np.asarray(data)
    abn_th = stats.chi2.interval(1-threshold, 1)[1]
    avg = np.average(data2)
    var = np.var(data2)
    data_abn = [(x - avg)**2 / var for x in data2]
    result = []
    result2 = []
    for (index, x) in enumerate(data_abn):
        result.append(x)
        if (x > abn_th) and (data2[index]<stat.median(data)):
            result2.append([index, data2[index], data.index(data2[index])])
    return result, result2

# ORIGINAL CODE BELOW
from astropy.io import fits
import matplotlib.pyplot as plt
import os
import pandas as pd
import csv
i=0
X=[]
y=[]

# Conversion from FITS files to lists.
for root, dirs, files in os.walk("/Users/davfrei/TRAIN"):
    for file in files:
        if file.endswith(".fits"):
            if "INJECTED" in file:
                label=1
            else:
                label=0
            X.append([])
            hdul = fits.open("/Users/davfrei/TRAIN/"+file)
            hdul.info()
            data = hdul[1].data
            for e in data["PDCSAP_FLUX"]:
                if np.isnan(e)!=True:
                    X[i].append(e)

# Usage of banpei module to find outliers, it runs a complicated stats function, but no ML involved.
            results,results2 = detect(X[i], 0.01)
            results,results_wide = detect(X[i], 0.2)
            results,results_medium = detect(X[i], 0.08)
            results,results_narrow = detect(X[i], 0.01)
#
# PLOTTING CODE USED FOR TESTING
#
#            if 1==1:
#                plt.subplot(2, 1, 1)
#                plt.plot(X[i])
#                plt.title('Exoplanet Data')
#                plt.ylabel('Luminosity')
#                plt.subplot(2, 1, 2)
#                plt.plot(results)
#                plt.xlabel('Time')
#                plt.ylabel('Anomalousness')
#                plt.show()
#
            i=i+1
            a=0
            past=0
            diff=[]
            print results_narrow
            if results_narrow != []:
                while a < len(results_narrow):
                    current = results_narrow[a][2]
                    diff.append(current-past)
                    past=current
                    a=a+1
                differences = stat.mean(diff)
            else:
                differences = -1
            print differences

            with open("output.csv", "a") as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow([label, len(results_wide), len(results_medium), len(results_narrow), differences])
