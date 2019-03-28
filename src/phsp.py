#!/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import sys
import os
import uproot
import time

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

''' ---------------------------------------------------------------------------
Load a PHSP (Phase-Space) file
Output is numpy structured array
'''
def load(filename, nmax=-1):
    b, extension = os.path.splitext(filename)
    nmax = int(nmax)

    if extension == '.root':
        return load_root(filename, nmax)

    # if extension == '.raw':
    #     return load_raw(filename)

    if extension == '.npy':
        return load_npy(filename, nmax)

    print('Error, dont know how to open phsp with extension ',
          extension,
          ' (known extensions: .root .npy)')
    exit(0)


''' ---------------------------------------------------------------------------
Load a PHSP (Phase-Space) file in root format
Output is numpy structured array
'''
def load_root(filename, nmax=-1):
    nmax = int(nmax)
    # Check if file exist
    if (not os.path.isfile(filename)):
        print("File '"+filename+"' does not exist.")
        exit()

    # Check if this is a root file
    try:
        f = uproot.open(filename)
    except Exception:
        print("File '"+filename+"' cannot be opened, not root file ?")
        exit()

    # Look for a single key named "PhaseSpace"
    k = f.keys()
    try:
        psf = f['PhaseSpace']
    except Exception:
        print("This root file does not look like a PhaseSpace, keys are: ",
              f.keys(), ' while expecting "PhaseSpace"')
        exit()
        
    # Get keys
    names = [k.decode('UTF-8') for k in psf.keys()]
    n = psf.numentries

    # Convert to arrays (this take times)
    if (nmax != -1):
        a = psf.arrays(entrystop=nmax)
    else:
        a = psf.arrays()

    # Concat arrays
    d = np.column_stack( a[k] for k in psf.keys())
    
    return d, names, n


''' ---------------------------------------------------------------------------
Load a PHSP (Phase-Space) file in npy
Output is numpy structured array
'''
def load_npy(filename, nmax=-1):
    # Check if file exist
    if (not os.path.isfile(filename)):
        print("File '"+filename+"' does not exist.")
        exit()

    x = np.load(filename, mmap_mode='r')
    n = len(x)
    print(nmax, n)
    if nmax > 0:
        x = x[:nmax]
    data = x.view(np.float32).reshape(x.shape + (-1,))
    #data = np.float64(data)
    return data, x.dtype.names, n


