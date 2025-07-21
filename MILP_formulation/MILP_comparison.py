from MILP_GUI.param_page import ParamPage
from MILP_GUI.loading_page import LoadingPage
from MILP_GUI.result_page import ResultPage 
from Multithreading.worker import Worker
import MILP_formulation.extrasprojekt
import MILP_formulation.MILP_peak_power as noflex_matrix
import Parameters.getData_noflex as noflex_data
import MILP_formulation.MILP_flex as flex_matrix
import Parameters.getData_flex as flex_data
import Result_Processing.result_processing_noflex as noflex_results
import Result_Processing.result_processing_flex as flex_results
import MILP_solve.milp_solve_no_flex as noflex_solve
import MILP_solve.milp_solve_flex as flex_solve

from MILP_formulation.histereza import runHistereza

class MILP_comparison:
    def __init__(self,flex, first_optim, second_optim, heater, *args):
        self.first_optim = first_optim
        self.second_optim = second_optim
        self.heater = heater
        self.data = noflex_data.getData(*args)
        if flex:
            self.data_flex = flex_data.getData(*args)
        self.result1 = None
        self.result2 = None
        
        self.getResult1()
        self.getResult2()


    def getResult1(self):
        if(self.first_optim == 0):
            data = self.data_flex
            model = flex_matrix.getModel(data)
            matrices = flex_matrix.get_Matrices_nom(data, model)
            matrices_alt = flex_matrix.getMatrices_alt(data, model)
            

            print("POKRECEM OPTIMIZACIJU")
            result1_sol = flex_solve._solve_cplex(
                            f = flex_matrix.getF(data),
                            Aeq= flex_matrix.getAeq(data,model,matrices, matrices_alt),
                            beq = flex_matrix.getbeq(data,matrices),
                            Aineq = flex_matrix.getAineq(data,matrices, model, matrices_alt),
                            bineq = flex_matrix.getbineq(data,matrices, matrices_alt, model),
                            lb = flex_matrix.getLb(data,matrices, matrices_alt),
                            ub = flex_matrix.getUb(data,matrices, matrices_alt),
                            data = data,
                            heater = self.heater)
            self.result1 = flex_results.result_processing(data, model, matrices, matrices_alt, result1_sol.x)

        elif(self.first_optim == 1):
            self.model = noflex_matrix.getModel(self.data)
            self.matrices = noflex_matrix.get_Matrices(self.data,self.model)

            result1_sol = noflex_solve.solve_cplex(self.data,
                          f = noflex_matrix.getF(self.data),
                          Aeq=noflex_matrix.getAeq(self.data,self.matrices,self.model),
                          beq = noflex_matrix.getbeq(self.data,self.matrices,self.model),
                          Aineq = noflex_matrix.getAineq(self.data,self.matrices),
                          bineq = noflex_matrix.getbineq(self.data,self.matrices),
                          lb = noflex_matrix.getLb(self.data,self.matrices),
                          ub = noflex_matrix.getUb(self.data,self.matrices),
                          heater = self.heater)
            
            self.result1 = noflex_results.result_processing(self.data, self.matrices,result1_sol.x)
            
    def getResult2(self):
        if(self.second_optim == 0):
            print(f"ovo je cpp {self.data.cpp}")
            self.model = noflex_matrix.getModel(self.data)
            self.matrices = noflex_matrix.get_Matrices(self.data,self.model)

            result1_sol = noflex_solve.solve_cplex(self.data,
                          f = noflex_matrix.getF(self.data),
                          Aeq=noflex_matrix.getAeq(self.data,self.matrices,self.model),
                          beq = noflex_matrix.getbeq(self.data,self.matrices,self.model),
                          Aineq = noflex_matrix.getAineq(self.data,self.matrices),
                          bineq = noflex_matrix.getbineq(self.data,self.matrices),
                          lb = noflex_matrix.getLb(self.data,self.matrices),
                          ub = noflex_matrix.getUb(self.data,self.matrices),
                          heater = self.heater)
            
            self.result2 = noflex_results.result_processing(self.data, self.matrices,result1_sol.x)
            
            

        elif(self.second_optim == 1):
            #TODO histereza
            self.result2 = runHistereza(self.data, self.result1, 10)

        elif(self.second_optim == 2):
            self.data.cpp = 0
            self.model = noflex_matrix.getModel(self.data)
            self.matrices = noflex_matrix.get_Matrices(self.data,self.model)

            result2_sol = noflex_solve.solve_cplex(self.data,
                          f = noflex_matrix.getF(self.data),
                          Aeq=noflex_matrix.getAeq(self.data,self.matrices,self.model),
                          beq = noflex_matrix.getbeq(self.data,self.matrices,self.model),
                          Aineq = noflex_matrix.getAineq(self.data,self.matrices),
                          bineq = noflex_matrix.getbineq(self.data,self.matrices),
                          lb = noflex_matrix.getLb(self.data,self.matrices),
                          ub = noflex_matrix.getUb(self.data,self.matrices),
                          heater = self.heater)
            
            self.result2 = noflex_results.result_processing(self.data, self.matrices,result2_sol.x)

            self.result2.case = "noflexcpp"



    