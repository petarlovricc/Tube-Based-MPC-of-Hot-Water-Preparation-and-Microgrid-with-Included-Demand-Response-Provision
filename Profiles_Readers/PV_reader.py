#funkcija koja pomoću odabranog dana u godini vraća profil potrošnje za taj dan
import numpy as np
import matplotlib.pyplot as plt
import os
from MILP_GUI.utils import resource_path


class PVreader:
    def __init__(self, day, month, PV_power, numberofPV):
        self.path = resource_path("Profiles_Readers/PV.csv")
        self.month = month
        self.day = day
        self.PV_power = PV_power
        self.numberofPV = numberofPV

    def csvreader(self):
        data = np.loadtxt(self.path, dtype="object", skiprows=1)
        PV_prod = data.astype("float")
        starting_index = self.datetonum()*96
        ending_index = starting_index + 96

        #dobivanje 96 uzoraka te pretvorba W -> Wh
        PV_prod_power = PV_prod[starting_index:ending_index]*self.PV_power*self.numberofPV 
        PV_prod_energy = PV_prod_power* 15/60
        return PV_prod_power,PV_prod_energy, sum(PV_prod_energy)/1000
        
    def datetonum(self):
        months = {
            1: 31,  # January
            2: 28,  # February
            3: 31,  # March
            4: 30,  # April
            5: 31,  # May
            6: 30,  # June
            7: 31,  # July
            8: 31,  # August
            9: 30,  # September
            10: 31, # October
            11: 30, # November
            12: 31  # December
        }

        sum_of_moths_before = sum(months[i] for i in range(1,self.month))

        total_sum = sum_of_moths_before + self.day - 1

        return total_sum
