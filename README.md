# BBLER

Downloads information about any building in nyc.

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

Install the program ` ./install `

This will set a fish shell universal variable `BBLER_PATH` and make a symlink in `/usr/local/bin`

## Data sources

It grabs PDFs and web-pages from the Department of Finance and Department of Buildings. All other information comes from [NYCDB's api](https://github.com/aepornis/nyc-db).

## Folder structure and schema

The program produces a number of files for any given BBL. The top-level folder is ` ~/.nyc-data `

in dob/[job_number]

    - [job_number].json -> json of information about the job
	
    - [job_number].html -> downloaded bis page for job
	
    - pw1.json  -> parsed bis html

in dof/[bbl] 

    - *.pdf -> downloaded tax bills
	
    - tax_bills.json -> array of parsed tax bills

in bbl/[bbl] 

    - dobjobs.json -> information about the dob (from dobjobs table in nycdb)
	
    - pluto.json -> json of pluto for bbl
	
    - rent_stab.json -> tax bills + compiled stats for the tax bills (see rent-stab.py)

    - [bbl].json -> all above json combined into one object
