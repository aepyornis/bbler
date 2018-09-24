#!/usr/bin/env python3
import os
import sys
import requests
import helpers
from collections import namedtuple
from bs4 import BeautifulSoup, NavigableString
from pathlib import Path
from time import sleep

USER_AGENT = 'Mozilla/5.0'
HEADERS = {'User-Agent': USER_AGENT}
FOLDER = 'dob-data'
THROTTLE = 4  # seconds between download

##
# URLS:
#
VIRTUAL_JOB_FOLDER_URL = "http://a810-bisweb.nyc.gov/bisweb/BScanVirtualJobFolderServlet?passjobnumber={}"
DOCUMENT_URL = "http://a810-bisweb.nyc.gov/bisweb/BSCANJobDocumentContentServlet?passjobnumber={job_number}&scancode={scancode}"


# Helper class
DOCUMENT = namedtuple('DOCUMENT', ['scancode', 'form_id'])

# Right now the only form we are interested in, is the PW1.
# But this script could easily be used to download other
# documents from the virutal job folder.
DESIRED_FORMS = set(['PW1'])


def document_path(document, job_number):
    """
    Returns string path to save the document
    Creates parent folders if needed
    """
    dir_path = Path(os.path.join(FOLDER, job_number))
    dir_path.mkdir(parents=True, exist_ok=True)
    file_name = "{}_{}.pdf".format(document.form_id, document.scancode)
    return os.path.abspath(str(dir_path.joinpath(file_name)))


# DOCUMENT -> string
def document_to_link(document, job_number):
    """ link to the document PDF """
    return DOCUMENT_URL.format(job_number=job_number, scancode=document.scancode)


@helpers.bis_retry
def job_folder_html(job_number):
    """
    Retrives 'virtual job folder' page via GET request.
    Returns a string.
    """
    url = VIRTUAL_JOB_FOLDER_URL.format(job_number)
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.text


def documents(html):
    """
    Parses html, retriving list of documents
    Str -> [DOCUMENT]
    """
    _documents = []
    soup = BeautifulSoup(html, 'html.parser')

    # loop through table of documents
    for tr in soup.find(id="tblVirtualJobFolder"):

        # skips rows without any links
        if isinstance(tr, NavigableString) or len(tr.find_all('a')) == 0:
            continue

        # extract scancode and form_id from table
        scancode = tr.find_all('td')[5].text.strip()
        form_id = tr.find_all('td')[1].text.strip().upper()
        _documents.append(DOCUMENT(scancode, form_id))
    return _documents


@helpers.bis_retry
def download_document(document, job_number):
    """
    Downloads and saves a document
    """
    url = document_to_link(document, job_number)
    print("download url: {}".format(url), file=sys.stderr)
    file_path = document_path(document, job_number)
    if os.path.isfile(file_path):
        print("Document already exists, skipping", file=sys.stderr)
        return True

    r = requests.get(url, headers=HEADERS, stream=True)
    r.raise_for_status()

    # Sometimes an error page is returned instead of
    # a PDF. We can detect that here and raise the error
    if 'html' in r.headers['Content-Type']:
        raise helpers.BisWebUnavailableException

    print("Saving file to {}".format(file_path), file=sys.stderr)
    with open(file_path, 'wb') as f:
        for chunk in r:
            f.write(chunk)
    return True


def download_documents_for_job(job_number):
    """
    Downloads all documents for the job number
    """
    for doc in documents(job_folder_html(job_number)):
        if doc.form_id in DESIRED_FORMS:
            print("Downloading {} ({})".format(doc.form_id, doc.scancode), file=sys.stderr)
            download_document(doc, job_number)
            sleep(THROTTLE)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise Exception("Missing argument, job number")

    try:
        FOLDER = sys.argv[2]
    except IndexError:
        pass

    download_documents_for_job(sys.argv[1])
