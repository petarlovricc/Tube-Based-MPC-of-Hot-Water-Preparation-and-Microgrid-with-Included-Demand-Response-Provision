# Household DR - Diplomski rad - Petar Lovrić

GitHub repozitorij za sve kodove za završni rad, diplomske seminare, diplomski projekt i diplomski rad 

## Setup Instructions
Follow these steps to set up the development environment:

1. Install CPLEX Optimization Studio 22.1.2

2. Clone the repository:
```aiignore
git clone https://github.com/KarnelutiA/Household_DR
cd Household_DR
```

3. Create a Virtual Environment:
```aiignore
conda create -n housedr python=3.10
conda activate housedr
```

4. Install dependencies:
```aiignore
pip install -r requirements.txt
```

5. Activate full CPLEX license.  
Make sure you don't have any Python processes running (e.g. a Python console), otherwise it throws an error.  
Adjust path to the CPLEX installation - the provided one is default for Windows installation.
```aiignore
docplex config --upgrade "C:\Program Files\IBM\ILOG\CPLEX_Studio2212"
```

6. Test if CPLEX is running with full version (not community version which is limited 
to 1000 variables and 1000 constraints).
```aiignore
import cplex
c = cplex.Cplex()
c.objective.set_sense(c.objective.sense.minimize)
for i in range(10_000):
    c.variables.add(obj=[1], ub=[100], lb=[-100])
c.solve()
```
If everything is correct, you should get something like:
```aiignore
Version identifier: 22.1.2.0 | 2024-11-25 | 0edbb82fd
CPXPARAM_Read_DataCheck                          1
Parallel mode: deterministic, using up to 12 threads for concurrent optimization:
 * Starting dual Simplex on 1 thread...
 * Starting Barrier on 9 threads...
 * Starting primal Simplex on 1 thread...
 * Starting Sifting on 1 thread...
Tried aggregator 1 time.
LP Presolve eliminated 0 rows and 10000 columns.
All rows and columns eliminated.
Presolve time = 0.02 sec. (0.97 ticks)

Dual simplex solved model.
```