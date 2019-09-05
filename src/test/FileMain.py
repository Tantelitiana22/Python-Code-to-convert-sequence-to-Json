from typing import Dict
import json

from src.main.sequenceViz.DataProcessing import *
import pandas as pd
import matplotlib.colors as col
import numpy as np


def listToString(val, cutoff=6) -> str:
    if len(val) >= cutoff:
        val = val[:cutoff]
        temp: str = "-".join(val)
        return temp + "-EndForced"
    else:
        temp:str = "-".join(val)
        return temp + "-Rien"


if __name__ == "__main__":
    # path = "~/Documents/process_mining/dataResult/example_log.csv"
    path = "D:/DATA/DATA_ADO/clusteringTFIDF/globaldatawithPrediction_3"
    # df = loadData(path)
    df = pd.read_parquet(path)
    df["Events"] = df.apply(lambda x: x["channel"] + ":" + x["motif"], axis=1)
    caseId, events, timestamp = "client_id", "Events", "date"
    coloration = list(col.cnames.values())
    activity = list(np.unique(df.loc[:, events]))
    activity.append("Rien")
    activity.append("EndForced")
    activityColor = dict(zip(activity, coloration))
    print(activityColor)
    pd.DataFrame({"activity": list(activityColor.keys()), "color": list(activityColor.values())}).to_csv(
        "D:/DATA/Python-Code-to-convert-sequence-to-Json/webvizfile/activity_color.csv", index=False, header=False)

    finalTable = df.loc[:, ["client_id", "channelMotifList"]]
    finalTable.columns = ["caseId", "sequences"]
    finalTable["sequences"] = finalTable.loc[:, "sequences"].apply(lambda val: listToString(val))
    temp = pd.Series(finalTable.loc[:, "sequences"])
    sequences: Dict[str, int] = dict(temp.groupby(temp).count())
    exportRes = pd.DataFrame({"sequences": list(sequences.keys()), "value": list(sequences.values())})
    exportRes.to_csv("D:/DATA/Python-Code-to-convert-sequence-to-Json/webvizfile/sequences-50.csv", index=False,
                     header=False)
    print("--------------------------------------------")
    print("--------------------------------------------")
    print(exportRes.columns)
    print("--------------------------------------------")
    print("--------------------------------------------")
    jsonStyle = buildHierarchy(exportRes)
    print("-----jsonWritter---------")
    print(jsonStyle)
    print("---------------------------")

    with open('../../webvizfile/result.json', 'w') as fp:
        json.dump(jsonStyle, fp)