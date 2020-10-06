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
    
def plot_curve(y, name, title):
    plt.plot(y, 'r')
    plt.xlabel('Generation number')
    plt.ylabel(name)
    plt.title(title)
    plt.legend()
    plt.axis([0, len(y), np.min(y), np.max(y)])
    plt.show()
