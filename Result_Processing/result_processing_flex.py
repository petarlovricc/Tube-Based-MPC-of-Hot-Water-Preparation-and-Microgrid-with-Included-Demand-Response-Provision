from MILP_formulation.extrasprojekt import *
from MILP_formulation.MILP_peak_power import getThetax
from MILP_formulation.MILP_peak_power import getPsix
import pandas as pd
import numpy as np
from Parameters.getData_flex import get_Ki
from Parameters.getData_flex import get_Kzx
import matplotlib.pyplot as plt
import MILP_formulation.MILP_flex as flex
from Parameters.getData_flex import getData
from MILP_solve.milp_solve_flex import _solve_cplex
import sys
print("Python koji se koristi:", sys.executable)


def result_processing(data, model, matrices, matrices_alt, solution):
    res = Structure()
    res.case = "flex"
    res.delte = solution[data.n_x:data.n_x+data.n_u*data.N:3]
    res.Ech_nom = solution[data.n_x+1:data.n_x+data.n_u*data.N:3]
    res.Edch_nom = solution[data.n_x+2:data.n_x+data.n_u*data.N:3]
    res.x_0 = solution[0:data.n_x]

    U_alt_beg = data.n_x+data.n_u*data.N
    U_alt_end = U_alt_beg + data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)
    res.delte_alt = solution[U_alt_beg:U_alt_end:3]
    res.Ech_alt = solution[U_alt_beg+1:U_alt_end:3]
    res.Edch_alt = solution[U_alt_beg+2:U_alt_end:3]
    

    Eps_abs_beg = U_alt_end
    Eps_abs_end = Eps_abs_beg + data.N_R*data.n_a*data.n_z
    res.eps_abs_alt = solution[Eps_abs_beg:Eps_abs_end]

    da_beg = Eps_abs_end
    da_end = Eps_abs_end + data.N
    res.da = solution[da_beg: da_end]
    epp_beg = da_end
    epp_end = da_end + 1 + data.n_a
    res.epp = solution[epp_beg:epp_end]
    res.epp_nom = res.epp[0]
    res.epp_alt = res.epp[1:]
    res.Pr = solution[-2]
    res.emax = solution[-1]

    res.grid_energy_nom = data.nc_load_energy - data.pv_energy + data.P_heater*data.ts*res.delte + res.Ech_nom - res.Edch_nom
    res.K_i = get_Ki(data)
    K_zx = get_Kzx(data)
    res.K_i_x = np.zeros((res.K_i.shape[0],res.K_i.shape[1]+1*data.n_z))
    for i in range(res.K_i.shape[0]):
        for j in range(data.n_z):
            res.K_i_x[i][j*(data.act_len+1):(j+1)*(data.act_len+1)] = np.append(res.K_i[i][j*data.act_len:(j+1)*data.act_len], int(K_zx[i][j]))

    theta_alt = flex.getTheta_a(data, matrices_alt, model)
    psi_alt = flex.get_Psi_x_alt(data, model)

    res.x_alt = theta_alt@solution.reshape(-1,1)+psi_alt

    res.temp_alt = res.x_alt[0::2].ravel()
    res.SOE_alt = res.x_alt[1::2].ravel()
    res.tempC_alt = res.temp_alt - 273.15
    res.SOE_alt = res.x_alt[1::2]


    theta_nom = flex.getTheta_n(data, matrices)
    psi_nom = flex.getPsix_nom(data, matrices)

    res.x_nom = theta_nom@solution.reshape(-1,1)+psi_nom

    res.temp_nom = np.append(res.x_0[0], res.x_nom[0::2])
    res.SOE_nom = np.append(res.x_0[1], res.x_nom[1::2])
    res.tempC_nom = res.temp_nom - 273.15
    dict_temp_alt = dict()

    

   
   
    res.talt = np.zeros((data.n_a,data.n_z*(data.N_F+data.N_R+1)))

    for i in range(data.n_a):
        for z in range(data.n_z):
            res.talt[i][z*(data.N_F+data.N_R+1): (z+1)*(data.N_F+data.N_R+1)] = res.temp_alt[i*data.n_z*(data.N_F+data.N_R+1) + z*(data.N_F+data.N_R+1):i*data.n_z*(data.N_F+data.N_R+1) + (z+1)*(data.N_F+data.N_R+1)]


    res.salt = np.zeros((data.n_a,data.n_z*(data.N_F+data.N_R+1)))

    for i in range(data.n_a):
        for z in range(data.n_z):
            res.salt[i][z*(data.N_F+data.N_R+1): (z+1)*(data.N_F+data.N_R+1)] = res.SOE_alt.ravel()[i*data.n_z*(data.N_F+data.N_R+1) + z*(data.N_F+data.N_R+1):i*data.n_z*(data.N_F+data.N_R+1) + (z+1)*(data.N_F+data.N_R+1)]
    

    res.nc_load_energy_alt = np.zeros((data.n_a,data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a):
        for j in range(data.n_z*(data.N_F+data.N_R)):
            res.nc_load_energy_alt[i][j] = data.nc_load_energy[int(res.K_i[i][j])]


    res.pv_energy_alt = np.zeros((data.n_a,data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a):
        for j in range(data.n_z*(data.N_F+data.N_R)):
            res.pv_energy_alt[i][j] = data.pv_energy[int(res.K_i[i][j])]



    delte_profili = np.zeros((data.n_a,data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a):
        delte_profili[i] = res.delte_alt[i*data.n_z*(data.N_F+data.N_R):(i+1)*data.n_z*(data.N_F+data.N_R)]

    Ech_profili = np.zeros((data.n_a,data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a):
        Ech_profili[i] = res.Ech_alt[i*data.n_z*(data.N_F+data.N_R):(i+1)*data.n_z*(data.N_F+data.N_R)]

    Edch_profili = np.zeros((data.n_a,data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a):
        Edch_profili[i] = res.Edch_alt[i*data.n_z*(data.N_F+data.N_R):(i+1)*data.n_z*(data.N_F+data.N_R)]

    
    res.grid_energy_alt = np.zeros((data.n_a,data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a):
        res.grid_energy_alt[i] = res.nc_load_energy_alt[i] - res.pv_energy_alt[i] + data.P_heater*data.ts*delte_profili[i] + Ech_profili[i] - Edch_profili[i]


    grid_nom_alt = np.zeros((data.n_a,data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a):
        for j in range(data.n_z*(data.N_F+data.N_R)):
            grid_nom_alt[i][j] = res.grid_energy_nom[int(res.K_i[i][j])]

    res.Jn = get_Jn(data, res)
    maxInd, Jai  = calculateJai(data, res)
    res.maxJai = Jai[maxInd]
    res.grid_power_nom = res.grid_energy_nom*4
    res.grid_power_alt = res.grid_energy_alt*4


    res.JDR = getJDR(data, res)
    
    ####################################
    res.table, res.worst_ind = getTable(data, res)

    return res

def getTable(data,res):
    resultlist = np.zeros((10,data.n_a))
    maxJai, Jai = calculateJai(data, res)
    Jn = get_Jn(data, res)
    intraday = get_intraday(data,res)
    for i in range(data.n_a):
        resultlist[0][i] = sum(res.da)
        resultlist[1][i] = -1
        resultlist[2][i] = res.epp_nom * data.cpp
        resultlist[3][i] = res.epp_alt[i] * data.cpp
        resultlist[4][i] = intraday[i]
        resultlist[5][i] = res.Pr
        resultlist[6][i] = Jai[i]
        resultlist[7][i] = Jn
        resultlist[8][i] = -1
        resultlist[9][i] = res.JDR
    return resultlist, maxJai

def calculateJai(data,res):
    Jai = np.zeros(data.n_a)
    for i in range(data.n_a):
        Jai[i] = data.cpp*res.epp_alt[i]+sum(res.da)+sum(res.eps_abs_alt[i*data.N_R*data.n_z:(i+1)*data.N_R*data.n_z])*data.cid

    maxJai = np.where(Jai == max(Jai))[0][0]

    return maxJai, Jai

def get_intraday(data, res):
    id = np.zeros(data.n_a)
    for i in range(data.n_a):
        id[i] = sum(res.eps_abs_alt[i*data.N_R*data.n_z:(i+1)*data.N_R*data.n_z])*data.cid
    return id

def getJDR(data, res):
    return res.Jn - data.alfa*data.cr*data.sgn_Pr*res.Pr+data.alfa*max(res.maxJai-res.Jn, 0)

def get_Jn(data,res):
    Jn =  data.cpp*res.epp_nom + sum(res.da)
    return Jn

def plot_state(data, res, scen, var):

    if (var == "heater"):
        alt = res.temp_alt - 273.15
        nom = res.temp_nom - 273.15
    
    elif (var == "batt"):
        alt = res.SOE_alt.ravel()
        nom = res.SOE_nom

    alt_indices = res.K_i_x[scen]

    act_indices = np.zeros((data.n_z, data.N_F+data.N_R+1))

    for z in range(data.n_z):
        act_indices[z] = alt_indices[z*(data.N_F+data.N_R+1) : (z+1)*(data.N_F+data.N_R+1)] 

    
    alt_values = alt[scen*data.n_z*(data.N_F+data.N_R+1): (scen+1)*data.n_z*(data.N_F+data.N_R+1)]

    act_values = np.zeros((data.n_z, data.N_F+data.N_R+1))

    for z in range(data.n_z):
        act_values[z] = alt_values[z*(data.N_F+data.N_R+1) : (z+1)*(data.N_F+data.N_R+1)] 

    
    plt.plot(np.arange(data.N+1), nom, color = "blue")

    for z in range(data.n_z):
        pre_act_ind = np.arange(act_indices[z][0])
        pre_act_val = [nom[ind] for ind in pre_act_ind.astype("i")]

        act_ind = act_indices[z]
        act_val = act_values[z]

        post_act_ind = np.arange(int(act_indices[z][-1])+1,data.N+1)
        post_act_val = [nom[ind] for ind in post_act_ind.astype("i")]

        if(0 in act_ind):
            index = np.where(act_ind==0)[0][0]
            #plt.plot(pre_act_ind, pre_act_val, color = "blue")
            plt.plot(np.append(act_ind[:index],data.N), act_val[:index+1], color = "orange")
            plt.plot(act_ind[index:], act_val[index:], color = "orange")
            #plt.plot(post_act_ind, post_act_val, color = "blue")
        else:
            #plt.plot(pre_act_ind, pre_act_val, color = "blue")
            plt.plot(act_ind, act_val, color = "orange")
            #plt.plot(post_act_ind, post_act_val, color = "blue")


    plt.show()


def plot_input_output(data, res, scen, var):

    if (var == "Ech"):
        alt = res.Ech_alt
        nom = res.Ech_nom
    
    elif (var == "Edch"):
        alt = res.Edch_alt
        nom = res.Edch_nom
    
    elif (var == "delte"):
        alt = res.delte_alt
        nom = res.delte

    elif (var == "grid"):
        alt = res.grid_energy_alt.ravel()
        nom = res.grid_energy_nom

    alt_indices = res.K_i[scen]

    act_indices = np.zeros((data.n_z, data.N_F+data.N_R))

    for z in range(data.n_z):
        act_indices[z] = alt_indices[z*(data.N_F+data.N_R) : (z+1)*(data.N_F+data.N_R)] 

    
    alt_values = alt[scen*data.n_z*(data.N_F+data.N_R): (scen+1)*data.n_z*(data.N_F+data.N_R)]

    act_values = np.zeros((data.n_z, data.N_F+data.N_R))

    for z in range(data.n_z):
        act_values[z] = alt_values[z*(data.N_F+data.N_R) : (z+1)*(data.N_F+data.N_R)] 

    
    
    plt.step(np.arange(data.N), nom, color = "blue", where="post", linestyle='dashed')
    for z in range(data.n_z):
       
        pre_act_ind = np.arange(act_indices[z][0])
        
        pre_act_val = [nom[ind] for ind in pre_act_ind.astype("i")]

        act_ind = act_indices[z]
        act_val = act_values[z]

        post_act_ind = np.arange(int(act_indices[z][-1])+1,data.N)
        post_act_val = [nom[ind] for ind in post_act_ind.astype("i")]

        if(0 in act_ind):
            index = np.where(act_ind==0)[0][0]
            plt.step(act_ind[:index], act_val[:index], color="orange", where="post", linestyle='dashed')
            plt.step(act_ind[index:], act_val[index:], color="orange", where="post", linestyle='dashed')
        
        else:
             plt.step(act_ind, act_val, color="orange", where="post", linestyle='dashed')


        if(nom[int(act_ind[0])-1] != act_val[0]):
            plt.step(np.append(int(act_ind[0]),int(act_ind[0])) , np.append(act_val[0], nom[int(act_ind[0])]), color="green", where="post", linestyle='dotted')
            #plt.step(act_ind, act_val, color="orange", where="post")
        
        if(nom[int(act_ind[-1])+1] != act_val[-1]):
            plt.step(np.append(int(act_ind[-1]),int(act_ind[-1])) , np.append(act_val[-1], nom[int(act_ind[-1])]), color="green", where="post", linestyle='dotted')
            #plt.step(act_ind, act_val, color="orange", where="post")
        else:
            #plt.step(act_ind, act_val, color="orange", where="post")
            pass

    plt.show()



if __name__ == "main":

    # --- parametri koji se ne mijenjaju -------------------------------------------------
    # === 2. Fiksni parametri ====================================================
    heater_power   = 2500      # [W]
    bat_cap        = 9400      # [Wh]
    converter_power = 2500     # [W]
    tank_volume    = 190       # [L]
    PV_power       = 410       # [W] po modulu
    numberofPV     = 10
    buyPriceHigh   = 0.18      # [€/kWh]
    buyPriceLow    = 0.09      # [€/kWh]

    month, day     = 7, 4      # 4. srpnja
    cpp            = 3.6       # [€/kWh] – kazna za energiju na dan unaprijed
    Q, F, R        = 12, 1, 2
    begin_flex, end_flex = 11, 12
    cr, sgn_Pr     = 0.7, 1
    cid            = 1.2 * buyPriceHigh   # kazna za intraday odstupanje
    heater_mode    = "C"       # ili "H", ovisno što vaš solver očekuje
    alpha = 0.8

    # === 3. Skup α koje testiramo ==============================================
    alpha_vec = [0.1, 0.3, 0.5, 0.7, 1]

    # === 4. Spremnik rezultata ==================================================
    records = []   # (alpha, Pr, epp_nom, worst_ind, Jn, maxJai)

    # === 5. Petlja optimizacije =================================================
    for alpha in alpha_vec:
        # --- 5.1 generiraj ulazne podatke
        data = getData(
            heater_power, bat_cap, converter_power, tank_volume,
            PV_power, numberofPV, buyPriceHigh, buyPriceLow,
            month, day, cpp, Q, F, R,
            begin_flex, end_flex,
            alpha, cr, sgn_Pr, cid,
        )

        # --- 5.2 model + matrice
        model         = flex.getModel(data)
        matrices      = flex.get_Matrices_nom(data, model)
        matrices_alt  = flex.getMatrices_alt(data, model)

        lb   = flex.getLb(data, matrices, matrices_alt)
        ub   = flex.getUb(data, matrices, matrices_alt)
        Aiq  = flex.getAineq(data, matrices, model, matrices_alt)
        biq  = flex.getbineq(data, matrices, matrices_alt, model)
        Aeq  = flex.getAeq(data, model, matrices, matrices_alt)
        beq  = flex.getbeq(data, matrices)
        f    = flex.getF(data)

        # --- 5.3 rješi MILP (CPLEX)
        sol = _solve_cplex(f, Aeq, beq, Aiq, biq, lb, ub, data, heater_mode).x

        # --- 5.4 obradi rješenje
        res = result_processing(data, model, matrices, matrices_alt, sol)

        # --- 5.5 zapiši ono što ti treba
        records.append(
            dict(alpha=alpha,
                Pr=float(res.Pr),
                epp_nom=float(res.epp_nom),
                worst_ind=int(res.worst_ind),
                Jn=float(res.table[7,0]),       # nominalni trošak
                maxJai=float(res.table[6, res.worst_ind]))  # najgori fleksibilni trošak
        )

    # === 6. Pretvori u DataFrame radi lakše analize =============================
    df = pd.DataFrame(records).set_index("alpha")
    print(df)                       # tablica u konzoli

    # === 7. Publikacijski graf (u boji) ========================================
    plt.rcParams.update({
        "font.family": "serif",      # npr. Times
        "font.size":   11,
        "axes.labelsize": 12,
        "axes.titlesize": 12,
        "legend.fontsize": 11,
    })

    fig, ax = plt.subplots(figsize=(6.3, 4.2))     # ≈ 16 × 10.5 cm

    cmap = plt.cm.get_cmap("viridis")
    ax.plot(df.index, df["maxJai"],
            color=cmap(0.75), marker='o', linewidth=1.8,
            label=r"Rezervirana snaga $P_r$")

    # anotiraj svaku točku
    for a, pr in zip(df.index, df["maxJai"]):
        ax.annotate(f"{pr:.1f}",
                    xy=(a, pr), xytext=(0, 4),
                    textcoords="offset points",
                    ha="center", va="bottom", fontsize=9)

    ax.set_xlabel(r"Vjerojatnost ugovaranja usluge fleksibilnosti $\alpha$ [–]")
    ax.set_ylabel(r"Rezervirana snaga $P_r$ [W]")
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.6)
    ax.set_axisbelow(True)          # da mreža bude ispod krivulje
    ax.legend(frameon=False)

    fig.tight_layout(pad=0.2)
    fig.savefig("Pr_vs_alpha_color.pdf", format="pdf", dpi=600)   # za LATeX/Figure
    fig.savefig("Pr_vs_alpha_color.png", dpi=300)                 # za word/powerpoint
    plt.show()






