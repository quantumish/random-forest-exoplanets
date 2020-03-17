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
Y=[]

# Conversion from FITS files to lists.
for root, dirs, files in os.walk("/Users/davfrei/TRAIN"):
    for file in files:
        if file.endswith(".fits"):
            if "INJECTED" in file:
                label=1
            else:
                label=0
            X.append([])
            Y.append([])
            hdul = fits.open("/Users/davfrei/TRAIN/"+file)
            hdul.info()
            data = hdul[1].data

            for e in data["SAP_FLUX"]:
                if np.isnan(e)!=True:
                    Y[i].append(e)

# GENERATE ANOMALY FEATURES
            for e in data["PDCSAP_FLUX"]:
                if np.isnan(e)!=True:
                    X[i].append(e)

# Usage of banpei module to find outliers--it runs a complicated stats function, but no ML involved.
            results,pdc_results_wide = detect(X[i], 0.2)
            results,pdc_results_medium = detect(X[i], 0.08)
            results,pdc_results_narrow = detect(X[i], 0.01)

            results,results_wide = detect(Y[i], 0.2)
            results,results_medium = detect(Y[i], 0.08)
            results,results_narrow = detect(Y[i], 0.01)

            i=i+1
            a=0
            past=0
            diff=[]
            if results_narrow != []:
                while a < len(pdc_results_narrow):
                    current = pdc_results_narrow[a][2]
                    diff.append(current-past)
                    past=current
                    a=a+1
                pdc_differences = stat.mean(diff)
            else:
                pdc_differences = -1
            a=0
            past=0
            diff=[]
            if results_narrow != []:
                while a < len(results_narrow):
                    current = results_narrow[a][2]
                    diff.append(current-past)
                    past=current
                    a=a+1
                differences = stat.mean(diff)
            else:
                differences = -1

# WRITE FEAUTURES TO FILE

            with open("output.csv", "a") as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow([label, len(results_wide), len(results_medium), len(results_narrow), differences, len(pdc_results_wide), len(pdc_results_medium), len(pdc_results_narrow), pdc_differences])
