#!/bin/bash
echo "Checking for iCloud dataless files..."
for f in $(git status --porcelain | awk '{print $2}'); do
    if [ -f "$f" ] && ls -lO "$f" | grep -q "dataless"; then
        echo "Forcing download of $f..."
        brctl download "$f"
        cat "$f" > /dev/null 2>&1
    fi
done
echo "Adding files to git..."
git add .
git commit -m "Auto sync"
git push origin main
echo "Done!"
