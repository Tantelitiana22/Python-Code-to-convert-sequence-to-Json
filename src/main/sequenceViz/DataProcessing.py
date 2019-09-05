import pandas as pd
from pandas import DataFrame
import numpy as np
from .modele import ClientSequence, Edge


def loadData(path: str) -> DataFrame:
    return pd.read_csv(path)


# def buildSequences(data: DataFrame, caseId: str, events: str, timestamp: str) -> set[ClientSequence]:
#    caseid: DataFrame = data.loc[:, caseId]
#    resultat: dict = {id: list(data[data.loc[:, caseId] == id].sort_values(timestamp).loc[:, events]) for id in caseid}
#    model: set[ClientSequence] = {ClientSequence(id, resultat[id]) for id in resultat}
#    return model


def buildHierarchy(csv: DataFrame):
    print(csv.head())
    global nodeName, children
    root = {"name": "root", "children": []}

    for i in range(csv.shape[0]):
        sequence = csv.iloc[i, 0]
        size = csv.iloc[i, 1]

        if np.isnan(size):
            ## e.g. if this is a header row
            continue

        parts = sequence.split("-")
        currentNode = root
        for j in range(len(parts)):

            lastChildren = []
            if "children" in currentNode:
                children = currentNode["children"]
                lastChildren = children
            else:
                children = lastChildren

            children = currentNode["children"]
            nodeName = parts[j]

            if j + 1 < len(parts):
                # Not yet at the end of the sequence; move down the tree.
                foundChild = False
                global childNode
                for k in range(len(children)):
                    if children[k]["name"] == nodeName:
                        childNode = children[k]
                        foundChild = True
                        break

                ## If we don't already have a child node for this branch, create it.
                if not foundChild:
                    childNode = {"name": nodeName, "children": []}
                    children.append(childNode)
                    currentNode = childNode
            else:
                ##Reached the end of the sequence; create a leaf node.
                childNode = {"name": nodeName, "size": size}
                children.append(childNode)
    return root


def markovChain(countEdge: dict, node: str) -> dict:
    selectEdges: dict = {key: countEdge[key] for key in countEdge if key[0] == node}

    return {key: selectEdges[key] / sum(selectEdges.values()) for key in selectEdges}
