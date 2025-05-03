#!/usr/bin/env bash
set -euo pipefail

mkdir -p k400/targz k400/val k400/annotations

cd k400

echo "Fetching list of validation tarballs…"
wget -q https://s3.amazonaws.com/kinetics/400/val/k400_val_path.txt

echo "Downloading tarballs into $(pwd)/targz/"
while IFS= read -r url; do
  wget -P targz "$url"
done < k400_val_path.txt

echo "Extracting all archives into $(pwd)/val/"
while IFS= read -r url; do
  file="${url##*/}"
  echo "Extracting $file"
  tar -zxvf "targz/$file" -C val
done < k400_val_path.txt

echo "Downloading validation annotations…"
wget -q -P annotations https://s3.amazonaws.com/kinetics/400/annotations/val.csv

echo "All done! Files are in:"
echo "  - $(pwd)/targz  (compressed archives)"
echo "  - $(pwd)/val    (extracted videos)"
echo "  - $(pwd)/annotations/val.csv   (annotations)"
