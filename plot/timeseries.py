import matplotlib.pyplot as plt
import numpy as np


def interval_shade(t_vec, state_vec, color_dict=None, alpha=0.3, label=True, ax=None):
    if isinstance(t_vec, pd.Series):
        t_vec = t_vec.values
    if isinstance(state_vec, pd.Series):
        state_vec = state_vec.values
    states = np.unique(state_vec)
    
    if color_dict is None:
        cmap = mpl.cm.get_cmap('Paired', len(states))
        color_dict = {s: list(c[:3]) + [alpha]
                      for s, c in zip(states,
                                      [cmap(i/(len(states)-1))
                                       for i in range(len(states))])}
    
    if ax is None:
        ax = plt.gca()
    
    transitions = np.flatnonzero(np.diff(state_vec))
    try:
        t_trans = np.mean(np.vstack([t_vec[transitions], t_vec[transitions + 1]]), axis=0)
    except:
        t_trans = t_vec[transitions+1]

    labeled = []
    for i in range(len(t_trans) + 1):
        if i == 0:
            t1 = t_vec[0]
        else:
            t1 = t_trans[i-1]
        if i == (len(t_trans)):
            t2 = t_vec[-1]
            s = state_vec[-1]
        else:
            s = state_vec[transitions[i]]
            t2 = t_trans[i]
        if s not in labeled and label:
            ax.axvspan(t1, t2, color=color_dict[s], label=s)
            labeled += [s]
        else:
            ax.axvspan(t1, t2, color=color_dict[s])