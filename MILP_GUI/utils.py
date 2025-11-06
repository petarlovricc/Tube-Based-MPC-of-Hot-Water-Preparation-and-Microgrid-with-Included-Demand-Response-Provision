import sys
import os
import subprocess

from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QPixmap, QPainter, QIcon
from PySide6.QtCore import Qt
from PySide6.QtCore import QRectF
from docplex.mp.environment import Environment




def check_cplex_full_version():
            try:
                import cplex
                c = cplex.Cplex()
                c.objective.set_sense(c.objective.sense.minimize)

                
                for i in range(10_000):
                    c.variables.add(obj=[1.0], ub=[100.0], lb=[-100.0])

                c.solve()
                return True  

            except ImportError:
                print("CPLEX nije instaliran.")
                return False

            except Exception as e:
                if "Community Edition" in str(e) or "size limits exceeded" in str(e):
                    print("Detektiran CPLEX Community Edition.")
                    return False
                else:
                    print("Greška pri pokretanju CPLEX-a:", e)
                    return False
        
            
def resource_path(relative_path: str) -> str:
    """
    Vrati apsolutnu putanju do resursa.
    Radi i kad se aplikacija pokreće normalno iz Pythona,
    i kad je spakirana u .exe preko PyInstaller-a.
    """
    if hasattr(sys, '_MEIPASS'):
        # kad radi iz .exe (PyInstaller unpacka u privremeni folder)
        base_path = sys._MEIPASS
    else:
        # kad radi normalno iz Pythona
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def invert_svg(path: str, size: int = 128) -> QIcon:
    renderer = QSvgRenderer(path)

    # iscrtamo u kvadrat, ali proporcionalno
    orig_size = renderer.defaultSize()
    scale_factor = min(size / orig_size.width(), size / orig_size.height())

    target_w = int(orig_size.width() * scale_factor)
    target_h = int(orig_size.height() * scale_factor)

    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    # centriraj unutar canvasa
    x = (size - target_w) // 2
    y = (size - target_h) // 2

    painter = QPainter(pixmap)
    renderer.render(painter, QRectF(x, y, target_w, target_h))
    painter.end()

    # invertiraj
    image = pixmap.toImage()
    
    return QIcon(path)

class InfeasibleException(Exception):
    pass