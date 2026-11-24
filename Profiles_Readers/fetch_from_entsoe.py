import os
import pandas as pd
from entsoe import EntsoePandasClient


api_key = os.getenv("ENTSOE_API_KEY")
if not api_key:
    raise RuntimeError("Add the user environment variable 'ENTSOE_API_KEY'. Restart the IDE after that.")
client = EntsoePandasClient(api_key=api_key)

def fetch_DA_prices_in_MW(path, day, month, year, timezone_city, country_code, duration):

    start = pd.Timestamp(year = year, month = month, day=day, hour = 0, minute= 0,  tz=f'Europe/{timezone_city}')
    end = pd.Timestamp(year = year, month = month, day=day + (duration-1)//24, hour = (duration-1)%24, minute= 45, tz=f'Europe/{timezone_city}')

    da = client.query_day_ahead_prices(country_code=country_code, start=start, end=end)  # Series, EUR/MWh, 15 min
    da.to_csv(path)


if __name__ == "__main__":
    fetch_DA_prices_in_MW(22,11,2026, "Zagreb", "HR", "24h")





