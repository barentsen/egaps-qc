#!/bin/bash
# This script will concatenate all 
# the summary.sum8 files into a single file

OUTPUT="tmp/concatenated-sum8-files.txt"

# Copy the header line from one of the files
HEADER=`head -n1 "tmp/uvex/apm3.ast.cam.ac.uk/~mike/uvex/aug2010/dqcinfo/summary.sum8"`
echo $HEADER > $OUTPUT

# Now copy the contents of all summary.sum8 files, except the header line
for FILE in `find tmp/ -name "summary.sum8"`; do
	echo "Adding $FILE"
	# Name of the run (e.g. oct2009) is the name of the 5th-level subdirectory
	RUNMONTH=`echo $FILE | cut -d"/" -f5`
	# Pad the string with spaces to respect the "fixed width" ascii format
	RUNMONTH_PADDED=`printf %15s $RUNMONTH`
	# --invert-match is used to grep everything EXCEPT the header line
	# sed is used to prefix every line with the padded runmonth
	grep --invert-match "Run" $FILE | grep --invert-match '^$' | sed -e "s/^/$RUNMONTH_PADDED /" > /tmp/sum8
	cat /tmp/sum8 >> $OUTPUT.tmp
done
sort -u $OUTPUT.tmp > $OUTPUT
rm $OUTPUT.tmp

# Also concatenate the summary.list files
OUTPUT_LISTS="tmp/concatenated-summary-lists.txt"
echo "Writing $OUTPUT_LISTS"
for FILE in `find tmp/ -name "summary.list"`; do
    echo "Adding $FILE"
    cat $FILE >> $OUTPUT_LISTS
done
