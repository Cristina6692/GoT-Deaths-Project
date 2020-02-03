import pandas as pd
import requests
import json
import numpy as np
from src.variab import regions
from src.variab import books


def cleanGender(colname,genders):
     return colname.replace(genders)

def apiToDf(url):

    response= requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    return df


def regionName(dfcol):
    for item in regions.items():
        key=item[0]
        for oldname in item[1]:
           dfcol = dfcol.replace(oldname,key)
    return dfcol




