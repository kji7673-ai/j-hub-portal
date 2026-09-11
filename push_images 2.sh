#!/bin/bash
git add docs/index.html index.html
git commit -m "Bump version to v=59"
git push origin HEAD

for file in static/images/* docs/static/images/* *.jpg *.png; do
    if [ -f "$file" ]; then
        git add "$file"
        git commit -m "Add image $file"
        git push origin HEAD
    fi
done
