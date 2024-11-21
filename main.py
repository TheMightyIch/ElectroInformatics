import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates



def loadCsv(path):
    return pd.read_csv(path)

def plotCsv(data):
    plt.plot(data["Anfang"],data["negative loads"]*10**3)
    ax=plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.axhline(0, color='black', lw=0.5)
    plt.grid()
    plt.xlabel("Time")
    plt.ylabel("Mismatch [GW]")
    plt.title("Mismatch between demand and generation 2023")
    plt.xticks(rotation=45)
    plt.show()


def highDemand(df):
    return np.sum(df.values.ravel())

def ex2_1():
    demandData = loadCsv('Csvs\demand.csv')
    generationData = loadCsv('Csvs\generation.csv')
    print("loaded data")
    generationData['summed PV and Wind x3 generation'] = (generationData["Wind Offshore [MWh] Originalauflösungen"] * 3 *0.25 + \
                                                         generationData["Wind Onshore [MWh] Originalauflösungen"] * 3*0.25 + \
                                                         generationData["Photovoltaik [MWh] Originalauflösungen"] * 3*0.25)
    print("summed data")
    continual_negative_residual_load = ((demandData[
        "Gesamt (Netzlast) [MWh] Originalauflösungen"]*0.25)-generationData['summed PV and Wind x3 generation']).to_frame(name="negative loads")
    continual_negative_residual_load["Anfang"] = pd.to_datetime(generationData["Datum"]+' '+ generationData["Anfang"])
    plotCsv(continual_negative_residual_load)
    print("plotted data")
    return continual_negative_residual_load
def ex2_2_3_4(continual_negative_residual_load):
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
    print("The energy curtailed was: " + energyCurtailedTWh + " TW")
    plt.boxplot(negative_groups.apply(len))
    plt.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    continual_negative_residual_load = ex2_1()
    ex2_2_3_4(continual_negative_residual_load)


