import numpy as np
import sys

def read_output(input):
    f = open(input, 'r')
    store = False
    spectrum = []
    total = 0
    spectra = []
    for line in f:
        if(store):
            if "total" in line:
                total = float(line.split()[1])
                store = False
   #             for i in range(len(spectra)):
   #                 spectra[i][1] *= 1./total
   #                 spectra[i][2] *= 1./total
                spectrum.append(spectra)
                total = 0
                spectra = []
            elif "energy" not in line:
                line_elements = line.split()
                spectra.append([float(i) for i in line_elements])
        if "cell union total" in line:
           store = True

    return spectrum

def main():
    file = sys.argv[1]
    read_output(file)


if __name__ == '__main__':
    main()
