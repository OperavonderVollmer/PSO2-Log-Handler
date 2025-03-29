from setuptools import setup, find_packages

setup(
    name="LogFileMonitor",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "Log-File-Monitor @ git+https://github.com/OperavonderVollmer/Log-File-Monitor.git@main",
        "OPR-Speaks @ git+https://github.com/OperavonderVollmer/OPR-Speaks.git@main",
        "OperaPowerRelay @ git+https://github.com/OperavonderVollmer/OperaPowerRelay.git",
    ],
    python_requires=">=3.7",
    author="Opera von der Vollmer",
    description="PSO2 Log Handler that reads chat messages",
    url="https://github.com/OperavonderVollmer/LogFileMonitor", 
    license="MIT",
)
