import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from Profiles_Readers.fetch_from_entsoe import fetch_DA_prices_in_MW
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class CSVDaReader:
    def __init__(self, day, month, year, timezone, country_code, duration):
        self.pathdaprices = os.path.join(BASE_DIR, f"da_prices_{day}_{month}_{year}_{country_code}_{duration}.csv")
        self.month = month
        self.day = day
        self.year = year
        self.timezone = timezone
        self.country_code = country_code
        self.duration = duration

    def csvreaderPrices(self):
        if not os.path.exists(self.pathdaprices):
            fetch_DA_prices_in_MW(self.pathdaprices, self.day, self.month, self.year, self.timezone, self.country_code, self.duration)
        df = pd.read_csv(self.pathdaprices)
        prices_in_EURMWh = np.array([df.values[i][1] for i in range(len(df))]).reshape(-1,1)
        if prices_in_EURMWh.shape[0] != self.duration*4:
            prices_in_EURMWh = np.repeat(prices_in_EURMWh, 4)
        return prices_in_EURMWh


if __name__ == "__main__":
    reader = CSVDaReader(22, 11, 2026, "Zagreb", "HR", "36h")
    prices = reader.csvreaderPrices()
    print(prices.shape, prices[:5])
