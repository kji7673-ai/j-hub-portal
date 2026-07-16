#!/bin/bash

# Get absolute path to the directory where this script is located
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# Define commands
CMD_DAILY="python3 $DIR/pipeline_daily.py && python3 $DIR/compile_articles.py"
CMD_WEEKLY="python3 $DIR/pipeline_weekly.py"

# Create a temporary file for the crontab
CRON_FILE=$(mktemp)
crontab -l > "$CRON_FILE" 2>/dev/null

# Remove existing jobs if they exist to avoid duplicates
sed -i '' '/pipeline_daily.py/d' "$CRON_FILE"
sed -i '' '/pipeline_weekly.py/d' "$CRON_FILE"

# Add new jobs
# Daily: Run pipeline_daily.py and compile_articles.py every weekday at 08:00
echo "0 8 * * 1-5 $CMD_DAILY" >> "$CRON_FILE"

# Weekly: Run pipeline_weekly.py every Monday at 07:50 (before daily compile at 08:00)
# This way, when the daily compile runs at 08:00, it picks up the latest weekly articles too.
echo "50 7 * * 1 $CMD_WEEKLY" >> "$CRON_FILE"

# Install new crontab
crontab "$CRON_FILE"
rm "$CRON_FILE"

echo "Cron jobs successfully set up!"
echo "Current crontab:"
crontab -l
