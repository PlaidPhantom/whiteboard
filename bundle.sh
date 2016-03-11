#!/bin/bash

echo "Bundling $1..."

OUTPUT="$1"

shift

echo "" > $OUTPUT

for FILE in "$@"; do
    cat $FILE >> $OUTPUT
    echo ";"  >> $OUTPUT
done


exit 0
