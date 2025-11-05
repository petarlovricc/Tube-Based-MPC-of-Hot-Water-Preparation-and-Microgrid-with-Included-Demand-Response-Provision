
import numpy as np
import matplotlib.pyplot as plt
from MILP_formulation.extrasprojekt import *

from MILP_formulation.MILP_peak_power import getModel

def histereza(data, res):

    model = getModel(data)
    Ebat = []
    temperature = []
    Emreza_arr = []
    delte = []
    x_0 = res.x_0
    temp_0 = x_0[0]
    soc_0 = x_0[1]
    SOC = soc_0
    SOC_arr = []
    delta_k = res.delte[0]
    temperature.append(temp_0)
    Thot_k = temp_0
    SOC_arr.append(SOC)
    delte.append(delta_k)

    for indeks in range(1,data.N+1):
        
        Thot_k = model.a11*Thot_k+model.b11*delta_k+model.c11*data.env_temp_K[indeks-1]+model.d11*data.mul_TQ[indeks-1]+model.e11*data.water_demand[indeks-1]
        temperature.append(Thot_k)
        Ebat_new = data.pv_energy[indeks-1] - data.nc_load_energy[indeks-1]  - data.P_heater*data.ts*delta_k 
        

        if(Thot_k < data.set_water_temp_K[indeks-1]+2):
            delta_k = 1
        else:
            delta_k = 0
        
        if(Ebat_new >= 0):
            Ebat_pom = min(Ebat_new, data.P_PC*data.ts, (0.8*data.E_bat_max - SOC)/data.nCh)
            Egrid = Ebat_pom - Ebat_new
            SOC = SOC + Ebat_pom*data.nCh

        elif(Ebat_new < 0):
            Ebat_pom = max(Ebat_new, -data.P_PC*data.ts, -(SOC - 0.2*data.E_bat_max)*data.nDch)
            Egrid = Ebat_pom - Ebat_new
            SOC = SOC + Ebat_pom/data.nDch

        delte.append(delta_k)
        

        Ebat.append(Ebat_pom)
        SOC_arr.append(SOC)
        Emreza_arr.append(Egrid)
    
    
    
    tempC = []
    for i in range (data.N+1):
        tempC.append(temperature[i]-273.15)
    hist = Structure()
    hist.case = "hist"
    hist.epsiloni = []
    hist.Ech = [0]*96
    hist.Edch = [0]*96
    for i in range(data.N):
        if Emreza_arr[i] >= 0:
            hist.epsiloni.append(Emreza_arr[i]*data.da_prices[i])
        else:
            hist.epsiloni.append(Emreza_arr[i]*data.sell_prices[i])
    
 

    hist.Ebat = np.array(Ebat)
    hist.Ech = []
    hist.Edch = []
    for i in hist.Ebat:
        if (i >= 0):
            hist.Ech.append(i)
        else: 
            hist.Ech.append(0)

    for i in hist.Ebat:
        if (i <= 0):
            hist.Edch.append(-i)
        else: 
            hist.Edch.append(0)
    
    hist.temp = np.array(temperature)
    hist.SOE = np.array(SOC_arr)
    hist.delte = np.array(delte)[:-1]
    hist.grid_energy = np.array(Emreza_arr)
    hist.tempC = tempC
    hist.PPV_used = data.pv_power
    
    sumaNovaca = 0

    for i in range(data.N):
        if (hist.grid_energy[i] < 0):
            sumaNovaca+= hist.grid_energy[i]*data.sell_prices[i] #energija Wh U kWh
        else:
            sumaNovaca+=hist.grid_energy[i]*data.da_prices[i]
          
    #dodavanje troska vrsne snage
    hist.grid_power = hist.grid_energy*4

    sumaNovaca+=max(hist.grid_power)*data.cpp

    hist.Jn = sumaNovaca
    
       
    hist.table = getTable(data, hist)
    hist.table2 = getTable_flow(data,hist)
    

    return hist




def getTable(data,hist):
    resultlist = np.zeros((10,1))
    resultlist[0][0] = sum(hist.epsiloni)
    resultlist[1][0] = max(hist.grid_power)*data.cpp
    resultlist[2][0] = -1
    resultlist[3][0] = -1
    resultlist[4][0] = -1
    resultlist[5][0] = -1
    resultlist[6][0] = -1
    resultlist[7][0] = -1
    resultlist[8][0] = hist.Jn
    resultlist[9][0] = -1
    return resultlist


def getTable_flow(data,hist):
    resultlist = np.zeros((6,1))
    resultlist[0][0] = -1
    resultlist[1][0] = -1
    resultlist[2][0] = sum(hist.delte*data.P_heater)*0.25/1000
    resultlist[3][0] = -1
    resultlist[4][0] = -1
    resultlist[5][0] = sum(hist.grid_energy)/1000
    return resultlist


def runHistereza(data, res, count):
    for i in range(count):
        hist = histereza(data, res)
        res.x_0[0] = hist.temp[-1]
        res.x_0[1] = hist.SOE[-1]

    return hist