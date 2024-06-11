#!/bin/sh

# Cron job script to run tasks
/usr/local/bin/python /usr/src/app/download.py
/usr/local/bin/python /usr/src/app/process_zip.py
/usr/local/bin/python /usr/src/app/upload.py
/usr/local/bin/python /usr/src/app/gpt_recommendation.py
