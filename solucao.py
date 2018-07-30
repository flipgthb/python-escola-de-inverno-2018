import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

rand = np.random.rand
choice = np.random.choice

def delta_E(lattice,site):
    i,j = site
    n,m = lattice.shape
    I, J = [(i-1)%n,(i+1)%n,i,i],[j,j,(j-1)%m,(j+1)%m]
    return 2*lattice[i,j]*(lattice[I,J].sum())

def maybe_flip_spin(lattice,beta):
    n,m = lattice.shape
    i,j = choice(n),choice(m)
    dE = delta_E(lattice, (i,j)) 
    flip = False
    if dE <= 0 or np.random.rand() < np.exp(-beta*dE):
        lattice[i,j] *= -1
        flip = True
    return flip

def init():
    ax.set_xticks([])
    ax.set_yticks([])
    for (_,s) in ax.spines.items():
        s.set_visible(False)
    ax.set_title(r'$\beta = $' + f'{beta}')
    steps_text.set_text('sfps: ')
    attempts_text.set_text('aps: ')
    return img, steps_text, attempts_text

def update(t):
    f = maybe_flip_spin(S,beta)
    global total_attempts
    total_attempts += 1
    if f:
        img.changed()
        global total_flips
        total_flips += 1
    steps_text.set_text(f'sfps: {(total_flips/(S.shape[0]*S.shape[1])):.3}')
    attempts_text.set_text(f'aps: {(total_attempts/(S.shape[0]*S.shape[1])):.3}')
    return img, steps_text, attempts_text

S = np.random.choice([-1,1],(16,16))
beta = 2
total_flips = 0
total_attempts = 0
fig, ax = plt.subplots()
img = plot_ising_spins(S,ax=ax,cmap='viridis',animated=True)
steps_text = ax.text(0.02, 0.95, 'sfps: ',color='r', size=12, transform=ax.transAxes)
attempts_text = ax.text(0.02, 0.90, 'aps: ',color='r', size=12, transform=ax.transAxes)
anim = FuncAnimation(fig, update,interval=1,init_func=init, blit=True)