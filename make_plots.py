import matplotlib.pyplot as plt
import numpy as np
import math
import mcnp_parser as mcnp

spectrum_7 = mcnp.read_output("mcnp_file/100d_800k.o")
spectrum_6 = mcnp.read_output("mcnp_file/100d_1200k.o")

input_file = open("data/endf-6[65834].txt", 'r')
E = []
b = []

for line in input_file:
    line_ = line.split(',')

    E.append(float(line_[0]))
    b.append(float(line_[1]))


for i in range(len(spectrum_6)):
    if(i % 2 == 0):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.semilogx()

        plt.grid(which='major', alpha=1)
        plt.grid(which='minor', alpha=0.5)

        x = [val[0] * 1e6 for val in spectrum_6[i]]
        y_6 = [val[1] for val in spectrum_6[i]]
        y_7 = [val[1] for val in spectrum_7[i]]
        y = [(y_7[i] - y_6[i]) / y_7[i] for i in range(len(y_7))]

        y_err_6 = [val[2] for val in spectrum_6[i]]
        y_err_7 = [val[2] for val in spectrum_7[i]]
        y_err = [math.sqrt(math.pow(y_err_7[j] / y_7[j], 2) +
                           math.pow(y_err_6[j] / y_6[j], 2)) for j in range(len(y_7))]

        for j in range(len(y)):
            if x[j] < 0.05 or x[j] > 1e6:
                y_err[j] = 0.

        ax.errorbar(x, y, xerr=0.0, yerr=y_err, linewidth=.3,
                   label='Relative Spectrum Difference')

        ax2 = fig.add_subplot(111, sharex=ax, frameon=False)
        line1 = ax2.loglog(E, b, linewidth=.3, color='red', 
                           label='Er-167 Total XS')
        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position('right')

        major_ticks = np.logspace(-3, 7, 11)

        minor_ticks = []
        for j in np.arange(-3, 7, 1):
            minor_ticks += list(np.arange(pow(10., j) * 2,
                                          pow(10., j) * 9, pow(10., j)))
        name = "myspectrum_" + str(int(i / 2)) + ".png"
        h1, l1 = ax.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax.legend(h1+h2, l1+l2, loc='upper right', fontsize='small')
        plt.xlim(5e-2, 1e3)
        plt.title('Spect Diff (800K & 1200K) vs  Er-167 XS (time step=' +\
str(int(i / 2)) + ')' )
        ax.set_ylabel('Rel Diff [-]')
        ax2.set_ylabel('Total XS [b]')
        plt.xlabel('Neutron Energy [eV]')
        plt.savefig(name, dpi=500)
