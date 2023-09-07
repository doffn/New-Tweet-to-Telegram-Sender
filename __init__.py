import os
import time
import sys


# List of filenames
filenames = ["listfile.txt", "data.txt", "ids.txt"]

# Check if each file exists and create it if it doesn't
for filename in filenames:
    if not os.path.exists(filename):
        with open(filename, "w"):
            pass
        print(f"Created {filename}")
    else:
        pass
        #print(f"{filename} already exists")

# List of required packages
required_packages = [
    ('time', 'time'),
    ('requests', 'requests'),
    ('KeepAlive', 'keep_alive'),
    ('collections', 'Counter'),
    ('bs4', 'BeautifulSoup'),
    ('urllib3', 'urllib3'),
    ('psutil', 'psutil'),
    ('logging', 'logging'),
    ('random', 'random'),
    ('http.server', 'http.server'),
    ('threading', 'threading'),
    ('socketserver', 'socketserver'),
    ('pandas', 'pandas'),
    ('telebot', 'telebot')
]

# Check if a package is installed
def package_installed(package_name):
    try:
        __import__(package_name)
    except ImportError:
        return False
    else:
        return True

# Install a package using pip
def install_package(package_name):
    os.system(f"pip install {package_name}")

# Import the necessary modules and packages
for package in required_packages:
    package_name, import_name = package
    if package_installed(package_name):
        globals()[import_name] = __import__(package_name)
        #print("Packages already installed")
    else:
        print(f"Package {package_name} is missing. Please install it.")
        install_package(package_name)


