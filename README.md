# BBLER

Downloads and reports information about buildings in nyc.


## Setup

It's a hodgepodge of scripts glued together by 🐟!

You'll need these installed:

- [fish](https://fishshell.com/)
- [python3](https://www.python.org/downloads/) (3.5+)
- [nodejs](https://nodejs.org/en/) (8+)

A handful of shell utilities and programs (which you may have already) are also required:

- [jq](https://stedolan.github.io/jq/)
- curl
- find
- xargs


Install node packages: ` npm install `

Install python3 packages: ` pip3 install -r requirements.txt `


## Folder structure and "database" schema

The program uses the file system as a database. The top-level folder is ` ~/.nyc-data `

Tax bills are stored in ` ~/.nyc-data/dof/[BBL] `

DOB permits/PW1  are stored in ` ~/.nyc-data/dob/[JOB-NUMBER] `

parsed json output from dob and tax bills along with other information retrived from nycdb is stored at ` ~/.nyc-data/bbl/[BBL]
