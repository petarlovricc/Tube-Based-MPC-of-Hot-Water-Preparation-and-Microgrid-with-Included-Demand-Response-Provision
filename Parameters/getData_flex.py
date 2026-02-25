import numpy as np
from scipy.sparse import csr_matrix
import cplex
import matplotlib.pyplot as plt
from MILP_formulation.extrasprojekt import *
import math
from Profiles_Readers.PV_reader import PVreader
from Profiles_Readers.Disturbances_Reader import CSV_disturbances_reader
from Profiles_Readers.da_prices_reader import CSV_da_reader


#funkcija koja sluzi stvaranju strukture
def getData(heater_power, bat_cap, converter_power, tank_volume,PV_power, numberofPV, month, day, Q, F, R, beginning_flex_ready, end_flex_ready, alfa_plus, alfa_minus,  cr_plus, cr_minus, sgn_Pr, hub_name,
            annual_load, annual_water, neg_prices_on_off):
    data = Structure()
    ######################################################
    #PARAMETRI SUSTAVA
    # print("\n[Kontrolni ispis parametara getData()]")
    # print(f"Heater Power: {heater_power}")
    # print(f"Battery Capacity: {bat_cap}")
    # print(f"Converter Power: {converter_power}")
    # print(f"Tank Volume: {tank_volume}")
    # print(f"PV Power: {PV_power}")
    # print(f"Number of PV: {numberofPV}")
    # print(f"Month: {month}")
    # print(f"Day: {day}")
    # print(f"Q: {Q}")
    # print(f"F: {F}")
    # print(f"R: {R}")
    # print(f"Beginning Flex Ready: {beginning_flex_ready}")
    # print(f"End Flex Ready: {end_flex_ready}")
    #print(f"Alpha: {alfa_plus}")
    #print(f"Alpha: {alfa_minus}")
    # print(f"cr: {cr}")
    # print(f"sgn_Pr: {sgn_Pr}")
    # print("--------------------------------------------------\n")
    data.annual_water = annual_water #vec je u m3 u profilu u csv
    data.annual_load = annual_load*1000 # prilagodi MWh u kWh kao sto je u profilima
    data.Pr_scen = sgn_Pr
    data.hub_name = hub_name
    PV_reader = PVreader(day=day, month=month, PV_power=PV_power, numberofPV=numberofPV) #klasa koja postavlja dan 
    disturbance_reader = CSV_disturbances_reader(day=day, month=month, watertemp = 40, hub_name= hub_name)
    da_prices_reader = CSV_da_reader(day=day, month = month)
    data.day = day
    data.month = month
    data.watertemp = 40
    #Podatci o dimen_zijama matrica
    data.sgn_Pr = sgn_Pr
    data.cr_minus = cr_minus/1000
    data.alfa_plus = alfa_plus/100
    data.cr_plus = cr_plus/1000
    data.alfa_minus = alfa_minus/100
    data.N =  96 #broj 15min intervala u jednom danu
    data.N_F = int(F*4)
    data.N_R = int(R*4)
    data.N_Q = int(Q*4)
    data.n_a = int((end_flex_ready - beginning_flex_ready)*4)
    data.n_z = data.N // (data.N_Q)
    data.n_x = 2 #[T(k) SOE(k)]
    data.n_u = 4
    data.len_U_nom = data.n_u*data.N #duljina upravljackog ulaza nominalnog profila
    data.len_Ua = data.n_u*data.n_a*data.n_z*(data.N_F + data.N_R)
    data.len_eps_abs = data.N_R*data.n_a*data.n_z
    data.len_eps_da = data.N #duljina vektora epsilona day ahead energije
    data.len_epp_nom = 1 #epsilon za peak power bez fleksibilnosti
    data.len_epp_alt = data.n_a

    #duljina optimizacijskog vektora
    data.len_chi = (data.n_x + data.len_U_nom +2*data.len_Ua
                    + 2*data.len_eps_abs+ data.len_eps_da +2*data.len_epp_alt+ data.len_epp_nom+2+2+1)
    print(data.len_chi)

    data.P_heater = heater_power*1000 #snaga grijača u W
    data.ts = 0.25 #duljina perioda diskretizacije u satima
    data.E_bat_max = bat_cap*1000 #kapacitet baterije u Wh
    data.P_PC = converter_power*1000 #snaga pretvarača snage
    data.tank_volume = tank_volume #volumen vode u spremniku(m3)
    data.tank_radius = (data.tank_volume / (4 * math.pi))**(1/3)  #promjer spremnika vode
    data.tank_area = 10 * math.pi * data.tank_radius**2  #vanjska povrsina spremnika vode
    data.Lambda = 0.0245 #koeficijent toplinske vodljivosti
    data.thickness = 0.05 #debljina spremnika vode u m
    data.R = data.thickness/(data.Lambda*data.tank_area) 
    data.ro_water = 1000 #kg/m3
    data.c_water = 4200/3600 #Wh(kg^-1)(K^-1)
    data.nCh = 0.9 #efikasnost punjenja baterije
    data.nDch = 0.9 #efikasnost pražnjenja baterije



    data.m_w_tank = data.tank_volume*data.ro_water
    data.cold_water_temp = 7+273.15 #temperatura hladne vode (°C -> K) 
    data.boiling_temp = 100+273.15 # maksimalna željena temperatura vode u grijaču

    #Podatci o proizvodnji i potrošnji
    data.pv_power, data.pv_energy, data.pv_energy_sum = PV_reader.csvreader()
    data.env_temp_K, data.env_temp_C = disturbance_reader.environment_Temperature()
    data.set_water_temp_K, data.set_water_temp_C = disturbance_reader.setWaterTemparray(data.watertemp)


    data.water_demand_not_scaled_volume_flow, data.total_water_consumption_m3 = disturbance_reader.csvreaderWater() #m3/h



    data.water_demand = data.water_demand_not_scaled_volume_flow*data.ro_water * (data.annual_water/data.total_water_consumption_m3)
    data.nc_load_power_not_scaled, data.nc_load_energy_not_scaled, data.sum_nc_load_energy, data.annual_consumption = disturbance_reader.csvreaderElectricity()
    data.nc_load_power = data.nc_load_power_not_scaled * (data.annual_load/data.annual_consumption)
    data.nc_load_energy = data.nc_load_energy_not_scaled * (data.annual_load/data.annual_consumption)

    data.mul_TQ = data.set_water_temp_K*data.water_demand

    #Cijene davanja i preuzimanja te cijena vršne snage
    len_mon = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    cpp = 4.188 #[€/kW]
    data.cpp = cpp/(1000*len_mon[month-1])  #cijena vrsne snage €/kWh --> €/Wh te na razini jednog dana

    renewable_energy_charge_eur_per_kwh = 0.013239/1000
    excise_duty_eur_per_kwh = 0.0005/1000
    commission = 0.08

    data.da_prices_reader = da_prices_reader.csvreaderPrices()
    day_ahead_prices = data.da_prices_reader + renewable_energy_charge_eur_per_kwh
    + excise_duty_eur_per_kwh

    data.day_ahead_prices = data.da_prices_reader

    if(neg_prices_on_off == True):
        data.da_prices = np.where(
                day_ahead_prices >= 0,
                day_ahead_prices * (1 + commission),
                day_ahead_prices * (1 - commission),
            )
    else:
        data.da_prices = np.clip(np.where(
                    day_ahead_prices >= 0,
                    day_ahead_prices * (1 + commission),
                    day_ahead_prices * (1 - commission),
                ), a_min=renewable_energy_charge_eur_per_kwh
        + excise_duty_eur_per_kwh* (1 + commission), a_max=None)



    sell_prices = setConvexPrices(data)
    data.sell_prices = np.where(
                sell_prices >= 0,
                sell_prices * (1 - commission),
                sell_prices * (1 + commission),
            )
    

    
    data.cid = 1.2*max(data.da_prices)
    
    #######################################################
    #SKUPOVI TRENUTAKA ALTERNATIVNIH SCENARIJA

    data.act_len = (data.N_F+data.N_R)
    
    data.a_i = np.arange(data.n_a)
    data.a_i_z = np.arange(data.act_len)
   

    data.Ka_min = np.arange(int(beginning_flex_ready*4),int(end_flex_ready*4))
    data.K_i = get_Ki(data)
    data.Kzx = get_Kzx(data)
    data.Kzu = get_Kzu(data)
    data.K_fi = get_Kfi(data)
    data.K_ri = get_Kri(data)


    #######################################################
    #OGRANIČENJA

    #Gornje i donje granice protoka i temperature
    data.Qmax = data.water_demand.max() #maksimalni protok vode u danu
    print(f"Qmax: {data.Qmax}")

    data.Tmax = 80+273.15

    return data


def setConvexPrices(data):
    sellPrices = np.zeros(96)
    for i in range(len(data.da_prices_reader)):
        if(data.da_prices_reader[i]>=0):
            sellPrices[i] = data.da_prices_reader[i]*0.9
        else:
             sellPrices[i] = (1/0.9)*data.da_prices_reader[i]
    return sellPrices
    
        
        
def get_Ki(data):
        data.K_i = np.zeros((data.n_a,data.n_z*data.act_len))

        for i in data.a_i:
            for k in range(data.n_z*data.act_len):
                    data.K_i[i,k] = (data.Ka_min[i] + (k//data.act_len)*data.N_Q + k%data.act_len)
        
        return data.K_i%data.N

def get_Kpi(data):
    K_pi = np.zeros((data.n_a,data.n_z))

    for i in data.a_i:
        for k in range(data.n_z):
                K_pi[i,k] = data.Ka_min[i] + k*data.N_Q
      
    return K_pi%data.N
     

def get_Kzu(data):
    K_zu = np.zeros((data.n_a,data.n_z))

    for i in data.a_i:
        for k in range(data.n_z):
                K_zu[i,k] = data.Ka_min[i] + k*data.N_Q + data.act_len-1
      
    return K_zu%data.N
       
        
def get_Kzx(data):
    K_zx = get_Kzu(data) + 1
      
    return K_zx%data.N


def get_Kfi(data):
    K_fi = np.zeros((data.n_a,data.N_F*data.n_z))

    K_i = get_Ki(data)

    for i in data.a_i:
        for k in range(data.n_z):
            K_fi[i,k*data.N_F: (k+1)*data.N_F] = K_i[i, k*data.act_len: k*data.act_len + data.N_F]
     
    return K_fi%data.N
        
def get_Kri(data):
    K_ri = np.zeros((data.n_a,data.N_R*data.n_z))

    K_i = get_Ki(data)

    for i in data.a_i:
        for k in range(data.n_z):
            K_ri[i,k*data.N_R: k*data.N_R + data.N_R] = K_i[i, k*data.act_len + data.N_F: k*data.act_len + data.N_F + data.N_R]
     
    return K_ri%data.N


        
if __name__ == "__main__":
    heater_power=2500
    bat_cap=9400
    converter_power=2500
    tank_volume=190
    PV_power=410
    numberofPV=10
    month=7
    day=4
    Q =8
    F = 2
    R = 5
    beginning_flex_ready = 11
    end_flex_ready = 12
    alfa = 1
    sgn_Pr = 1
    cr = 0.7
    
    data = getData(
            heater_power,
            bat_cap,
            converter_power,
            tank_volume,
            PV_power,
            numberofPV,
            month,
            day,
            Q,
            F,
            R,
            beginning_flex_ready,
            end_flex_ready,
            alfa,
            cr,
            sgn_Pr
        )
    print(get_Kfi(data))
    print(get_Kri(data))