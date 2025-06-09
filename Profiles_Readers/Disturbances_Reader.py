import numpy as np
import matplotlib.pyplot as plt
import os
class CSV_disturbances_reader:
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        self.pathElectricity = os.path.join(base_dir, "electric_demand_Wh.csv")
        self.pathWater = os.path.join(base_dir, "water_demand.csv")
        self.electricityLoad = self

    def csvreaderElectricity(self):
        data = np.loadtxt(self.pathElectricity, dtype="object",encoding='utf-8-sig')
        electricity = data.astype("float")
        electricity_power = electricity*4

        return electricity_power,electricity, sum(electricity)
    
    def csvreaderWater(self):
        data = np.loadtxt(self.pathWater, dtype="object",skiprows=1)

        #masa tople vode u 15 minutnom intervalu
        water = data.astype("float")

        #protok tople vode kg/h = water[i]/0.25h 
        flow = water*4

        return  flow
    
    def setWaterTemparray(self):
        setTempKelvin = np.r_[np.repeat(312.15,4),np.repeat(311.15,20),np.repeat(314.15,8),np.repeat(312.15,16),np.repeat(313.15,16),
                     np.repeat(311.15,8),np.repeat(313.15,8),np.repeat(316.15,8),np.repeat(312.15,8)]
        
        setTempCelsius = setTempKelvin - 273.15

        return setTempKelvin, setTempCelsius
    
    def environment_Temperature(self):
        tempCelsius = np.r_[np.repeat(18,24), np.repeat(20,8), np.repeat(22,48),
                            np.repeat(20,10),np.repeat(19,3),np.repeat(18,3)]
        tempKelvin = tempCelsius+273.15

        return tempKelvin, tempCelsius