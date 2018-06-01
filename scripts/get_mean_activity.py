#!/usr/bin/env python

import numpy as np
import subprocess
from scipy.optimize import curve_fit
import json

MAXACT = 10000.

def logistic(x, u05, alpha):
    return MAXACT/(1.+np.exp(-(x-u05)/alpha))


subprocess.call(['/home/hd/hd_hd/hd_wv385/git/neuralsampling/neuralsampler/bin/neuralsampler', 'sim.json'], stdout=open('output', 'w'))

print("Parsing output")
with open('output', 'r') as f:
    for line in f:
        # Find summary output
        if line.startswith('____End'):
            break
    for line in f:
        # Find content begin
        if line.startswith('-----------'):
            break
    nspikes = []
    for line in f:
        try:
            n = int(line.strip().split()[1])
            nspikes.append(n)
        except IndexError:
            break

simdict = json.load(open('sim.json', 'r'))
MAXACT = simdict["Config"]["nupdates"] / simdict["Config"]["tauref"]

popt, pcov = curve_fit(logistic, simdict['bias'], nspikes, p0=[0.0, 1.0])
u05 = float(popt[0])
alpha = float(popt[1])
print(popt, pcov)


outdict = {'parameters': simdict,
           'results': {'nspikes': nspikes, 'u05': u05, 'alpha': alpha, 'cov': pcov.tolist()}}
json.dump(outdict, open('analysis', 'w'))
