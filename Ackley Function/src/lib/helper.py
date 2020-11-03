import matplotlib.pyplot as plt

def plot_result(bests, means, stds, figname):

    plt.plot(bests, 'r', label='Best')
    plt.plot(means, 'g', label='Mean')
    plt.plot(stds, 'b', label='Standard Deviation')
    plt.locator_params(axis='x', nbins=10)
    plt.xlabel('Iteration number')
    plt.legend()
    #diff = np.max(y) - np.min(y)
    #plt.axis([0, len(y), np.min(y) - diff, np.max(y) + diff])
    plt.savefig(figname)
    plt.close()
