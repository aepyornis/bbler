#!/usr/bin/env python3
import os
import sys
import requests
import helpers
from time import sleep
from pathlib import Path

JOB_URL = "http://a810-bisweb.nyc.gov/bisweb/JobsQueryByNumberServlet?passjobnumber={}"
USER_AGENT = 'Mozilla/5.0'
HEADERS = {'User-Agent': USER_AGENT }
FOLDER = 'data'
UNAVAILABLE = 'Due to the high demand it may take a little longer'
# seconds between download
THROTTLE = 8


def job_url(job_number):
    return JOB_URL.format(job_number)


@helpers.bis_retry
def job_html(job_number):
    r = requests.get(job_url(job_number), headers=HEADERS)
    r.raise_for_status()
    return r.text


def job_file_path(job_number):
    return os.path.join(FOLDER, job_number, "{}.html".format(job_number))


def download_job(job_number):
    html = job_html(job_number)
    if html:
        with open(job_file_path(job_number), 'w') as f:
            f.write(html)
    print("✓ {}".format(job_number))

def download_job_unless_file_exists(job_number):
    job = str(job_number).strip()
    file_path = job_file_path(job)
    if not os.path.isfile(file_path):
        Path(os.path.dirname(file_path)).mkdir(parents=True, exist_ok=True)
        download_job(job)
        sleep(THROTTLE)
    else:
        print("😻 {}".format(job))


if __name__ == '__main__':
    # optionally alllow folder to be redefined
    try:
        FOLDER = sys.argv[2]
    except IndexError:
        pass

    download_job_unless_file_exists(sys.argv[1])
