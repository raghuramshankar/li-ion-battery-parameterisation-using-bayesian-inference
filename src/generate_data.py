# %%
import pybamm
import sys
import os
import numpy as np
import pandas as pd

# add base folder path
if "__ipython__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(os.getcwd()))))

# setup RC model
model = pybamm.equivalent_circuit.Thevenin()
param = model.default_parameter_values
param["Cell capacity [A.h]"] = 8.0
param["Initial SoC"] = 1.0

# import drive cycle from file
drive_cycle_current = pybamm.step.current(
    pd.read_csv("../data/US06.csv", skiprows=1).to_numpy()
)

experiment = pybamm.Experiment([drive_cycle_current] * 100)

# run simulation
sim = pybamm.Simulation(
    model,
    parameter_values=param,
    solver=pybamm.CasadiSolver(mode="fast"),
    experiment=experiment,
)

# solve the model
solution = sim.solve()
solution.plot(
    [
        "Time [s]",
        "Current [A]",
        "Voltage [V]",
        "R0 [Ohm]",
        "R1 [Ohm]",
        "tau1 [s]",
        "SoC",
        "Discharge capacity [A.h]",
    ]
)

# create solution variables by creating a QuickPlot object
quick_plot = pybamm.QuickPlot(solution)

# save data
solution.save_data(
    "../data/dynamic_data.csv", list(solution.data.keys()), to_format="csv"
)
