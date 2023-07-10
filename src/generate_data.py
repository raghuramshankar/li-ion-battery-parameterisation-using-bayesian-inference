# %%
import pybamm
import sys
import os
import numpy as np
import pandas as pd

if "__ipython__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(os.getcwd()))))


# current function
def current_func(a, omega):
    def current(t):
        # parameterize upto 3C current
        return a + 5 * a * pybamm.sin(2 * np.pi * omega * t)
        # return a * pybamm.sin(2 * np.pi * omega * t)

    return current


# setup RC model
model = pybamm.equivalent_circuit.Thevenin()
# model = pybamm.lithium_ion.SPMe()
param = model.default_parameter_values
# a = param["Cell capacity [A.h]"]
a = param["Nominal cell capacity [A.h]"]
omega = 0.1

# constant 1C discharge with 3C magnitude sine function
param["Current function [A]"] = current_func(a, omega)
param["Initial SoC"] = 1

# run simulation
sim = pybamm.Simulation(
    model, parameter_values=param, solver=pybamm.CasadiSolver(mode="fast")
)

# need enough timesteps to resolve output
simulation_time = 3600
npts = int(50 * simulation_time * omega)
t_eval = np.linspace(0, simulation_time, npts)

# save solution
solution = sim.solve(t_eval)
solution.plot(
    [
        "Current [A]",
        "R0 [Ohm]",
        "R1 [Ohm]",
        "C1 [F]",
        "tau1 [s]",
        "SoC",
        "Discharge capacity [A.h]",
    ]
)
quick_plot = pybamm.QuickPlot(solution)

solution.save_data(
    "../data/discharge_data.csv", list(solution.data.keys()), to_format="csv"
)
