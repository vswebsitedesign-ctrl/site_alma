#!/bin/bash
LABEL=$1
if [ -z "$LABEL" ]; then
  echo "Usage: bash snapshot.sh \"label\""
  exit 1
fi
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DIR="snapshots/${TIMESTAMP}_${LABEL}"
mkdir -p "$DIR"
cp build.py "$DIR/build.py"
cp theme/base.html "$DIR/base.html"
cp data/pages.json "$DIR/pages.json"
echo "Snapshot saved to $DIR"
