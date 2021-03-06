#!/usr/bin/env python
"""Identify UVEX fields in the CASU data quality stats.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import numpy as np
from astropy.table import Table

COLNAMES = ('field', 'dir', 'ra', 'dec', 'l', 'b',
            'runno_u', 'runno_g', 'runno_r', 'runno_hei',
            'time_u', 'time_g', 'time_r', 'time_hei',
            'exptime_u', 'exptime_g', 'exptime_r', 'exptime_hei',
            'seeing_u', 'seeing_g', 'seeing_r', 'seeing_hei',
            'ellipt_u', 'ellipt_g', 'ellipt_r', 'ellipt_hei',
            'sky_u', 'sky_g', 'sky_r', 'sky_hei',
            'noise_u', 'noise_g', 'noise_r', 'noise_hei',
            'airmass_u', 'airmass_g', 'airmass_r', 'airmass_hei',
            'lm_u', 'lm_g', 'lm_r', 'lm_hei')

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
        if not t[idx]['name'].startswith("uvex"):
            continue

        myrun = t[idx]['runno']
        try:
            myname = t[idx]['name'].strip().split('_')[1].split(' ')[0]
        except IndexError:
            # Hack: on one occasion the name had the underscore missing
            myname = t[idx]['name'].strip().split('x')[1].split(' ')[0]
        myfilter = t[idx]['filter'].strip().lower()

        if myfilter not in ['u', 'g', 'r', 'hei']:
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

    Table(fieldlist, names=COLNAMES).write('observed-uvex-fields.fits', overwrite=True)
