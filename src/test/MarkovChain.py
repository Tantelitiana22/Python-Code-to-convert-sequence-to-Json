import pandas as pd
from typing import Set, Union, Dict
from pandas import DataFrame, Series
from src.main.sequenceViz.modele import ClientSequence, Sequences
from src.main.sequenceViz.DataProcessing import markovChain
import json
import numpy as np


def dataResult(pattern: int) -> int:
    if pattern > 300:
        return 300
    if pattern < 150:
        return 150
    return int(pattern)


if __name__ == "__main__":
    # path = "~/Documents/process_mining/dataResult/example_log.csv"
    path = "D:/DATA/DATA_ADO/clusteringTFIDF/globaldatawithPrediction_5"
    df: DataFrame = pd.read_parquet(path)
    clientSequence: Set[ClientSequence] = {ClientSequence(id, Sequences(seq)) for id, seq in
                                           zip(df.client_id, df.channelMotifList)}

    Nodes: Union[Series, DataFrame] = df.apply(lambda x: x["channel"] + ":" + x["motif"], axis=1)
    dictNodes: Dict[str, int] = dict(Nodes.groupby(Nodes).count())
    countNodes: Dict[str, int] = {id: dictNodes[id] for id in dictNodes}

    edges = sum([idseq.getSequence().buildEdge() for idseq in clientSequence], [])
    edges = pd.Series(edges)
    countEdge = dict(edges.groupby(edges).count())

    markovEdgeChaine = {}
    for nodes in countNodes.keys():
        markovEdgeChaine.update(markovChain(countEdge, nodes))

    nodesList = [{"node": key, "size": dataResult(countNodes[key])} for key in countNodes]

    edgesList = [{"from": key[0], "to": key[1], "size": float(np.round(markovEdgeChaine[key], 2))} for key in
                 markovEdgeChaine if markovEdgeChaine[key] > 0.2]

    toExport = {"nodes": nodesList, "edges": edgesList}

    with open('../../visnetwork_javascript/node_modules/MarkovResult.json', 'w') as fp:
        json.dump(toExport, fp)
