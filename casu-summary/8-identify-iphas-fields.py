#!/usr/bin/env python
"""Identify IPHAS fields in the CASU data quality stats.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import numpy as np
from astropy.table import Table

COLNAMES = ('field', 'dir', 'ra', 'dec', 'l', 'b',
            'runno_hal', 'runno_r', 'runno_i',
            'time_hal', 'time_r', 'time_i',
            'exptime_hal', 'exptime_r', 'exptime_i',
            'seeing_hal', 'seeing_r', 'seeing_i',
            'ellipt_hal', 'ellipt_r', 'ellipt_i',
            'sky_hal', 'sky_r', 'sky_i',
            'noise_hal', 'noise_r', 'noise_i',
            'airmass_hal', 'airmass_r', 'airmass_i',
            'lm_hal', 'lm_r', 'lm_i')

fieldlist = []
def register(field):
    # Fill missing values
    for name in COLNAMES:
        if not name in field:
            if name.startswith(('runno', 'time')):
                field[name] = ''
            else:
                field[name] = np.float32(np.nan)
    fieldlist.append(field)


if __name__ == '__main__':
    t = Table.read('observed-egaps-runs.fits')

    field = {'field': 'ignore'}  # hack: "ignore" the first field

    for idx in np.argsort(t['runno']):
        if not t[idx]['name'].startswith("intphas"):
            continue

        myrun = t[idx]['runno']
        try:
            myname = t[idx]['name'].strip().split('_')[1].split(' ')[0]
        except IndexError:
            # Hack: on one occasion the name had the underscore missing
            myname = t[idx]['name'].strip().split('x')[1].split(' ')[0]
        myfilter = t[idx]['filter'].strip().lower()

        if myfilter not in ['hal', 'r', 'i']:
            logging.warn('run {0} used filter {1}'.format(myrun, myfilter))
            continue  # ignore run

        if field['field'] != myname:
            if field['field'] != 'ignore':
                register(field)
            field = {'field': myname, 'dir': t[idx]['dir'],
                     'ra': t[idx]['ra'], 'dec': t[idx]['dec'],
                     'l': t[idx]['l'], 'b': t[idx]['b']}

        for colname in ['runno', 'time', 'exptime', 'seeing', 'ellipt', 'sky', 'noise', 'airmass', 'lm']:
            field[colname+'_'+myfilter] = t[idx][colname]

    Table(fieldlist, names=COLNAMES).write('observed-iphas-fields.fits', overwrite=True)
