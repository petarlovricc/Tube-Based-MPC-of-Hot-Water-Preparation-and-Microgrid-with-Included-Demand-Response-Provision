import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from MILP_GUI.utils import resource_path


class CSV_da_reader:
    def __init__(self, day, month):
        self.pathdaprices = resource_path("Profiles_Readers/day-ahead_prices_CRO_2024.csv")
        self.month = month
        self.day = day
       

    def csvreaderPrices(self):
        df = pd.read_csv(self.pathdaprices, sep=";")
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d.%m.%Y %H:%M")

        target_time = pd.to_datetime(f"{self.day:02}.{self.month:02}.2024 00:00", format="%d.%m.%Y %H:%M")

        indeks = df[df["timestamp"] == target_time].index[0]

        df["Day-ahead (EUR/MWh)"] = df["Day-ahead (EUR/MWh)"]/10**6 #MW -> W
        
        prices = np.repeat(df["Day-ahead (EUR/MWh)"].values[indeks: indeks+24], 4)

        return prices
    
    