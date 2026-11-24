import numpy as np
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
from MILP_formulation_accelerated.extrasprojekt import *
import math
from Profiles_Readers.PV_reader import PVreader
from Profiles_Readers.Disturbances_Reader import CSV_disturbances_reader
from Profiles_Readers.da_prices_reader import CSVDaReader


RENEWABLE_ENERGY_CHARGE_EUR_PER_WH = 0.013239  / 1000
EXCISE_DUTY_EUR_PER_WH = 0.0005 / 1000
ENERGY_PRICE_COMMISION = 0.08

# Profiles are for 2024 (leap year), so February has 29 days
DAYS_IN_MONTH = np.array([31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])

TARIFF_MODELS = {
    "LV red (3)": {"energy": 28.78 / 1e6, "peak": 6.559},
    "MV white (2)": {"energy": 18.71 / 1e6, "peak": 4.341},
    "HV white (1)": {"energy": 5.18 / 1e6, "peak": 2.289},
    "LV household white (8)" : {"energy": 50.28 / 1e6, "peak": 0.0}
}

LV_MV_LIMIT_W = 300e3  # approximate peak power limit, low / medium voltage
MV_HV_LIMIT_W = 10e6  # approximate peak power limit, medium / high voltage



def set_tariff_model(peak_power_W: np.ndarray, hub_name: str):
    """
    Choose the network tariff model from the peak of the load profile.

    Returns the tariff model name, network energy charge [EUR/Wh]
    and peak power price [EUR/kW per month].
    """
    peak = np.max(peak_power_W)

    if hub_name == "Household":
        model = "LV household white (8)"
    elif peak <= LV_MV_LIMIT_W:
        model = "LV red (3)"
    elif peak <= MV_HV_LIMIT_W:
        model = "MV white (2)"
    else:
        model = "HV white (1)"

    return model, TARIFF_MODELS[model]["energy"], TARIFF_MODELS[model]["peak"]


def _price_formation(price, which_price, neg_buy_price, network_charge: float):
    """Marza samo na energiju; mrezna naknada, OIE i trosarina samo na kupnju."""
    c = ENERGY_PRICE_COMMISION
    if which_price == "buy":
        energy = np.where(price >= 0, price * (1 + c), price * (1 - c))
        if not neg_buy_price:
            energy = np.maximum(energy, 0.0)
        return energy + network_charge + RENEWABLE_ENERGY_CHARGE_EUR_PER_WH + EXCISE_DUTY_EUR_PER_WH
    elif which_price == "sell":
        return np.where(price >= 0, price * (1 - c), price * (1 + c))
    raise ValueError("Set the correct price direction: 'buy' or 'sell'!")


#funkcija koja sluzi stvaranju strukture
def getData(heater_power, bat_cap, converter_power, tank_volume,PV_power, numberofPV, month, day, Q, F, R, beginning_flex_ready, end_flex_ready, alfa_plus, alfa_minus,  cr_plus, cr_minus, sgn_Pr, hub_name,
            annual_load, annual_water, neg_prices_on_off, year=2024, timezone="Zagreb", country_code="HR", duration=24):
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
    da_reader = CSVDaReader(
        day=day,
        month=month,
        year = year,
        timezone = timezone,
        country_code = country_code,
        duration = duration

    )
    data.day = day
    data.month = month
    data.watertemp = 40
    #Podatci o dimen_zijama matrica
    data.sgn_Pr = sgn_Pr
    data.cr_minus = cr_minus/1000#*(end_flex_ready - beginning_flex_ready)
    data.alfa_plus = alfa_plus/100
    data.cr_plus = cr_plus/1000#*(end_flex_ready - beginning_flex_ready)
    data.alfa_minus = alfa_minus/100
    data.N =  96 #broj 15min intervala u jednom danu
    data.N_F = int(F*4)
    data.N_R = int(R*4)
    data.N_Q = int(Q*4)
    data.n_a = min(int((end_flex_ready - beginning_flex_ready)*4), data.N_Q)
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

    #######################################################
    #Ograničenja za histerzno upravljanje grijačem vode
    data.hist_donja = 0.5      
    data.hist_gornja = 1.5


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
    data.year = year
    data.timezone = timezone
    data.country_code = country_code
    data.duration = duration
    data.negative_buying_price_allowed = neg_prices_on_off

    annual_peak_not_scaled, data.load_factor = disturbance_reader.annual_peak_and_load_factor()
    data.annual_peak_power = annual_peak_not_scaled * (data.annual_load/data.annual_consumption)  # W

    data.day_ahead_prices = da_reader.csvreaderPrices().reshape(-1)/1e6 #EUR/MWh -> EUR/Wh

    tariff_model, network_charge, peak_price = set_tariff_model(data.annual_peak_power, data.hub_name)
    data.da_prices = _price_formation(
        data.day_ahead_prices,
        "buy",
        data.negative_buying_price_allowed,
        network_charge
    )

    data.sell_prices = _price_formation(data.day_ahead_prices, "sell", data.negative_buying_price_allowed,
                                          network_charge)

    data.tariff_model = tariff_model
    # Peak power price in EUR/W of peak power per day (monthly price spread over days in month)
    data.cpp = peak_price / (DAYS_IN_MONTH[month - 1] * 1000)

    data.cid = 1.2*data.da_prices
    data.cid = np.clip(data.cid, a_min=0, a_max=None)
    
    #######################################################
    #SKUPOVI TRENUTAKA ALTERNATIVNIH SCENARIJA

    
    
    data.a_i = np.arange(data.n_a)
    data.a_i_z = np.arange((data.N_F+data.N_R))
   

    data.Ka_min = np.arange(int(beginning_flex_ready*4),int(beginning_flex_ready*4) + data.n_a)
    data.K_i = get_Ki(data)
    data.K_i.setflags(write = False)
    data.Kzx = get_Kzx(data)
    data.Kzu = get_Kzu(data)
    data.K_fi = get_Kfi(data)
    data.K_ri = get_Kri(data)


    #######################################################
    #OGRANIČENJA

    #Gornje i donje granice protoka i temperature
    data.Qmax = data.water_demand.max() #maksimalni protok vode u danu
   
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
        K_i = np.zeros((data.n_a,data.n_z*(data.N_F+data.N_R)))

        for i in data.a_i:
            for k in range(data.n_z*(data.N_F+data.N_R)):
                    K_i[i,k] = (data.Ka_min[i] + (k//(data.N_F+data.N_R))*data.N_Q + k%(data.N_F+data.N_R))
        
        return K_i%data.N

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
                K_zu[i,k] = data.Ka_min[i] + k*data.N_Q + (data.N_F+data.N_R)-1
      
    return K_zu%data.N
       
        
def get_Kzx(data):
    K_zx = get_Kzu(data) + 1
      
    return K_zx%data.N


def get_Kfi(data):
    K_fi = np.zeros((data.n_a,data.N_F*data.n_z))

    K_i = get_Ki(data)

    for i in data.a_i:
        for k in range(data.n_z):
            K_fi[i,k*data.N_F: (k+1)*data.N_F] = K_i[i, k*(data.N_F+data.N_R): k*(data.N_F+data.N_R) + data.N_F]
     
    return K_fi%data.N
        
def get_Kri(data):
    K_ri = np.zeros((data.n_a,data.N_R*data.n_z))

    K_i = get_Ki(data)

    for i in data.a_i:
        for k in range(data.n_z):
            K_ri[i,k*data.N_R: k*data.N_R + data.N_R] = K_i[i, k*(data.N_F+data.N_R) + data.N_F: k*(data.N_F+data.N_R) + data.N_F + data.N_R]
     
    return K_ri%data.N


   