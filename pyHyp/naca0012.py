"""
This script uses the NACA 0018 airfoil equation to generate a 2D RANS mesh.
This mesh has a blunt trailing edge.
"""
import os
import numpy
from pyhyp import pyHyp

baseDir = os.path.dirname(os.path.abspath(__file__))
surfaceFile = os.path.join(baseDir, "naca0018STL.fmt")
volumeFile = os.path.join(baseDir, "naca0018STL.cgns")

x, y = numpy.loadtxt('naca0018STl.dat', skiprows=1, unpack=True)
#print(x,y)

alpha = numpy.linspace(0, 2 * numpy.pi, len(x))

# Write the plot3d input file:
f = open(surfaceFile, "w")
f.write("1\n")
f.write("%d %d %d\n" % (len(x), 2, 1))
for iDim in range(3):
    for j in range(2):
        for i in range(len(x)):
            if iDim == 0:
                f.write("%g\n" % x[i])
            elif iDim == 1:
                f.write("%g\n" % y[i])
            else:
                f.write("%g\n" % (float(j)))
f.close()

options = {
    # ---------------------------
    #        Input Parameters
    # ---------------------------
    "inputFile": surfaceFile,
    "unattachedEdgesAreSymmetry": False,
    "outerFaceBC": "farfield",
    "autoConnect": True,
    "BC": {
        1: {"jLow": "zSymm", "jHigh": "zSymm", "iLow": "ySymm", "iHigh": "splay"}
    },
    "families": "wall",
    # ---------------------------
    #        Grid Parameters
    # ---------------------------
    "N": 64,
    "s0": 1.0376e-4,
    "marchDist": 1.0,
    # ---------------------------
    #   Pseudo Grid Parameters
    # ---------------------------
    "ps0": -1.0,
    "pGridRatio": -1.0,
    "cMax": 2.0,
    # ---------------------------
    #   Smoothing parameters
    # ---------------------------
    "epsE": 0.5,
    "epsI": 1.0,
    "theta": 4.0,
    "volCoef": 0.5,
    "volBlend": 0.0005,
    "volSmoothIter": 200,
}

hyp = pyHyp(options=options)
hyp.run()
hyp.writeCGNS(volumeFile)
