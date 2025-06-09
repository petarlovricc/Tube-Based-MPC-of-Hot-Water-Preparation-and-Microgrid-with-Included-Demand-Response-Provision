import MILP_formulation.MILP_peak_power as optim


class MILP_comparison:
    def __init__(self,first_optim, second_optim, *args):
        self.first_optim = first_optim
        self.second_optim = second_optim
        self.data = optim.getData(*args)
        self.result1 = None
        self.result2 = None
        
        self.getResult1()
        self.getResult2()


    def getResult1(self):
        if(self.first_optim == 0):
            pass
        elif(self.first_optim == 1):
            self.model = optim.getModel(self.data)
            self.matrices = optim.get_Matrices(self.data,self.model)

            result1_sol = optim.solve_cplex(self.data,
                          f = optim.getF(self.data),
                          Aeq=optim.getAeq(self.data,self.matrices,self.model),
                          beq = optim.getbeq(self.data,self.matrices,self.model),
                          Aineq = optim.getAineq(self.data,self.matrices),
                          bineq = optim.getbineq(self.data,self.matrices),
                          lb = optim.getLb(self.data,self.matrices),
                          ub = optim.getUb(self.data,self.matrices))
            
            self.result1 = optim.result_processing(self.data, self.matrices,result1_sol.x)
            
    def getResult2(self):
        if(self.second_optim in [0,1,2]):
            pass
        elif(self.second_optim == 3):
            self.data.cpp = 0
            self.model = optim.getModel(self.data)
            self.matrices = optim.get_Matrices(self.data,self.model)

            result2_sol = optim.solve_cplex(self.data,
                          f = optim.getF(self.data),
                          Aeq=optim.getAeq(self.data,self.matrices,self.model),
                          beq = optim.getbeq(self.data,self.matrices,self.model),
                          Aineq = optim.getAineq(self.data,self.matrices),
                          bineq = optim.getbineq(self.data,self.matrices),
                          lb = optim.getLb(self.data,self.matrices),
                          ub = optim.getUb(self.data,self.matrices))
            
            self.result2 = optim.result_processing(self.data, self.matrices,result2_sol.x)



    