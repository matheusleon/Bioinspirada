import matplotlib.pyplot as plt
import numpy as np

def translate_to_bin(person):
    res = ""
    for gene in person:
        bin_gene = bin(gene)[2:]
        while len(bin_gene) < 3:
            bin_gene = '0' + bin_gene
        res += bin_gene
    return res

def translate_to_perm(bin_gene):
    res = []
    for i in range(0, 24, 3):
        cur_gene = bin_gene[i:i+3]
        res.append(int(cur_gene, 2))
    return res
    
def plot_one_curve(y, name, title, figname):
    #plt.clf()
    plt.plot(y, 'r')
    plt.xlabel('Iteration number')
    plt.ylabel(name)
    plt.title(title)
    plt.legend()
    plt.axis([0, len(y), np.min(y) - 1, np.max(y) + 1])
    plt.savefig(figname)
    #plt.close()
    
def plot_all_curves(all_y, name, title, figname):
    #plt.clf()
    for y in all_y:
        plt.plot(y, 'r')
    plt.xlabel('Iteration number')
    plt.ylabel(name)
    plt.title(title)
    plt.legend()
    plt.axis([0, len(y), np.min(y) - 1, np.max(y) + 1])
    plt.savefig(figname)
    #plt.close()
    
def bar_graph(y, name, title, figname):
    #plt.clf()
    fig, ax = plt.subplots()
    arr = range(len(y))
    y_pos = np.arange(len(y))
    ax.bar(y_pos, y, align='center', width = 0.5, log=False)
    ax.set_xticks(y_pos)
    ax.set_xticklabels(arr)
    ax.set_ylabel(name)
    ax.set_xlabel('Execution')
    plt.locator_params(axis='x', nbins=10)
    
    rects = ax.patches
    
    for rect, v in zip(rects, y):
        if (v > 0):
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height, round(v, 3), ha='center', va='bottom')
    plt.savefig(figname)
    #plt.close()
