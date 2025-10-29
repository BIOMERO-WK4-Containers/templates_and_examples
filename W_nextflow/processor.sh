#!/usr/bin/env bash

RESFILE="res_of_$1"

echo "PWD: " $PWD > "$RESFILE"
echo "params: " $@ >> "$RESFILE"

# This is currently only a demo script that simulates processing
# of files that are listed on this script's command line.
# The files are "basenames" (without paths), nevertheless they
# are in the script's current working directory -- so, one just
# "opens" them without any path mangling.
#
# The script must create an output file in the current working
# directory, and the file must be prefixed with "res_of_"
# (to make nextflow happy, nextflow is watching for such files).

