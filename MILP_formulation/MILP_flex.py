import numpy as np
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
from MILP_formulation.extrasprojekt import *
import math


from Parameters.getData_flex import getData
from Parameters.getData_flex import get_Kpi
from Parameters.getData_flex import get_Kfi
from Parameters.getData_flex import get_Kri
from Parameters.getData_flex import get_Ki





def getModel(data):
    model = Structure()
    model.kapa1 = -1/(data.R*data.m_w_tank*data.c_water)
    model.kapa2 = data.P_heater/(data.m_w_tank*data.c_water)
    
    model.a11 = np.exp(model.kapa1*data.ts)
    model.A = np.array([[model.a11, 0],
                       [0, 1]],dtype="float64")
    
    model.b11 = (np.exp(model.kapa1*data.ts)-1)*model.kapa1**-1*model.kapa2
    model.B = np.array([[model.b11, 0, 0, 0],
                       [0, data.nCh, -1/data.nDch, 0]])
    
    model.c11 = (np.exp(model.kapa1*data.ts)-1)*model.kapa1**-1/(data.R*data.m_w_tank*data.c_water)

    model.C = np.array([[model.c11],
                        [0]])
    
    model.d11 = -(np.exp(model.kapa1*data.ts)-1)*model.kapa1**-1/(data.m_w_tank)
    model.D = np.array([[model.d11],
                        [0]])
    
    model.e11 = (np.exp(model.kapa1*data.ts)-1)*model.kapa1**-1*(data.cold_water_temp/data.m_w_tank)
    model.E = np.array([[model.e11],
                        [0]])


    return model


def get_Matrices_nom(data,model):
    matrices = Structure()

    matrices.u_min = np.zeros((data.n_u,1))
    matrices.u_max = np.array([1, data.P_PC*data.ts,data.P_PC*data.ts, np.inf]).reshape(-1,1)


     ######################################
    #Ograničenja stanja nominalnog profila

    matrices.Tmin_interval_before_nom = ((data.water_demand)/data.Qmax*
                                (data.set_water_temp_K-data.cold_water_temp)+data.cold_water_temp).reshape(-1,1)

    #Ogranicenje temperature Thot(k) vezano za Qmix(k) i Tmix(k), s time da je isto ogr. za Qmix(N-1)
    matrices.Tmin_interval_after_nom = np.r_[matrices.Tmin_interval_before_nom[1:].ravel(),matrices.Tmin_interval_before_nom[-1]].reshape(-1,1)


    matrices.x0_min = np.array([matrices.Tmin_interval_before_nom[0][0],0.2*data.E_bat_max]).reshape(-1,1)
    matrices.x0_max = np.array([data.Tmax,0.8*data.E_bat_max]).reshape(-1,1)


    ######################################
    #Ograničenja stanja nominalnog profila


    matrices.X_max_n = np.tile(matrices.x0_max, (data.N,1))

    matrices.X_min_l_n = np.zeros((data.N*2,1))
    matrices.X_min_l_n[::2] = matrices.Tmin_interval_before_nom
    matrices.X_min_l_n[1::2]= 0.2*data.E_bat_max

    matrices.X_min_u_n = np.zeros((data.N*2,1))
    matrices.X_min_u_n[::2] = matrices.Tmin_interval_after_nom
    matrices.X_min_u_n[1::2]= 0.2*data.E_bat_max

    matrices.lower_triang_AB = np.zeros((data.N*2,data.N*data.n_u))
    for i in range(data.N):
        for j in range(i+1):
             matrices.lower_triang_AB[2*i:2*(i+1),data.n_u*j:data.n_u*(j+1)] = np.linalg.matrix_power(model.A, i-j)@model.B

    matrices.lower_triang_AC = np.zeros((data.N*2,data.N))
    for i in range(data.N):
        for j in range(i+1):
             matrices.lower_triang_AC[2*i:2*(i+1),j:(j+1)] = np.linalg.matrix_power(model.A, i-j)@model.C
    
    matrices.lower_triang_AD = np.zeros((data.N*2,data.N))
    for i in range(data.N):
        for j in range(i+1):
             matrices.lower_triang_AD[2*i:2*(i+1),j:(j+1)] = np.linalg.matrix_power(model.A, i-j)@model.D

    matrices.lower_triang_AE = np.zeros((data.N*2,data.N))
    for i in range(data.N):
        for j in range(i+1):
             matrices.lower_triang_AE[2*i:2*(i+1),j:(j+1)] = np.linalg.matrix_power(model.A, i-j)@model.E

    matrices.matrix_A_x0 = np.zeros((data.N*2,2))
    for i in range(data.N):
        matrices.matrix_A_x0[2*i: 2*(i+1),:] = np.linalg.matrix_power(model.A, i+1)

    return matrices


def getMatrices_alt(data, model):
    matrices_alt = Structure()

    matrices_alt.u_min = np.zeros((data.n_u, 1))
    matrices_alt.u_max = np.array([1, data.P_PC * data.ts, data.P_PC * data.ts, np.inf]).reshape(-1, 1)

    matrices_alt.x0_max = np.array([data.Tmax, 0.8 * data.E_bat_max]).reshape(-1, 1)

    matrices_alt.lower_triang_AB = np.zeros((data.N * 2, data.N * data.n_u))
    for i in range(data.N):
        for j in range(i + 1):
            matrices_alt.lower_triang_AB[2 * i:2 * (i + 1), data.n_u * j:data.n_u * (j + 1)] = np.linalg.matrix_power(model.A, i - j) @ model.B

    matrices_alt.lower_triang_AB_zeros = np.zeros((data.n_x, data.n_u*(data.N_F + data.N_R)))
    matrices_alt.lower_triang_AB_full = np.zeros(((data.N_F + data.N_R) * data.n_x, data.n_u*(data.N_F + data.N_R)))
    for i in range(data.N_F + data.N_R):
        for j in range(i + 1):
            matrices_alt.lower_triang_AB_full[2 * i:2 * (i + 1), j*data.n_u:(j + 1)*data.n_u] = np.linalg.matrix_power(model.A, i - j) @ model.B
    matrices_alt.lower_triang_AB = np.vstack((matrices_alt.lower_triang_AB_zeros, matrices_alt.lower_triang_AB_full))

    matrices_alt.matrix_A_x0_FR = np.zeros(((data.N_F + data.N_R + 1) * data.n_x, 2))
    for i in range(data.N_F + data.N_R + 1):
        matrices_alt.matrix_A_x0_FR[2 * i: 2 * (i + 1), :] = np.linalg.matrix_power(model.A, i)

    return matrices_alt

def get_lower_triang(data, trans_mat_A, trans_mat,  kp):
    lower_triang_zeros = np.zeros((2, (data.N_F + data.N_R)))
    lower_triang_full = np.zeros(((data.N_F + data.N_R) * 2, (data.N_F + data.N_R)))
    for i in range(data.N_F + data.N_R):
        for j in range(i + 1):
           lower_triang_full[2 * i:2 * (i + 1), j:(j + 1)] = np.linalg.matrix_power(trans_mat_A, i+kp - j) @ trans_mat
    lower_triang = np.vstack((lower_triang_zeros, lower_triang_full))

    return lower_triang

def get_row_matrix(data, matA, mat, kp):
    A_row_kp = np.zeros((data.n_x, data.N))
    for k in range(0,kp):
        A_row_kp[:,k:k+1] = np.linalg.matrix_power(matA, kp - k-1)@mat

    return A_row_kp

def get_alt_transform(data, matA, mat, kp):
    alt_trans_mat = np.zeros(((data.N_F + data.N_R+1) * 2, (kp + data.N_F + data.N_R)))

    for i in range((data.N_F + data.N_R+1)):
        for j in range(kp+i):
            alt_trans_mat[2*i:2*(i+1), j:j+1] = np.linalg.matrix_power(matA, kp+i-1-j)@mat

    return alt_trans_mat








def get_Psi_alt_a_i_z(data,model, i,z):
    K_pi = get_Kpi(data)
    kp = int(K_pi[i,z])


    K_i = get_Ki(data).astype("i")
    activation_indices = K_i[i][z*data.act_len:(z+1)*data.act_len]

    env_temp = data.env_temp_K
    env_temp_act = []

    for k in activation_indices:
        env_temp_act.append(env_temp[k])


    env_temp_act = np.array(env_temp_act).reshape(-1,1)


    Q = data.water_demand
    Q_act = []

    for k in activation_indices:
        Q_act.append(Q[int(k)])

    Q_act = np.array(Q_act).reshape(-1,1)


    TQ = data.mul_TQ
    TQ_act = []

    for k in activation_indices:
        TQ_act.append(TQ[int(k)])

    TQ_act = np.array(TQ_act).reshape(-1,1)

    env_activation = np.vstack((env_temp[0:kp].reshape(-1,1), env_temp_act))
    Q_activation = np.vstack((Q[0:kp].reshape(-1,1), Q_act))
    TQ_activation = np.vstack((TQ[0:kp].reshape(-1,1), TQ_act))


    env_trans = get_alt_transform(data, model.A, model.C, kp)
    TQ_trans = get_alt_transform(data, model.A, model.D, kp)
    Q_trans = get_alt_transform(data, model.A, model.E, kp)
    


    Psi_a_i_z_x = env_trans @ env_activation + TQ_trans @ TQ_activation + Q_trans @ Q_activation

    return Psi_a_i_z_x

def get_Psi_alt_i(data,model, i):
    Psi_a_i = np.zeros((data.n_x*data.n_z*(data.N_F+data.N_R+1),1))
    for z in range(data.n_z):
        Psi_a_i[2*z*(data.N_F+data.N_R+1):2*(z+1)*(data.N_F+data.N_R+1),:] = get_Psi_alt_a_i_z(data, model, i, z)

    return Psi_a_i

def get_Psi_x_alt(data,model):
    Psi_a = np.zeros((data.n_x*data.n_a*data.n_z*(data.N_F+data.N_R+1),1))
    for i in range(data.n_a):
        Psi_a[2*i*data.n_z*(data.N_F+data.N_R+1):2*(i+1)*data.n_z*(data.N_F+data.N_R+1)] = get_Psi_alt_i(data,model, i)

    return Psi_a

def get_Psi_x_alt_two_reservations(data,model):
    return np.vstack((get_Psi_x_alt(data,model), get_Psi_x_alt(data,model)))

def getPsix_nom(data, matrices):
    Psi = (matrices.lower_triang_AC@data.env_temp_K.reshape(-1,1) + 
            matrices.lower_triang_AD@data.mul_TQ.reshape(-1,1) +
            matrices.lower_triang_AE@data.water_demand.reshape(-1,1)
            )
    return Psi

def get_Xmin_u_a_i_z(data,i,z):
    X_min_u_a_i_z = np.zeros((2*(data.N_F+data.N_R+1),1))
    K_i = get_Ki(data).astype("i")
    activation_indices = K_i[i][z*data.act_len:(z+1)*data.act_len]

    set_temp = data.set_water_temp_K
    set_temp_act = []

    for k in activation_indices:
        set_temp_act.append(set_temp[int(k)])

    set_temp_act = np.array(set_temp_act).reshape(-1,1)


    Q = data.water_demand
    Q_act = []

    for k in activation_indices:
        Q_act.append(Q[int(k)])

    Q_act = np.array(Q_act).reshape(-1,1)

    T_min_u_i_z = ((Q_act)/data.Qmax*
                                (set_temp_act-data.cold_water_temp)+data.cold_water_temp).reshape(-1,1)
    
    T_min_u_i_z = np.append(T_min_u_i_z,T_min_u_i_z[-1]).reshape(-1,1)
    X_min_u_a_i_z[::2] = T_min_u_i_z
    X_min_u_a_i_z[1::2]= 0.2*data.E_bat_max


    return X_min_u_a_i_z

def get_Xmin_u_a_i(data,i):
    X_min_u_a_i = np.zeros((2*data.n_z*(data.N_F+data.N_R+1),1))
    for z in range(data.n_z):
         X_min_u_a_i[2*z*(data.N_F+data.N_R+1):2*(z+1)*(data.N_F+data.N_R+1),:] = get_Xmin_u_a_i_z(data,i,z)

    return X_min_u_a_i

def get_Xmin_u_a(data):
    X_min_u_a = np.zeros((data.n_x*data.n_a*data.n_z*(data.N_F+data.N_R+1),1))

    for i in range(data.n_a):
        X_min_u_a[2*i*data.n_z*(data.N_F+data.N_R+1):2*(i+1)*data.n_z*(data.N_F+data.N_R+1),:] = get_Xmin_u_a_i(data,i)

    return X_min_u_a

def get_Xmin_u_a_two_reservations(data):
    return np.vstack((get_Xmin_u_a(data), get_Xmin_u_a(data)))

def get_Xmin_l_a_i_z(data,i,z):
    Xu = get_Xmin_u_a_i_z(data,i,z)

    Xmin_l_a_i_z = np.vstack((Xu[:2,], Xu[:-2,]))

    return Xmin_l_a_i_z

def get_Xmin_l_a_i(data,i):
    X_min_l_a_i = np.zeros((2*data.n_z*(data.N_F+data.N_R+1),1))

    for z in range(data.n_z):
         X_min_l_a_i[2*z*(data.N_F+data.N_R+1):2*(z+1)*(data.N_F+data.N_R+1),:] = get_Xmin_l_a_i_z(data,i,z)

    return X_min_l_a_i

def get_Xmin_l_a(data):
    X_min_l_a = np.zeros((data.n_x*data.n_a*data.n_z*(data.N_F+data.N_R+1),1))

    for i in range(data.n_a):
        X_min_l_a[2*i*data.n_z*(data.N_F+data.N_R+1):2*(i+1)*data.n_z*(data.N_F+data.N_R+1),:] = get_Xmin_l_a_i(data,i)

    return X_min_l_a

def get_Xmin_l_a_two_reservations(data):
    return np.vstack((get_Xmin_l_a(data), get_Xmin_l_a(data)))


def Xmax_alt(data,matrices_alt):
    Xmax_alt = np.tile(matrices_alt.x0_max, (2*data.n_a*data.n_z*(data.N_F+data.N_R+1),1))

    return Xmax_alt

def getPsiPPC_nom(data):
    PsiPPC_nom = np.zeros((data.N,1))
    PsiPPC_nom = np.tile(data.P_PC*data.ts, (PsiPPC_nom.shape[0],1))

    return PsiPPC_nom

def getPsiPPC_alt(data):
    PsiPPC_alt = np.tile((data.P_PC*data.ts), (2*data.n_a*data.n_z*(data.N_F + data.N_R),1))

    return PsiPPC_alt


def getPsiSell(data):
    PsiSell = np.zeros((data.N,1))
    PsiSell = data.sell_prices*(-data.nc_load_energy)
    return PsiSell.reshape(-1,1)


def getPsiBuy(data):
    PsiBuy = np.zeros((data.N, 1))
    PsiBuy = data.da_prices * (- data.nc_load_energy)
    return PsiBuy.reshape(-1, 1)


def getPsiPP_nom(data):
    PP_nom = np.zeros((data.N, 1))
    PP_nom = (1/data.ts) * (- data.nc_load_energy)
    return PP_nom.reshape(-1, 1)


def get_psi_nom_a(data):
    psi_nom_a = np.tile(getPsiPP_nom(data),(data.n_a,1))
    K_i = get_Ki(data)

    for i in range(data.n_a):
        for ki in K_i[i]:
            psi_nom_a[data.N*i+int(ki)] = np.array([0])

    return psi_nom_a

def get_psi_nom_a_two_reservations(data):
    return np.vstack((get_psi_nom_a(data), get_psi_nom_a(data)))


def getPsiPP_alt_i_z(data,i,z):
    pv_profile = data.pv_energy
    nc_profile = data.nc_load_energy
    K_i = get_Ki(data).astype("i")
    activation_indices = K_i[i][z*data.act_len:(z+1)*data.act_len]

    nc_profile_Act = []

    for k in activation_indices:
        nc_profile_Act.append(nc_profile[k])

    nc_profile_Act = np.array(nc_profile_Act).reshape(-1,1)[data.N_F:]

    PsiPP_alt_i_z = 1/data.ts*(- nc_profile_Act)

    return PsiPP_alt_i_z

def getPsiPP_alt_i(data,i):
    PsiPP_alt_i = np.zeros((data.N_R*data.n_z,1))

    for z in range(data.n_z):
        PsiPP_alt_i[data.N_R*z:data.N_R*(z+1),:] = getPsiPP_alt_i_z(data,i,z)

    return PsiPP_alt_i

def getPsiPP_alt(data):
    PsiPP_alt = np.zeros((data.N_R*data.n_a*data.n_z,1))

    for i in range(data.n_a):
        PsiPP_alt[data.N_R*i*data.n_z:data.N_R*(i+1)*data.n_z,:] = getPsiPP_alt_i(data,i)

    return PsiPP_alt

def getPsiPP_alt_two_reservations(data):
    return np.vstack((getPsiPP_alt(data), getPsiPP_alt(data)))

def getPsiPV_nom(data):
    PV_nom = np.zeros((data.N, 1))
    PV_nom = data.pv_energy
    return PV_nom.reshape(-1, 1)

def getPsiPV_alt_i_z(data,i,z):
    pv_profile = data.pv_energy
    K_i = get_Ki(data).astype("i")
    activation_indices = K_i[i][z*data.act_len:(z+1)*data.act_len]
    pv_profile_Act = []
    for k in activation_indices:
        pv_profile_Act.append(pv_profile[k])

    pv_profile_Act = np.array(pv_profile_Act).reshape(-1,1)
    return pv_profile_Act

def getPsiPV_alt_i(data,i):
    PsiPV_alt_i = np.zeros(((data.N_F+data.N_R)*data.n_z,1))

    for z in range(data.n_z):
        PsiPV_alt_i[(data.N_F+data.N_R)*z:(data.N_F+data.N_R)*(z+1),:] = getPsiPV_alt_i_z(data,i,z)

    return PsiPV_alt_i

def getPsiPV_alt(data):
    PsiPV_alt = np.zeros(((data.N_F+data.N_R)*data.n_a*data.n_z,1))

    for i in range(data.n_a):
        PsiPV_alt[(data.N_F+data.N_R)*i*data.n_z:(data.N_F+data.N_R)*(i+1)*data.n_z,:] = getPsiPV_alt_i(data,i)

    return PsiPV_alt

def getPsiPV_alt_two_reservations(data):
    return np.vstack((getPsiPV_alt(data), getPsiPV_alt(data)))

def getTheta_a_plus(data, matrices_alt, model):
    Theta_a = np.hstack((
                    getTheta_a_x0(data,model),
                    getTheta_a_Un(data, matrices_alt, model),
                    getTheta_a_Ua(data, matrices_alt),
                    np.zeros(((data.n_x*data.n_a*data.n_z*(data.N_F+data.N_R+1)), (data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))),
                    np.zeros(((data.n_x*data.n_a*data.n_z*(data.N_F+data.N_R+1)), (2*data.n_a*data.n_z*data.N_R + data.N + 1 + 2*data.n_a + 5 )))))
    return Theta_a

def getTheta_a_minus(data, matrices_alt, model):
    Theta_a = np.hstack((
                    getTheta_a_x0(data,model),
                    getTheta_a_Un(data, matrices_alt, model),
                    np.zeros(((data.n_x*data.n_a*data.n_z*(data.N_F+data.N_R+1)), (data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))),
                    getTheta_a_Ua(data, matrices_alt),
                    np.zeros(((data.n_x*data.n_a*data.n_z*(data.N_F+data.N_R+1)), (2*data.n_a*data.n_z*data.N_R + data.N + 1 + 2*data.n_a + 5)))))
    return Theta_a


def getTheta_a(data, matrices_alt, model):
    Theta_a = np.vstack((
                   getTheta_a_plus(data, matrices_alt, model),
                   getTheta_a_minus(data, matrices_alt, model)
    ))
    return Theta_a

# def getTheta_a_x0(data):
#     Theta_a_x0 = np.zeros((data.n_x*data.n_a*data.n_z*(data.N_F+data.N_R+1), data.n_x))
#     model = getModel(data)
#     for i in range(data.n_a):
#         for j in range(data.n_z*(data.N_F+data.N_R)): 
#             k = int(data.K_i[i][j])
#             Theta_a_x0[i*data.n_z*(data.N_F+data.N_R)+2*j: i*data.n_z*(data.N_F+data.N_R)+2*(j+1),:] = np.linalg.matrix_power(model.A, k+1)
#     return Theta_a_x0

def getTheta_a_x0_kp(data, kp, model):
    matrix_A_kp_FR = np.zeros(((data.N_F + data.N_R + 1) * data.n_x, 2))
    for i in range(data.N_F + data.N_R + 1):
        matrix_A_kp_FR[2 * i: 2 * (i + 1), :] = np.linalg.matrix_power(model.A, i+kp)
    
    return  matrix_A_kp_FR

def getTheta_a_x0(data, model):
    Theta_a_x0 = np.zeros((data.n_x*data.n_a*data.n_z*(data.N_F+data.N_R+1), data.n_x))
    K_pi = get_Kpi(data).ravel().astype("i")

    i = 0
    for kp in K_pi:
        Theta_a_x0[i*((data.N_F + data.N_R + 1) * data.n_x):(i+1)*((data.N_F + data.N_R + 1) * data.n_x),:] = getTheta_a_x0_kp(data, kp, model)
        i+=1

    return Theta_a_x0


def getTheta_a_Un_kp(data, matrices_alt, model,kp):
    A_row_kp_B = np.zeros((data.n_x, data.N*data.n_u))
    for k in range(1,kp+1):
        A_row_kp_B[:,data.n_u*(k-1):data.n_u*k] = np.linalg.matrix_power(model.A, kp - k)@model.B

    Theta_a_Un_kp =  matrices_alt.matrix_A_x0_FR @ A_row_kp_B

    return Theta_a_Un_kp


def getTheta_a_Un(data, matrices_alt, model): #TODO
    Theta_a_Un = np.zeros((data.n_x*data.n_a*data.n_z*(data.N_F+data.N_R+1),data.N*data.n_u))

    K_pi = get_Kpi(data).ravel().astype("i")
    i = 0
    for kp in K_pi:
        Theta_a_Un[i*data.n_x*(data.N_F+data.N_R+1):(i+1)*data.n_x*(data.N_F+data.N_R+1),:] = getTheta_a_Un_kp(data, matrices_alt, model,kp)
        i+=1
    return  Theta_a_Un


def getTheta_a_Ua_i(data, matrices_alt): #TODO
    Theta_a_Ua_i = np.zeros((data.n_x*data.n_z*(data.N_F+data.N_R+1), data.n_u*data.n_z*(data.N_F+data.N_R)))
    for z in range(data.n_z):
           Theta_a_Ua_i[data.n_x*z*(data.N_F+data.N_R+1):data.n_x*(z+1)*(data.N_F+data.N_R+1),data.n_u*z*(data.N_F+data.N_R):data.n_u*(z+1)*(data.N_F+data.N_R)] = matrices_alt.lower_triang_AB

    return Theta_a_Ua_i

def getTheta_a_Ua(data, matrices_alt): #TODO
    Theta_a_Ua_i = np.zeros((data.n_x*data.n_a*data.n_z*(data.N_F+data.N_R+1), data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))
    for i in range(data.n_a):
           row_beg = data.n_x*i*data.n_z*(data.N_F+data.N_R+1)
           row_end = data.n_x*(i+1)*data.n_z*(data.N_F+data.N_R+1)
           col_beg = data.n_u*i*data.n_z*(data.N_F+data.N_R)
           col_end = data.n_u*(i+1)*data.n_z*(data.N_F+data.N_R)
           Theta_a_Ua_i[row_beg:row_end, col_beg:col_end] = getTheta_a_Ua_i(data, matrices_alt)

    return Theta_a_Ua_i

def getTheta_n(data, matrices):
    Theta_n = np.hstack((matrices.matrix_A_x0,
                        matrices.lower_triang_AB,
                        np.zeros(((data.N*data.n_x), (2*data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R) + 2*data.n_a*data.n_z*data.N_R + data.N + 1 + 2*data.n_a + 5 )))))
    return Theta_n

def getTheta_PC_n(data):
    Theta_PC_n = np.hstack((
                        np.zeros(((data.N), (data.n_x))),                        
                        getTheta_PC_Un(data),
                        np.zeros(((data.N), (2*data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R) + 2*data.n_a*data.n_z*data.N_R + data.N + 1 + 2*data.n_a + 5 )))))
    return Theta_PC_n

def getTheta_PC_Un(data):
    Theta_PC_Un = np.zeros((data.N, data.N*data.n_u))
    for i in range(data.N):
        Theta_PC_Un[i,data.n_u*i:data.n_u*(i+1)] = np.array([0,1,1,0])
    return Theta_PC_Un

def getTheta_PC_Ua(data):
    Theta_PC_Ua = np.zeros((data.n_a*data.n_z*(data.N_F+data.N_R), data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))
    for i in range(data.n_a*data.n_z*(data.N_F+data.N_R)):
        Theta_PC_Ua[i,data.n_u*i:data.n_u*(i+1)] = np.array([0,1,1,0])
    return Theta_PC_Ua

def getTheta_PC_a_plus(data):
    Theta_PC_a = np.hstack((
                        np.zeros((data.n_a*data.n_z*(data.N_F+data.N_R), (data.n_x + data.N*data.n_u))),                        
                        getTheta_PC_Ua(data),
                        np.zeros(((data.n_a*data.n_z*(data.N_F+data.N_R)), data.n_a*data.n_z*data.n_u*(data.N_F+data.N_R))),
                        np.zeros(((data.n_a*data.n_z*(data.N_F+data.N_R)), 2*data.n_a*data.n_z*data.N_R + data.N + 1 + 2*data.n_a + 5))))
    return Theta_PC_a

def getTheta_PC_a_minus(data):
    Theta_PC_a = np.hstack((
                        np.zeros((data.n_a*data.n_z*(data.N_F+data.N_R), (data.n_x + data.N*data.n_u))),   
                        np.zeros(((data.n_a*data.n_z*(data.N_F+data.N_R)), data.n_a*data.n_z*data.n_u*(data.N_F+data.N_R))),                     
                        getTheta_PC_Ua(data),
                        np.zeros(((data.n_a*data.n_z*(data.N_F+data.N_R)), 2*data.n_a*data.n_z*data.N_R + data.N + 1 + 2*data.n_a + 5))))
    return Theta_PC_a

def getTheta_PC_a(data):
    return np.vstack((getTheta_PC_a_plus(data), getTheta_PC_a_minus(data)))


def getTheta_sell(data): 
    Theta_sell = np.hstack((
                        np.zeros(((data.N), (data.n_x))),                        
                        getTheta_sell_Un(data),
                        np.zeros(((data.N), (2*data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R) + 2*data.n_a*data.n_z*data.N_R))),
                        -np.eye(data.N),
                        np.zeros(((data.N), 1 + 2*data.n_a + 5)),
                        ))
    return Theta_sell

def getTheta_sell_Un(data): 
    Theta_sell_Un = np.zeros((data.N, data.N*data.n_u))
    for i in range(data.N):
        Theta_sell_Un[i,data.n_u*i:data.n_u*(i+1)] = data.sell_prices[i]*np.array([data.P_heater*data.ts,1,-1, -1])     
    return Theta_sell_Un

def getTheta_buy(data): 
    Thetabuy = np.hstack((
                        np.zeros(((data.N), (data.n_x))),                        
                        getTheta_buy_Un(data),
                        np.zeros(((data.N), (2*data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R) + 2*data.n_a*data.n_z*data.N_R))),
                        -np.eye(data.N),
                        np.zeros(((data.N), 1 + 2*data.n_a + 5)),
                        ))
    return Thetabuy

def getTheta_buy_Un(data):
    Theta_buy_Un = np.zeros((data.N, data.N*data.n_u))
    for i in range(data.N):
        Theta_buy_Un[i,data.n_u*i:data.n_u*(i+1)] = data.da_prices[i]*np.array([data.P_heater*data.ts,1,-1, -1])     
    return Theta_buy_Un

def getTheta_pp_nom_a(data):
    theta_pp_nom_a = np.tile(getTheta_pp_n_Un(data),(data.n_a,1))
    K_i = get_Ki(data)

    for i in range(data.n_a):
        for k_i in K_i[i]:
            theta_pp_nom_a[i*data.N+int(k_i), data.n_u*int(k_i):data.n_u*(int(k_i)+1)] = np.array([0,0,0,0])

    return theta_pp_nom_a

def get_Theta_pp_epp(data):
    theta_pp_nom_a_eps = np.zeros((data.n_a*data.N, data.n_a))
    K_i = get_Ki(data)
    for i in range(data.n_a):
        for j in range(data.N):
            if j not in K_i[i]:
                theta_pp_nom_a_eps[i*data.N+j, i] = -1
    return theta_pp_nom_a_eps

def get_theta_nom_a_plus(data):
    theta_nom_a = np.hstack((np.zeros((data.n_a*data.N,2)),
                      getTheta_pp_nom_a(data),
                      np.zeros((data.n_a*data.N, data.N+2*data.n_u*(data.N_F+data.N_R)*data.n_a*data.n_z + 2*data.N_R*data.n_a*data.n_z)),
                      np.zeros((data.n_a*data.N,1)),
                      get_Theta_pp_epp(data),
                      np.zeros((data.n_a*data.N,data.n_a)),
                      np.zeros((data.n_a*data.N,5))
                      ))
    return theta_nom_a

def get_theta_nom_a_minus(data):
    theta_nom_a = np.hstack((np.zeros((data.n_a*data.N,2)),
                      getTheta_pp_nom_a(data),
                      np.zeros((data.n_a*data.N, data.N+2*data.n_u*(data.N_F+data.N_R)*data.n_a*data.n_z + 2*data.N_R*data.n_a*data.n_z)),
                      np.zeros((data.n_a*data.N,1)),
                      np.zeros((data.n_a*data.N,data.n_a)),
                      get_Theta_pp_epp(data),
                      np.zeros((data.n_a*data.N,5))
                      ))
    return theta_nom_a

def get_theta_nom_a(data):
    return np.vstack((get_theta_nom_a_plus(data), get_theta_nom_a_minus(data)))

def getTheta_pp_n(data):
    Theta_pp_n = np.hstack((
                        np.zeros(((data.N), (data.n_x))),                        
                        getTheta_pp_n_Un(data),
                        np.zeros(((data.N), (2*data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R) + 2*data.n_a*data.n_z*data.N_R + data.N))),
                        getTheta_pp_n_eps(data),
                        np.zeros(((data.N), 5))
                        ))
    return Theta_pp_n

def getTheta_pp_n_Un(data):
    Theta_pp_n_Un = np.zeros((data.N, data.N*data.n_u))
    for i in range(data.N):
        Theta_pp_n_Un[i, data.n_u*i:data.n_u*(i+1)] = np.array([data.P_heater, 1/data.ts, -1/data.ts, -1/data.ts])
    return Theta_pp_n_Un

def getTheta_pp_n_eps(data):
    Theta_pp_n_eps = np.zeros((data.N, 1 + 2*data.n_a))
    Theta_pp_n_eps[:, 0] = -1
    return Theta_pp_n_eps

######################################################################################################

def getTheta_pp_a_plus(data):
    Theta_pp_a = np.hstack((
                        np.zeros(((data.N_R*data.n_a*data.n_z), (data.n_x))),                        
                        getTheta_pp_a_Ua(data),
                        np.zeros(((data.N_R*data.n_a*data.n_z), (data.n_u*data.N))),
                        np.zeros(((data.N_R*data.n_a*data.n_z), (data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))),
                        np.zeros(((data.N_R*data.n_a*data.n_z), (2*data.n_a*data.n_z*data.N_R + data.N))),
                        np.zeros(((data.N_R*data.n_a*data.n_z), 1)),
                        getTheta_pp_a_eps(data),
                        np.zeros(((data.N_R*data.n_a*data.n_z), data.n_a)),
                        np.zeros(((data.N_R*data.n_a*data.n_z), 5)),
                        ))
    return Theta_pp_a

def getTheta_pp_a_minus(data):
    Theta_pp_a = np.hstack((
                        np.zeros(((data.N_R*data.n_a*data.n_z), (data.n_x))),                        
                        np.zeros(((data.N_R*data.n_a*data.n_z), (data.n_u*data.N))),
                        np.zeros(((data.N_R*data.n_a*data.n_z), (data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))),
                        getTheta_pp_a_Ua(data),
                        np.zeros(((data.N_R*data.n_a*data.n_z), (2*data.n_a*data.n_z*data.N_R + data.N))),
                        np.zeros(((data.N_R*data.n_a*data.n_z), 1)),
                        np.zeros(((data.N_R*data.n_a*data.n_z), data.n_a)),
                        getTheta_pp_a_eps(data),
                        np.zeros(((data.N_R*data.n_a*data.n_z), 5)),
                        ))
    return Theta_pp_a

def getTheta_pp_a(data):
    return np.vstack((getTheta_pp_a_plus(data), getTheta_pp_a_minus(data)))


def getTheta_pp_a_Ua(data):
    Theta_pp_a_Ua = np.zeros((data.N_R*data.n_a*data.n_z, data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a*data.n_z):
        for j in range(data.N_R):
            j = int(j)
            Theta_pp_a_Ua[i*data.N_R+j,  i*data.n_u*(data.N_F+data.N_R)+data.N_F*data.n_u+data.n_u*j:i*data.n_u*(data.N_F+data.N_R)+data.N_F*data.n_u+data.n_u*(j+1)] = np.array([data.P_heater, 1/data.ts, -1/data.ts, -1/data.ts])

    
    return Theta_pp_a_Ua

def getTheta_pp_a_eps(data):
    Theta_pp_a_eps = np.zeros((data.N_R*data.n_a*data.n_z, data.n_a))
    for i in range(data.n_a):
        Theta_pp_a_eps[i*data.N_R*data.n_z:(i+1)*data.N_R*data.n_z, i] = np.tile(-1, (data.N_R*data.n_z))
    return Theta_pp_a_eps

######################################################################################################

def getTheta_PV_n(data):
    Theta_PV_n = np.hstack((
                        np.zeros(((data.N), (data.n_x))),                        
                        getTheta_PV_n_Un(data),
                        np.zeros(((data.N), (2*data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R) + 2*data.n_a*data.n_z*data.N_R + data.N))),
                        np.zeros((data.N, 1 + 2*data.n_a)),
                        np.zeros(((data.N), 5)),
                        ))
    return Theta_PV_n

def getTheta_PV_n_Un(data):
    Theta_PV_n_Un = np.zeros((data.N, data.N*data.n_u))
    for i in range(data.N):
        Theta_PV_n_Un[i, data.n_u*i:data.n_u*(i+1)] = np.array([0,0,0,1])
    return Theta_PV_n_Un

def getTheta_PV_a_plus(data):
    Theta_pp_a = np.hstack((
                        np.zeros((((data.N_F+data.N_R)*data.n_a*data.n_z), (data.n_x))),                        
                        np.zeros((((data.N_F+data.N_R)*data.n_a*data.n_z), (data.n_u*data.N))),
                        getTheta_PV_a_Ua(data),
                        np.zeros((((data.N_F+data.N_R)*data.n_a*data.n_z), (data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))),
                        np.zeros((((data.N_F+data.N_R)*data.n_a*data.n_z), (2*data.n_a*data.n_z*data.N_R + data.N))),
                        np.zeros(((data.N_F+data.N_R)*data.n_a*data.n_z, 1 + 2*data.n_a)),
                        np.zeros((((data.N_F+data.N_R)*data.n_a*data.n_z), 5)),
                        ))
    return Theta_pp_a


def getTheta_PV_a_minus(data):
    Theta_pp_a = np.hstack((
                        np.zeros((((data.N_F+data.N_R)*data.n_a*data.n_z), (data.n_x))),                        
                        np.zeros((((data.N_F+data.N_R)*data.n_a*data.n_z), (data.n_u*data.N))),
                        np.zeros((((data.N_F+data.N_R)*data.n_a*data.n_z), (data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))),
                        getTheta_PV_a_Ua(data),
                        np.zeros((((data.N_F+data.N_R)*data.n_a*data.n_z), (2*data.n_a*data.n_z*data.N_R + data.N))),
                        np.zeros(((data.N_F+data.N_R)*data.n_a*data.n_z, 1 + 2*data.n_a)),
                        np.zeros((((data.N_F+data.N_R)*data.n_a*data.n_z), 5)),
                        ))
    return Theta_pp_a

def getTheta_PV_a(data):
    return np.vstack((getTheta_PV_a_plus(data), getTheta_PV_a_minus(data)))


def getTheta_PV_a_Ua(data):
    Theta_PV_a_Ua = np.zeros(((data.N_F+data.N_R)*data.n_a*data.n_z, data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a*data.n_z):
        for j in range(data.N_F+data.N_R):
            j = int(j)
            Theta_PV_a_Ua[i*(data.N_F+data.N_R)+j,  i*data.n_u*(data.N_F+data.N_R)+data.n_u*j:i*data.n_u*(data.N_F+data.N_R)+data.n_u*(j+1)] = np.array([0,0,0,1])
    return Theta_PV_a_Ua

def getTheta_abs_poz_plus(data): 
    Theta_abs_poz = np.hstack((
                        np.zeros(((data.n_a*data.n_z*data.N_R), (data.n_x))),                        
                        -getTheta_abs_Un(data),
                        getTheta_abs_Ua(data),
                        np.zeros(((data.n_a*data.n_z*data.N_R), (data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))),
                        -np.eye((data.n_a*data.n_z*data.N_R)),
                        np.zeros(((data.n_a*data.n_z*data.N_R), (data.n_a*data.n_z*data.N_R))),
                        np.zeros(((data.n_a*data.n_z*data.N_R), data.N + 1 + 2*data.n_a + 5))
                        ))
    return Theta_abs_poz

def getTheta_abs_poz_minus(data): 
    Theta_abs_poz = np.hstack((
                        np.zeros(((data.n_a*data.n_z*data.N_R), (data.n_x))),                        
                        -getTheta_abs_Un(data),
                        np.zeros(((data.n_a*data.n_z*data.N_R), (data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))),
                        getTheta_abs_Ua(data),
                        np.zeros(((data.n_a*data.n_z*data.N_R), (data.n_a*data.n_z*data.N_R))),
                        -np.eye((data.n_a*data.n_z*data.N_R)),
                        np.zeros(((data.n_a*data.n_z*data.N_R), data.N + 1 + 2*data.n_a + 5))
                        ))
    return Theta_abs_poz

def getTheta_abs_neg_plus(data):
    Theta_abs_neg = np.hstack((
                        np.zeros(((data.n_a*data.n_z*data.N_R), (data.n_x))),                        
                        getTheta_abs_Un(data),
                        -getTheta_abs_Ua(data),
                        np.zeros(((data.n_a*data.n_z*data.N_R), (data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))),
                        -np.eye((data.n_a*data.n_z*data.N_R)),
                        np.zeros(((data.n_a*data.n_z*data.N_R), (data.n_a*data.n_z*data.N_R))),
                        np.zeros(((data.n_a*data.n_z*data.N_R), data.N + 1 + 2*data.n_a + 5))
                        ))
    return Theta_abs_neg

def getTheta_abs_neg_minus(data):
    Theta_abs_neg = np.hstack((
                        np.zeros(((data.n_a*data.n_z*data.N_R), (data.n_x))),                        
                        getTheta_abs_Un(data),
                        np.zeros(((data.n_a*data.n_z*data.N_R), (data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))),
                        -getTheta_abs_Ua(data),
                        np.zeros(((data.n_a*data.n_z*data.N_R), (data.n_a*data.n_z*data.N_R))),
                        -np.eye((data.n_a*data.n_z*data.N_R)),
                        np.zeros(((data.n_a*data.n_z*data.N_R), data.N + 1 + 2*data.n_a + 5))
                        ))
    return Theta_abs_neg

def getTheta_abs_poz(data):
    return np.vstack((getTheta_abs_poz_plus(data), getTheta_abs_poz_minus(data)))

def getTheta_abs_neg(data):
    return np.vstack((getTheta_abs_neg_plus(data), getTheta_abs_neg_minus(data)))


def getTheta_abs_Un(data): 
    Theta_abs_Un = np.zeros((data.n_a*data.n_z*data.N_R, data.N*data.n_u))
    for i in range(data.n_a):
        for j in range(data.n_z*data.N_R):
            k = int(data.K_ri[i][j])
            j = int(j)
            Theta_abs_Un[i*data.n_z*data.N_R+j, data.n_u*k:data.n_u*(k+1)] = np.array([data.P_heater*data.ts, 1, -1, -1])
    return Theta_abs_Un

def getTheta_abs_Ua(data): 
    Theta_abs_Ua = np.zeros((data.n_a*data.n_z*data.N_R, data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))
    for i in range(data.n_a*data.n_z):
        for j in range(data.N_R):
            j = int(j)
            Theta_abs_Ua[i*data.N_R+j,  i*data.n_u*(data.N_F+data.N_R)+data.N_F*data.n_u+data.n_u*j:i*data.n_u*(data.N_F+data.N_R)+data.N_F*data.n_u+data.n_u*(j+1)] = np.array([data.P_heater*data.ts, 1, -1, -1])
    return Theta_abs_Ua


def getTheta_delta_plus(data):
    Theta_delta = np.hstack((
                        np.zeros(((data.n_a*data.n_z*data.N_F), (data.n_x))),                        
                        getTheta_delta_Un(data),
                        getTheta_delta_Ua_plus(data),
                        np.zeros(((data.n_a*data.n_z*data.N_F), data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R))),
                        np.zeros(((data.n_a*data.n_z*data.N_F), 2*data.n_a*data.n_z*data.N_R + data.N + 1 + 2*data.n_a)),
                        np.tile(data.ts,((data.n_a*data.n_z*data.N_F), 1)),
                        np.zeros((data.n_a*data.n_z*data.N_F, 1 )),
                        np.zeros(((data.n_a*data.n_z*data.N_F), 3 )),
                        ))
    return Theta_delta

def getTheta_delta_minus(data):
    Theta_delta = np.hstack((
                        np.zeros(((data.n_a*data.n_z*data.N_F), (data.n_x))),                        
                        -getTheta_delta_Un(data),
                        np.zeros(((data.n_a*data.n_z*data.N_F), data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R))),
                        getTheta_delta_Ua_minus(data),
                        np.zeros(((data.n_a*data.n_z*data.N_F), 2*data.n_a*data.n_z*data.N_R + data.N + 1 + 2*data.n_a)),
                        np.zeros((data.n_a*data.n_z*data.N_F, 1 )),
                        np.tile(data.ts,((data.n_a*data.n_z*data.N_F), 1)),
                        np.zeros(((data.n_a*data.n_z*data.N_F), 3)),
                        ))
    return Theta_delta

def getTheta_delta_Un(data):
    Theta_delta_Un = np.zeros((data.n_a*data.n_z*data.N_F, data.N*data.n_u))
    for i in range(data.n_a):
        for j in range(data.n_z*data.N_F):
            j = int(j)
            k = int(data.K_fi[i][j])
            Theta_delta_Un[i*data.n_z*data.N_F+j, data.n_u*k:data.n_u*(k+1)] = np.array([-data.P_heater*data.ts, -1, 1, 1]) 
    return Theta_delta_Un

def getTheta_delta_Ua_plus(data):
    Theta_delta_Ua = np.zeros((data.n_a*data.n_z*data.N_F, data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))
    for i in range(0,data.n_a*data.n_z):
        for j in range(data.N_F):
            Theta_delta_Ua[i*data.N_F+j, data.n_u*i*(data.N_F+data.N_R)+data.n_u*j:data.n_u*i*(data.N_F+data.N_R)+data.n_u*(j+1)] = np.array([data.P_heater*data.ts, 1, -1, -1])
    return Theta_delta_Ua

def getTheta_delta_Ua_minus(data):
    Theta_delta_Ua = np.zeros((data.n_a*data.n_z*data.N_F, data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))
    for i in range(0,data.n_a*data.n_z):
        for j in range(data.N_F):
            Theta_delta_Ua[i*data.N_F+j, data.n_u*i*(data.N_F+data.N_R)+data.n_u*j:data.n_u*i*(data.N_F+data.N_R)+data.n_u*(j+1)] = np.array([-data.P_heater*data.ts, -1, 1, 1])
    return Theta_delta_Ua

def getTheta_max_plus(data): 
    Theta_max = np.hstack((
                        np.zeros(((data.n_a), (data.n_x + data.N*data.n_u + 2*data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))),                        
                        getTheta_max_eps_abs(data),     #intraday eps
                        np.zeros((data.n_a, data.N_R*data.n_a*data.n_z)),
                        np.zeros(((data.n_a), data.N)), #day ahead prices
                        np.tile(-data.cpp,((data.n_a), 1)), #nom pp eps
                        getTheta_max_eps_pp(data),          #alt pp eps
                        np.zeros(((data.n_a), data.n_a)),
                        np.zeros(((data.n_a), 2 )),         #Pr+ and Pr-
                        -np.ones(((data.n_a), 1)),          #eps_max_+
                        np.zeros(((data.n_a), 1 )),          #eps_max_-
                        np.zeros(((data.n_a), 1 ))          #eps_max_+-
                        ))
    return Theta_max

def getTheta_max_minus(data): 
    Theta_max = np.hstack((
                        np.zeros(((data.n_a), (data.n_x + data.N*data.n_u + 2*data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))),  
                        np.zeros((data.n_a, data.N_R*data.n_a*data.n_z)),                      
                        getTheta_max_eps_abs(data),     #intraday eps
                        np.zeros(((data.n_a), data.N)), #day ahead prices
                        np.tile(-data.cpp,((data.n_a), 1)), #nom pp eps
                        np.zeros(((data.n_a), data.n_a)),
                        getTheta_max_eps_pp(data),          #alt pp eps
                        np.zeros(((data.n_a), 2 )),         #Pr+ and Pr-
                        np.zeros(((data.n_a), 1)),          #eps_max_+
                        -np.ones(((data.n_a), 1 )),          #eps_max_-
                        np.zeros(((data.n_a), 1))          #eps_max_+-
                        ))
    return Theta_max

def getTheta_max(data):
    return np.vstack((getTheta_max_plus(data), getTheta_max_minus(data)))

def getTheta_max_eps_abs(data): 
    Theta_max_eps_abs = np.zeros((data.n_a, data.n_a*data.n_z*data.N_R))
    for i in range(data.n_a):
        Theta_max_eps_abs[i, i*data.n_z*data.N_R:(i+1)*data.n_z*data.N_R] = np.tile(1, (data.N_R*data.n_z))*data.cid

    return Theta_max_eps_abs

def getTheta_max_eps_pp(data): 
    return np.eye(data.n_a)*data.cpp

def getTheta_max_plus_minus(data):
    Theta_max_plus_minus = np.zeros((2, data.len_chi))
    Theta_max_plus_minus[0,-3:] = [1,0,-1]
    Theta_max_plus_minus[1,-3:] = [0,1,-1]

    return Theta_max_plus_minus


def getLb(data,matrices, matrices_alt):
    lb = np.zeros((data.len_chi,1))
    U_min_nom = np.tile(matrices.u_min, (data.N ,1))
    U_min_alt = np.tile(matrices_alt.u_min, (data.n_a*data.n_z*(data.N_F+data.N_R),1))
    Eps_abs_min = np.zeros((data.n_a*data.n_z*data.N_R,1))
    Eps_da_min = np.tile(-np.inf,(data.N ,1))
    Epp_nom_min = np.zeros((1,1))
    Epp_alt_min = np.zeros((data.n_a,1))

    
    Pr_min_plus = 0
    Pr_min_minus = 0
    E_max_min = 0
    lb = np.vstack((matrices.x0_min,
                     U_min_nom, 
                     U_min_alt,
                     U_min_alt,
                     Eps_abs_min,
                     Eps_abs_min,
                     Eps_da_min,
                     Epp_nom_min,
                     Epp_alt_min,
                     Epp_alt_min,
                     Pr_min_plus,
                     Pr_min_minus,
                     E_max_min,
                     E_max_min,
                     E_max_min
                    ))
    return lb

def getUb(data,matrices, matrices_alt):
    ub = np.zeros((data.len_chi,1))
    U_max_nom = np.tile(matrices.u_max, (data.N ,1))
    U_max_alt = np.tile(matrices_alt.u_max, (data.n_a*data.n_z*(data.N_F+data.N_R),1))
    Eps_abs_max = np.tile(np.inf, (data.n_a*data.n_z*data.N_R,1))
    Eps_da_max = np.tile(np.inf,(data.len_eps_da ,1))
    Epp_nom_max = np.inf
    Epp_alt_max = np.tile(np.inf,(data.n_a,1))

    Pr_max_plus = np.inf
    Pr_max_minus = np.inf
    if (data.Pr_scen == "Positive"):
        Pr_max_minus = 0
    if (data.Pr_scen == "Negative"):
        Pr_max_plus = 0
    

    E_max_max = np.inf
    ub = np.vstack((matrices.x0_max,
                     U_max_nom, 
                     U_max_alt,
                     U_max_alt,
                     Eps_abs_max,
                     Eps_abs_max,
                     Eps_da_max,
                     Epp_nom_max,
                     Epp_alt_max,
                     Epp_alt_max,
                     Pr_max_plus,
                     Pr_max_minus,
                     E_max_max,
                     E_max_max,
                     E_max_max
                    ))
    return ub

def getF(data):
    f = np.r_[np.zeros((data.n_x)),np.zeros((data.n_u*data.N)),np.zeros((2*data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R))), np.zeros((2*data.N_R*data.n_a*data.n_z)),
            np.ones((data.N)), data.cpp, np.zeros(2*data.n_a),
            -data.alfa_plus*data.cr_plus,-data.alfa_minus*data.cr_minus, data.alfa_plus-data.alfa_plus*data.alfa_minus, data.alfa_minus-data.alfa_plus*data.alfa_minus, 
            data.alfa_plus*data.alfa_minus]
    return f.reshape(-1,1)

def getPsiTmix_nom(data):
    return np.tile([data.set_water_temp_K[0], 0], data.N).reshape(-1,1)

def getPsiTmix_alt(data):
    return np.tile([data.set_water_temp_K[0], 0], 2*data.n_a*data.n_z*(data.N_F+data.N_R+1)).reshape(-1,1)

def getAineq(data,matrices, model, matrices_alt):
    Theta_a = getTheta_a(data, matrices_alt, model)
    Theta_n = getTheta_n(data, matrices)
    Aineq = np.vstack((
        Theta_a,
        -Theta_a,
        -Theta_a,
        Theta_n,
        -Theta_n,
        -Theta_n,
        -Theta_n, #Thot>=Tmix nominalni
        -Theta_a, #Thot>=Tmix alternativni
        getTheta_PC_n(data),
        getTheta_PC_a(data),
        getTheta_sell(data),
        getTheta_buy(data),
        getTheta_pp_n(data),
        get_theta_nom_a(data),
        getTheta_pp_a(data),
        getTheta_PV_n(data),
        getTheta_PV_a(data),
        getTheta_abs_poz(data),
        getTheta_abs_neg(data),
        getTheta_delta_plus(data),
        getTheta_delta_minus(data),
        getTheta_max(data),
        getTheta_max_plus_minus(data)
    ))
    return csr_matrix(Aineq)


def getbineq(data,matrices, matrices_alt, model):
    bineq = np.vstack((
        Xmax_alt(data,matrices_alt) - get_Psi_x_alt_two_reservations(data,model),
        get_Psi_x_alt_two_reservations(data,model)- get_Xmin_l_a_two_reservations(data),
        get_Psi_x_alt_two_reservations(data,model)- get_Xmin_u_a_two_reservations(data),
        matrices.X_max_n - getPsix_nom(data,matrices),
        getPsix_nom(data,matrices) - matrices.X_min_l_n,
        getPsix_nom(data,matrices) - matrices.X_min_u_n,
        getPsix_nom(data,matrices) - getPsiTmix_nom(data), #ogranicenje Thot>=Tmix nominalni
        get_Psi_x_alt_two_reservations(data,model) - getPsiTmix_alt(data), #ogranicenje Thot>=Tmix
        getPsiPPC_nom(data),
        getPsiPPC_alt(data),
        getPsiSell(data),
        getPsiBuy(data),
        getPsiPP_nom(data),
        get_psi_nom_a_two_reservations(data),
        getPsiPP_alt_two_reservations(data),
        getPsiPV_nom(data),
        getPsiPV_alt_two_reservations(data),
        np.zeros((2*data.n_a*data.n_z*data.N_R,1)),
        np.zeros((2*data.n_a*data.n_z*data.N_R,1)),
        np.zeros((data.n_a*data.n_z*data.N_F,1)),
        np.zeros((data.n_a*data.n_z*data.N_F,1)),
        np.zeros((2*data.n_a,1)),
        np.zeros((2,1))
    ))
    return bineq


def getAeq_Un(data,matrices,model):
    Aeq = np.zeros((2,data.len_chi))
    Aeq_x0 = np.linalg.matrix_power(model.A,data.N)-np.eye(2)
    Aeq_Un = matrices.lower_triang_AB[-2:,:]

    Aeq[:,:2] = Aeq_x0
    Aeq[:,2:2+data.N*data.n_u] = Aeq_Un

    return Aeq

def getbeq_Un(data,matrices):
    beq = -(matrices.lower_triang_AC[-2:, :] @ data.env_temp_K.reshape(-1, 1) + 
        matrices.lower_triang_AD[-2:, :] @ data.mul_TQ.reshape(-1, 1) + 
        matrices.lower_triang_AE[-2:, :] @ data.water_demand.reshape(-1, 1))

    return beq

def getAeq_Ua(data, model, matrices_alt):
    Aeq_Ua_plus = np.hstack((np.zeros((data.n_x*data.n_a*data.n_z,data.n_x)),
                        Aeq_Ua_Un(data,model),
                        -Aeq_Ua_Ua(data, matrices_alt),
                        np.zeros((data.n_x*data.n_a*data.n_z,data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R))),
                        np.zeros((data.n_x*data.n_a*data.n_z,2*data.N_R*data.n_a*data.n_z+data.N+1+2*data.n_a+5))))
    
    Aeq_Ua_minus = np.hstack((np.zeros((data.n_x*data.n_a*data.n_z,data.n_x)),
                        Aeq_Ua_Un(data,model),
                        np.zeros((data.n_x*data.n_a*data.n_z,data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R))),
                        -Aeq_Ua_Ua(data, matrices_alt),
                        np.zeros((data.n_x*data.n_a*data.n_z,2*data.N_R*data.n_a*data.n_z+data.N+1+2*data.n_a+5))))
    
    return np.vstack((Aeq_Ua_plus, Aeq_Ua_minus))

def Aeq_Ua_Un_i_z(data,model, i, z): #TODO
    Aeq_Ua_Un_i_z_arr = np.zeros((data.n_x, data.n_u*(data.N)))
    K_i = get_Ki(data).astype("i")
    K_i_act = K_i[i][z*(data.N_F+data.N_R):(z+1)*(data.N_F+data.N_R)]
    for k in range(len(K_i_act)):
        Aeq_Ua_Un_i_z_arr[:,K_i_act[k]*data.n_u:(K_i_act[k]+1)*data.n_u] = np.linalg.matrix_power(model.A, data.N_F+data.N_R-k-1)@model.B
        
    return Aeq_Ua_Un_i_z_arr

def Aeq_Ua_Un_i(data,model, i):
    Aeq_Ua_Un_i_arr = np.zeros((data.n_x*data.n_z, data.n_u*(data.N)))

    for z in range(data.n_z):
        Aeq_Ua_Un_i_arr[data.n_x*z:data.n_x*(z+1),:] = Aeq_Ua_Un_i_z(data,model, i, z)

    return Aeq_Ua_Un_i_arr

def Aeq_Ua_Un(data,model):
    Aeq_Ua_Un_arr = np.zeros((data.n_x*data.n_z*data.n_a, data.n_u*(data.N)))

    for i in range(data.n_a):
        Aeq_Ua_Un_arr[data.n_x*data.n_z*i:data.n_x*data.n_z*(i+1),:] = Aeq_Ua_Un_i(data,model, i)

    return Aeq_Ua_Un_arr

def Aeq_Ua_Ua(data, matrices_alt): #TODO
    Aeq_Ua_Un_arr = np.zeros((data.n_x*data.n_z*data.n_a, data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)))
    for i in range(data.n_z*data.n_a):
        Aeq_Ua_Un_arr[i*2:(i+1)*2, i*data.n_u*(data.N_F+data.N_R):(i+1)*data.n_u*(data.N_F+data.N_R)] = matrices_alt.lower_triang_AB[-2:,:]

    return Aeq_Ua_Un_arr


def beq_Ua(data):
    return np.zeros((2*data.n_x*data.n_a*data.n_z,1))


def getAeq(data, model, matrices, matrices_alt):
    Aeq =  np.vstack((getAeq_Un(data, matrices, model), getAeq_Ua(data, model, matrices_alt)))
    return csr_matrix(Aeq)

def getbeq(data,matrices):
    return np.vstack((getbeq_Un(data,matrices),beq_Ua(data)))
    


    
    
