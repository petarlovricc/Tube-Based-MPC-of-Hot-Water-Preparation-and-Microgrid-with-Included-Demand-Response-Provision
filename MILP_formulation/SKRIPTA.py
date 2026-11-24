import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_packages(packages):
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} is not installed. Installing...")
            install(package)
        else:
            print(f"{package} is already installed.")

# Packages to check and install
packages_to_install = ['numpy', 'scipy', 'matplotlib']

#check_and_install_packages(packages_to_install)
