import pandas as pd


def preprocess_binary(path):

    data = pd.read_csv(path)

    data[["retention_1", "retention_7"]] = data[["retention_1", "retention_7"]].applymap(lambda x: 1 if x == True else 0)
    data["version"] = data["version"].map({"gate_30": "control", "gate_40": "variant"})

    return data

def new_func():

    return 2


def preprocess_continuous(path):

    data = pd.read_csv(path)

    return data




