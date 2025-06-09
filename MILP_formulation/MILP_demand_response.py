import numpy as np
from scipy.sparse import csr_matrix
import cplex
import matplotlib.pyplot as plt
from .extrasprojekt import *
import math
from ..Profiles_Readers.PV_reader import PVreader
from ..Profiles_Readers.Disturbances_Reader import CSV_disturbances_reader

#funkcija koja sluzi stvaranju strukture
def getData(heater_power, bat_cap, converter_power, tank_volume,PV_power, numberofPV, buyPriceHigh, buyPriceLow, sellPrice, month, day, setTemp, Q, F, R, beginning_flex_ready, end_flex_ready, cpp):
    data = Structure()

    PV_reader = PVreader(day, month, PV_power, numberofPV) #klasa koja postavlja dan 
    disturbance_reader = CSV_disturbances_reader()
    
    #Podatci o dimenzijama matrica
    data.N =  96 #broj 15min intervala u jednom danu
    data.na = (beginning_flex_ready - end_flex_ready)*4 #broj alternativnih profila
    data.nz = F+R #duljina aktivacije
    data.len_x0 = 2 #[T(k) SOE(k)]
    data.len_Un = 3*data.N #duljina upravljackog ulaza nominalnog profila
    data.len_Uai = 3*data.nz*(F+R) #duljina jednog alternativnog profila
    data.len_eps_abs_i = R*data.nz #duljina jednog vektora epsilona za uravnoteženje
    data.len_eps_da = data.N #duljina vektora epsilona day ahead energije
    data.len_epp_nom = 1 #epsilon za peak power nom
    data.len_epp_alt = data.na #duljina vektora svih peak power alt
    data.len_Pr = 1 #rezervirana snaga
    data.len_eps_max = 1 #epsilon za maksimum u f_krit
    
    #duljina optimizacijskog vektora
    data.len_chi = (data.len_x0 + data.len_Un + data.len_Uai*data.na + 
                    data.len_eps_abs_i*data.na + data.len_eps_da + data.len_epp_nom + 
                    data.len_epp_alt + data.len_Pr + data.len_eps_max)


    data.P_heater = heater_power #snaga grijača u W
    data.ts = 0.25 #duljina perioda diskretizacije u satima
    data.E_bat_max = bat_cap #kapacitet baterije u Wh
    data.P_PC = converter_power #snaga pretvarača snage
    data.tank_volume = tank_volume/1000 #volumen vode u grijaču(m3)
    data.tank_radius = (data.tankVolume / (4 * math.pi))**(1/3)  #promjer spremnika vode
    data.tank_area = 10 * math.pi * data.tank_radius**2  #vanjska povrsina spremnika vode
    data.Lambda = 0.0245 #koeficijent toplinske vodljivosti
    data.thickness = 0.05 #debljina spremnika vode u m
    data.R = data.thickness/(data.Lambda*data.area) 
    data.ro_water = 1000 #kg/m3
    data.c_water = 4200/3600 #Wh(kg^-1)(K-1)
    data.nCh = 0.9 #efikasnost punjenja baterije
    data.nDch = 0.9 #efikasnost pražnjenja baterije


    data.cold_water_temp = 7+273.15 #temperatura hladne vode (°C -> K) 
    data.boiling_temp = 100+273.15 # maksimalna željena temperatura vode u grijaču

    
    data.m = [0,0,0]
    data.M = [1,data.PPc*data.ts, data.PPc*data.ts]

    #Podatci o proizvodnji i potrošnji
    data.pv_power, data.pv_energy, data.pv_energy_sum = PV_reader.csvreader()
    data.env_temp_Kelvin, data.env_temp_Celsius = disturbance_reader.environment_Temperature()
    data.set_water_temp_Kelvin, data.set_water_temp_Celsius = disturbance_reader.setWaterTemparray()
    data.water_demand = disturbance_reader.csvreaderWater()
    
    #Cijene davanja i preuzimanja te cijena vršne snage
    data.cpp = cpp  #cijena vrsne snage
    data.c_buy = np.r_[np.repeat(buyPriceLow,28), np.repeat(buyPriceHigh,56)
                       ,np.repeat(buyPriceLow,12)] 
    data.c_sell = data.c_buy*0.8

    
    
    data.qmax = max(data.water)/2
    data.Tmin = []
   
    #nazivna ograničenja
    data.umin = [0,0,0] #donje ograničenje na ulazni vektor u
    data.umax = [1, data.PPc*data.ts, data.PPc*data.ts] #gornje ograničenje na ulazni vektor u

    #data.xmin = [data.Tmin,0.2*data.Cbat]
    #data.xmax = [data.Tmax, 0.8*data.Cbat]
    data.g = [np.exp(-data.ts/(data.R*data.roWater*data.cWater*data.volWater)) for indeks in range (data.N)]

    return data
