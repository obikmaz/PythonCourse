

import numpy as np
import pandas as pd
import regression

#read data
data= pd.read_csv("data.csv")

#set row index
data = data.set_index("election")

print(data.corr())

print(regression.reg([data["unemployment"],data["gdp per capita/cpi"], data["median age"],data["ppp"]], data["government votes"]))





