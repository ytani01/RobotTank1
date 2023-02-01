#!/bin/sh

VENVDIR=$HOME/env2-robottank
BINDIR=$VENVDIR/bin

. $BINDIR/activate

echo "VIRTUAL_ENV=$VIRTUAL_ENV"

while true; do
    python3 -m ab_shutter dc-mtr 1 2
    sleep 2
done
