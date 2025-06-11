import numpy as np
from scipy.sparse import csr_matrix
import cplex
import matplotlib.pyplot as plt
from MILP_formulation.extrasprojekt import *
import math
import sys
import os

from Profiles_Readers.PV_reader import PVreader
from Profiles_Readers.Disturbances_Reader import CSV_disturbances_reader

def getData(heater_power, bat_cap, converter_power, tank_volume,PV_power, numberofPV, buyPriceHigh, buyPriceLow, month, day, cpp):
    data = Structure()

    PV_reader = PVreader(day=day, month=month, PV_power=PV_power, numberofPV=numberofPV) #klasa koja postavlja dan 
    disturbance_reader = CSV_disturbances_reader()
    
    #Podatci o dimenzijama matrica
    data.N =  96 #broj 15min intervala u jednom danu
    data.len_x0 = 2 #[T(k) SOE(k)]
    data.len_U_noflex = 3*data.N #duljina upravljackog ulaza nominalnog profila
    data.len_eps_da = data.N #duljina vektora epsilona day ahead energije
    data.len_epp_noflex = 1 #epsilon za peak power bez fleksibilnosti
    
    #duljina optimizacijskog vektora
    data.len_chi = (data.len_x0 + data.len_U_noflex + data.len_eps_da + data.len_epp_noflex)


    data.P_heater = heater_power #snaga grijača u W
    data.ts = 0.25 #duljina perioda diskretizacije u satima
    data.E_bat_max = bat_cap #kapacitet baterije u Wh
    data.P_PC = converter_power #snaga pretvarača snage
    data.tank_volume = tank_volume/1000 #volumen vode u spremniku(m3)
    data.tank_radius = (data.tank_volume / (4 * math.pi))**(1/3)  #promjer spremnika vode
    data.tank_area = 10 * math.pi * data.tank_radius**2  #vanjska povrsina spremnika vode
    data.Lambda = 0.0245 #koeficijent toplinske vodljivosti
    data.thickness = 0.05 #debljina spremnika vode u m
    data.R = data.thickness/(data.Lambda*data.tank_area) 
    data.ro_water = 1000 #kg/m3
    data.c_water = 4200/3600 #Wh(kg^-1)(K-1)
    data.nCh = 0.9 #efikasnost punjenja baterije
    data.nDch = 0.9 #efikasnost pražnjenja baterije



    data.m_w_tank = data.tank_volume*data.ro_water
    data.cold_water_temp = 7+273.15 #temperatura hladne vode (°C -> K) 
    data.boiling_temp = 100+273.15 # maksimalna željena temperatura vode u grijaču

    #Podatci o proizvodnji i potrošnji
    data.pv_power, data.pv_energy, data.pv_energy_sum = PV_reader.csvreader()
    data.env_temp_K, data.env_temp_C = disturbance_reader.environment_Temperature()
    data.set_water_temp_K, data.set_water_temp_C = disturbance_reader.setWaterTemparray()
    data.water_demand = disturbance_reader.csvreaderWater() #kg/h
    data.nc_load_power, data.nc_load_energy, data.sum_nc_load_energy = disturbance_reader.csvreaderElectricity()
    data.mul_TQ = data.set_water_temp_K*data.water_demand
    #Cijene davanja i preuzimanja te cijena vršne snage
    data.cpp = cpp/1000  #cijena vrsne snage €/kWh --> €/Wh
    data.c_buy = np.r_[np.repeat(buyPriceLow,28), np.repeat(buyPriceHigh,56)
                       ,np.repeat(buyPriceLow,12)] /1000 #€/kWh --> €/Wh
    data.c_sell = data.c_buy*0.8

    #################################################################################

    #Gornje i donje granice protoka i temperature
    data.Qmax = data.water_demand.max() #maksimalni protok vode u danu

    #Ogranicenje temperature Thot(k) vezano za Qmix(k-1) i Tmix(k-1)
    data.Tmin_interval_before = ((data.water_demand)/data.Qmax*
                                (data.set_water_temp_K-data.cold_water_temp)+data.cold_water_temp).reshape(-1,1)

    #Ogranicenje temperature Thot(k) vezano za Qmix(k) i Tmix(k), s time da je isto ogr. za Qmix(N-1)
    data.Tmin_interval_after = np.r_[data.Tmin_interval_before[1:].ravel(),data.Tmin_interval_before[-1]].reshape(-1,1)
    data.Tmax = data.boiling_temp

    return data