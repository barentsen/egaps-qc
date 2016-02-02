#!/bin/bash
java -jar /home/gb/bin/topcat-full.jar -stilts tcat in=tmp/egaps-casu-dqc-by-run-with-lm.csv ifmt=csv \
ocmd="addcol -before run runno parseInt(substring(run,1));
      addcol -before ra_hms ra hmsToDegrees(ra_hms);
      addcol -before ra_hms dec dmsToDegrees(dec_dms);
      replacecol name 'name.toLowerCase()';
      addskycoords -inunit deg -outunit deg icrs galactic ra dec l b;
      addcol field 'trim(name.split(\"_\")[1].split(\" \")[0])';" \
ofmt=fits out=observed-egaps-runs.fits
#gzip uvex-casu-dqc.fits

# select 'name.startsWith(\"uvex\")';
# replacecol seeing parseFloat(seeing);
# replacecol sky parseFloat(sky);
# replacecol ellipt parseFloat(ellipt);
