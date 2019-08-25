from typing import Dict
import json


from src.main.sequenceViz.DataProcessing import *
import pandas as pd
import matplotlib.colors as col
import numpy as np

def listToString(val):
    temp = " "
    for x in val:
        temp = temp + "-" + x
    return temp[2:]


if __name__ == "__main__":

    path = "~/Documents/process_mining/dataResult/example_log.csv"
    df = loadData(path)

    caseId ,events ,timestamp ="CaseId","Events","timestamp"
    coloration = list(col.cnames.values())
    activity = np.unique(df.loc[:,events])
    activityColor =dict(zip(activity, coloration))
    print(activityColor)
    pd.DataFrame({"activity":list(activityColor.keys()),"color":list(activityColor.values())}).to_csv("~/Documents/process_mining/dataResult/activity_color.csv",index=False,header=False)

    dictseq: dict = buildSequences(df,caseId,events,timestamp)
    finalTable = pd.DataFrame({"caseId": list(dictseq.keys()), "sequences": list(dictseq.values())})
    finalTable["sequences"] = finalTable.loc[:, "sequences"].apply(lambda val: listToString(val))
    temp = pd.Series(finalTable.loc[:, "sequences"])
    sequences: Dict[str, int] = dict(temp.groupby(temp).count())
    exportRes = pd.DataFrame({"sequences":list(sequences.keys()),"value":list(sequences.values())})
    exportRes.to_csv("~/Documents/process_mining/dataResult/sequences-50.csv",index=False,header=False)

    jsonStyle = buildHierarchy(exportRes)
    jsonWritter = pd.DataFrame(jsonStyle)
    jsonWritter.to_json("~/Documents/process_mining/dataResult/result.json")
