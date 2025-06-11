import subprocess
import sys




#naredba za runnanje GUI-ja
subprocess.run(f'{sys.executable} -m MILP_GUI.main_window', shell = True, check = True)