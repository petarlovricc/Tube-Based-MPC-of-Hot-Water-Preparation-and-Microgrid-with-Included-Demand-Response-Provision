import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class CSV_disturbances_reader:
    def __init__(self, day, month, watertemp, hub_name):
        self.pathElectricity = os.path.join(BASE_DIR, hub_name, f"noncontrollable_load_annual_profile_{hub_name}.csv")
        self.pathWater = os.path.join(BASE_DIR, hub_name, f"water_demand_annual_profile_{hub_name}.csv")
        self.pathEnvtemp = os.path.join(BASE_DIR, hub_name, "environment_temperature_annual_profile.csv")
        self.day = day
        self.month = month
        self.watertemp = watertemp

    # def csvreaderElectricity(self):
    #     data = np.loadtxt(self.pathElectricity, dtype="object",encoding='utf-8-sig')
    #     electricity = data.astype("float")
    #     electricity_power = electricity*4

    #     return electricity_power,electricity, sum(electricity)
    
    def csvreaderElectricity(self):
        df = pd.read_csv(self.pathElectricity, sep=";")
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d.%m.%Y %H:%M")

        target_time = pd.to_datetime(f"{self.day:02}.{self.month:02}.2024 00:00", format="%d.%m.%Y %H:%M")

        indeks = df[df["timestamp"] == target_time].index[0]


        electricity_energy = df["Electricity demand (kWh)"].values[indeks: indeks+96]*1000
        total_annual_consumption = df["Electricity demand (kWh)"].sum() # !!!!!!!!! u kWh !!!!!!!!!
        df["Electricity demand (kWh)"] = df["Electricity demand (kWh)"]*4000 #kWh -> W
        
        
        return (df["Electricity demand (kWh)"].values[indeks: indeks+96],electricity_energy,
                 sum(electricity_energy), total_annual_consumption)

    def csvreaderWater(self):
        df = pd.read_csv(self.pathWater, sep=";")
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d.%m.%Y %H:%M")

        target_time = pd.to_datetime(f"{self.day:02}.{self.month:02}.2024 00:00", format="%d.%m.%Y %H:%M")

        indeks = df[df["timestamp"] == target_time].index[0]
       
        total_annual_consumption = df["Water demand (m3)"].sum() # !!!!!!!!! u m3 !!!!!!!!!!!!
        df["Water demand (m3)"] = df["Water demand (m3)"]*4 #protok tople vode m3/h = water[i]/0.25h
        
        
        return df["Water demand (m3)"].values[indeks: indeks+96], total_annual_consumption
    
    
    def setWaterTemparray(self, watertemp):
        setTempKelvin = np.r_[np.repeat(watertemp+273.15,96)]
        
        setTempCelsius = setTempKelvin - 273.15

        return setTempKelvin, setTempCelsius
    
    # def environment_Temperature(self):
    #     tempCelsius = np.r_[np.repeat(18,24), np.repeat(20,8), np.repeat(22,48),
    #                         np.repeat(20,10),np.repeat(19,3),np.repeat(18,3)]
    #     tempKelvin = tempCelsius+273.15

    #     return tempKelvin, tempCelsius
    

    
                      

    def environment_Temperature(self):
        df = pd.read_csv(self.pathEnvtemp, sep=";")
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d.%m.%Y %H:%M")

        target_time = pd.to_datetime(f"{self.day:02}.{self.month:02}.2024 00:00", format="%d.%m.%Y %H:%M")

        indeks = df[df["timestamp"] == target_time].index[0]
       

        tempCelsius = df["Room temperature (°C)"].values[indeks: indeks+96]
        tempKelvin = tempCelsius+273.15

        
        
        return tempKelvin, tempCelsius

    def annual_peak_and_load_factor(self):
        """
                Return the annual peak of the non-controllable load and the annual load factor.

                Returns
                -------
                tuple
                    peak_power:
                        Maximum 15-minute average power over the whole year [W].

                    load_factor:
                        Annual energy / (peak power * hours in year) [-].
        """

        df = pd.read_csv(self.pathElectricity, sep=";")
        energy_kWh = df["Electricity demand (kWh)"].values

        peak_power = energy_kWh.max()*4000
        hours = len(energy_kWh)*0.25

        load_factor = energy_kWh.sum()/(hours*peak_power/1000)

        return peak_power, load_factor
