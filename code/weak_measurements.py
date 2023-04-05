#
# Author: Victor Gitton
# Course: Advanced Topics in Quantum information theory 2023, ETH Zurich
# 

# PARAMETERS -------------

# Physics 

# The r_z component of the density matrix rho
rz_rho = 0.42
# The target worst case single-qubit fidelity, which fixes the measurement
worst_case_fidelity = 0.95
# The number of qubits
N_qubits = 10000

# Misc

# How many points we will show
N_attempts = 40
font_size = 17
# May want to set this one to false depending on the backend...
try_to_maximize_window = True

# ------------------------

# COLORS -----------
myblue   = "#235789"
myred    = "#CA1551"
myyellow = "#F2C078"
mypink   = "#CC7E85"
mygreen  = "#1B998B"
# ------------------

import random
import matplotlib.pyplot as plt
from numpy import sqrt

# =========== FUNCTIONS =============

# PHYSICS ----------

def get_Gs():
    delta = 1. - worst_case_fidelity
    F = 1. - 2.*delta
    
    Gs = [0., 0.]

    # Random measurement, F + G = 1
    Gs[0] = 1. - F
    # Weak measurement, F^2 + G^2 = 1
    Gs[1] = sqrt(1. - F ** 2)

    return Gs

# SAMPLING ---------

# Param G in range [0,1]
# Returns \pm1 with probability 0.5*(1 \pm G*rz)
def sample_pm_var(G):
    # This happens with probability 0.5*(1 + G*rz)
    if(random.random() < 0.5*(1 + G*rz_rho)):
        return +1
    else:
        return -1

# Param G in range [0,1]
# Returns the average of N calls to sample_pm_var(G)
def sample_average(G):
    ret = 0
    for i in range(N_qubits):
        ret += sample_pm_var(G)
    ret /= N_qubits
    return ret

# Param G in range [0,1]
# Returns sample_average(G) / G
def sample_unbiased_average(G):
    assert G > 0.
    return sample_average(G) / G

# Param G
# Param i : 0 (1) = assign low (high) random y value
#           (for visualization purposes only)
# Returns (x-list, y-list)
def sample_data_points(G, i):
    return (
        [sample_unbiased_average(G)        for _ in range(N_attempts)],
        [0.2 + 0.4*i + 0.2*random.random() for _ in range(N_attempts)]
    )

# PLOTTING ------------

def get_color(i):
    if i == 0:
        return myblue
    else:
        return mygreen
    
def get_name(i):
    if i == 0:
        return "Random measurement"
    else:
        return "Weak measurement"

def plot_data_points(ax, G, i):
    data_points = sample_data_points(G, i)
    ax.scatter(data_points[0], data_points[1], 
               facecolor=get_color(i), 
               label=get_name(i),
               marker="o"
    )

def plot_vert_line_discrete(ax, x, color):
    ax.plot([x, x], [0., 1.], color=color, linewidth=1.5, linestyle="dashed")

def plot_vert_line(ax, x, color):
    ax.plot([x, x], [0., 1.], color=color, linewidth=1.5, linestyle="solid")

def get_ax():
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    plt.rcParams.update({'font.size': font_size})
    
    if try_to_maximize_window:
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
    
    return ax

def decorate(ax):
    xlim = ax.get_xlim()
    if xlim[0] > -1:
        ax.set_xlim(xmin = -1.)
    else:
        plot_vert_line_discrete(ax, -1., "darkgrey")
    if xlim[1] < 1.:
        ax.set_xlim(xmax =  1.)
    else:
        plot_vert_line_discrete(ax,  1., "darkgrey")

    ax.set_ylim(0., 1.)
    ax.set_yticks([])
    
    # ax.set_xlabel(r"$r_z$", size=font_size)
    ax.set_xticks([-1., rz_rho, 1.])
    ax.set_xticklabels(["-1", r"$r_z(\rho)$", "+1"], size=font_size)
    plot_vert_line(ax, rz_rho, myred)
    ax.legend()

    ax.set_title(r"Weak vs random measurement, $\mathcal{F}_{\mathrm{w}} = "
                 + str(worst_case_fidelity)
                 + r"$, N = " + str(N_qubits))

# MAIN ----------------

def main():

    # Seed with current time
    random.seed()

    Gs = get_Gs()
    ax = get_ax()

    for i in [1,0]:
        G = Gs[i]
        plot_data_points(ax, G, i)
    
    # To plot the extremal values possible (rarely achieved anyway)
    # min_G = min(Gs)
    # ax.set_xlim(1.05 * (-1./min_G), 1.05 * (1./min_G))

    decorate(ax)
    
    plt.show()
    
if __name__=="__main__":
    main()
