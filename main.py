import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def loadCsv(path):
    return pd.read_csv(path)

def plotCsv(datas, columnNames):
    for i,data in enumerate(datas):
        line,=plt.plot(data[columnNames[i]])
        line.set_label(columnNames[i])
    plt.legend()
    plt.show()


def highDemand(df):
    return np.sum(df.values.ravel())

def ex2_1():
    demandData = loadCsv('Csvs\demand.csv')
    generationData = loadCsv('Csvs\generation.csv')
    print("loaded data")
    generationData['summed PV and Wind x3 generation'] = generationData["Wind Offshore [MWh] Originalauflösungen"] * 3 + \
                                                         generationData["Wind Onshore [MWh] Originalauflösungen"] * 3 + \
                                                         generationData["Photovoltaik [MWh] Originalauflösungen"] * 3
    print("summed data")
    plotCsv([demandData, generationData],
            ["Residuallast [MWh] Originalauflösungen", 'summed PV and Wind x3 generation'])
    print("plotted data")
    return demandData, generationData

def ex2_2_3_4(demandData, generationData):
    continual_negative_residual_load = (generationData['summed PV and Wind x3 generation'] - demandData[
        "Gesamt (Netzlast) [MWh] Originalauflösungen"]).to_frame(name="negative loads")
    continual_negative_residual_load["negative mask"] = continual_negative_residual_load["negative loads"] < 0
    continual_negative_residual_load["groups"] = (
                continual_negative_residual_load["negative mask"] != continual_negative_residual_load[
            "negative mask"].shift()).cumsum()
    negative_groups = \
    continual_negative_residual_load[continual_negative_residual_load['negative mask']].groupby('groups')[
        "negative loads"].apply(list)
    longest_negative_series = max(negative_groups, key=len)

    continual_negative_residual_loadCount = highDemand(continual_negative_residual_load["negative mask"])
    print("The number of times the demand was higher than the generation was: ", continual_negative_residual_loadCount)
    print("The longest series of negative residual load was: ", len(longest_negative_series))
    energyCurtailedTWh = str(np.sum(longest_negative_series) * 10 ** -6)
    print("The energy curtailed was: " + energyCurtailedTWh + " TWh")
    plt.boxplot(negative_groups.apply(len))
    plt.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    demandData, generationData = ex2_1()
    ex2_2_3_4(demandData, generationData)


