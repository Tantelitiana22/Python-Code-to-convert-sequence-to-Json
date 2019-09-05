from typing import List,Tuple


class Edge:
    def __init__(self, source: str, target: str):
        self.source: str = source
        self.target: str = target

    def getSource(self) -> str:
        return self.source

    def getTarget(self) -> str:
        return self.target


class Sequences:
    def __init__(self,sequences:List[str]):
        self.sequences:List[str] = sequences

    def getSequences(self)->List[str]:
        return self.sequences

    def buildEdge(self)->List[Tuple[str, str]]:
        return [(source,target) for source,target in zip(self.sequences,self.sequences[1:])]



class ClientSequence:
    def __init__(self, client_id:str, sequences:Sequences):
        self.client_id: str = client_id
        self.sequences: Sequences = sequences

    def getKey(self)->str:
        return self.client_id

    def getSequence(self)-> Sequences:
        return self.sequences


class NodeCount:
    def __init__(self, node: str, occurrences: int):
        self.node: str = node
        self.occurrences: int = occurrences

    def getNode(self) -> str:
        return self.node

    def getOccurrences(self) -> int:
        return self.occurrences


class EdgeCount:
    def __init__(self, edge: Edge, occurrences: int):
        self.edge: Edge = edge
        self.occurrences: int = occurrences

    def getEdge(self) -> Edge:
        return self.edge

    def getOccurrences(self) -> int:
        return self.occurrences


