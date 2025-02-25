"""
This will be your new module defining SPM-like functions

Here you want the get_spm_globals function from the earlier
``four_dimensions_exercise``, with anything that function imports and other
definitions that the function needs.

When you are done, you should be able to run this spm_funcs.py module as a
script and see the script print a message beginning with "OK".

You run this module as a script like this::

    python3 spm_funcs.py

or better, in IPython::

    %run spm_funcs.py
"""

import numpy as np

import nibabel as nib

import nipraxis


def spm_global(vol):
    """ Calculate SPM global metric for array `vol`

    Parameters
    ----------
    vol : array
        Array giving image data, usually 3D.

    Returns
    -------
    g : float
        SPM global metric for `vol`
    """
    T = np.mean(vol) / 8
    return np.mean(vol[vol > T])


def get_spm_globals(fname):
    """ Calculate SPM global metrics for volumes in image filename `fname`

    Parameters
    ----------
    fname : str
        Filename of file containing 4D image

    Returns
    -------
    spm_vals : array
        SPM global metric for each 3D volume in the 4D image.
    """
    img = nib.load(fname)
    data = img.get_fdata()
    globals = []
    for i in range(data.shape[-1]):
        vol = data[...,i]
        globals.append(spm_global(vol))
    return np.array(globals)



def main():
    # This function run when file executed as a script
    bold_fname = nipraxis.fetch_file('ds107_sub012_t1r2.nii')
    glob_vals = get_spm_globals(bold_fname)
    if glob_vals is None:
        raise ValueError('Did you return your global values?')
    expected_values = np.loadtxt('global_signals.txt')
    if np.allclose(glob_vals, expected_values, rtol=1e-4):
        print('OK: your values and SPMs are close')
    else:
        print('SPM and your values differ')
        print('Yours:', [float(v) for v in glob_vals])
        print('SPMs:', expected_values)


if __name__ == '__main__':
    # File being executed as a script
    main()
