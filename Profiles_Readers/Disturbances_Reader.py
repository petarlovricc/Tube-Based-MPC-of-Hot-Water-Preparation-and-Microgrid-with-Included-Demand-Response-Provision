import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from MILP_GUI.utils import resource_path

class CSV_disturbances_reader:
    def __init__(self, day, month, watertemp):
        self.pathElectricity = resource_path("Profiles_Readers/profil_el_ne_upravljivo_BEZ_bojlera_PLUS_2024_15min.csv")
        self.pathWater = resource_path("Profiles_Readers/profil_topla_voda_4_osobe_2024_15min_float.csv")
        self.pathEnvtemp = resource_path("Profiles_Readers/profil_temperatura_prostorije_bojler_2024_15min.csv")
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
        df["Electricity demand (kWh)"] = df["Electricity demand (kWh)"]*4000 #kWh -> W
        
        
        return df["Electricity demand (kWh)"].values[indeks: indeks+96],electricity_energy, sum(df["Electricity demand (kWh)"].values[indeks: indeks+96])

    def csvreaderWater(self):
        df = pd.read_csv(self.pathWater, sep=";")
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d.%m.%Y %H:%M")

        target_time = pd.to_datetime(f"{self.day:02}.{self.month:02}.2024 00:00", format="%d.%m.%Y %H:%M")

        indeks = df[df["timestamp"] == target_time].index[0]
       

        df["Water demand (L)"] = df["Water demand (L)"]*4 #protok tople vode kg/h = water[i]/0.25h
        
        
        return df["Water demand (L)"].values[indeks: indeks+96]
    
    
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