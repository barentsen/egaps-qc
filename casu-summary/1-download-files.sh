#!/bin/bash
# Recursively downloads all *.sum8 and *.list files at Cambridge under
wget --mirror --no-parent --no-verbose -A.sum8,.list --directory-prefix tmp/uvex/ --http-user=$UVEXUSER --http-passwd=$UVEXPASSWD http://apm3.ast.cam.ac.uk/~mike/uvex/
wget --mirror --no-parent --no-verbose -A.sum8,.list --directory-prefix tmp/iphas/ --http-user=$IPHASUSER --http-passwd=$IPHASPASSWD http://apm3.ast.cam.ac.uk/~mike/iphas/
