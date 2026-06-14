#!/bin/bash
DIR=$1
if [ -z "$DIR" ]; then
  echo "Usage: bash restore.sh snapshots/TIMESTAMP_label"
  exit 1
fi
cp "$DIR/build.py" build.py
cp "$DIR/base.html" theme/base.html
cp "$DIR/pages.json" data/pages.json
echo "Restored from $DIR"
