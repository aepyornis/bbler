# Helper functions for BBLer

function verify_bbl_input -a args
    #  Ensure first argument is a properly formated BBL
    if test (count $args) -eq 0
	printf "\e[31mPlease provide a BBL!\e[0m"
	exit 1
    else if not string match -q --regex '^[12345]{1}[0-9]{9}$' $args[1]
	printf "\e[31mInvalid BBL!\e[0m"
	exit 1
    end
end


function print_error -a message
    printf "\e[31m$message\e[0m\n"
end

function print_blue -a message
    printf "\e[34m$message\e[0m\n"
end



function _setup_folder_structure
    # This is the outer folder where all data is saved
    mkdir -p ~/.nyc-data
    
    mkdir -p ~/.nyc-data/dof
    mkdir -p ~/.nyc-data/dob
    mkdir -p ~/.nyc-data/bbl
end

function dobjobs_for -a bbl
    cat ~/.nyc-data/bbl/$bbl/dobjobs.json | jq '.[] | .job' | sort | uniq
end

function job_info_for -a job_number
    curl -sS -G "https://api.nycdb.info/dobjobs" --data "job=eq.$job_number"
end


function download_and_parse_job -a job_number bbl
    # scripts
    set -l job_download $BBLER_PATH/lib/job_download.py
    set -l job_parse $BBLER_PATH/lib/job_parse.py
    # file and folder vars
    set -l dob_folder ~/.nyc-data/dob
    set -l job_html_file "$dob_folder/$job_number/$job_number.html"
    set -l job_json_file "$dob_folder/$job_number/pw1.json"
    set -l dobjob_info_file "$dob_folder/$job_number/$job_number.json"
    set -l dobjobs_file ~/.nyc-data/bbl/$BBL/dobjobs.json

    if not test -s $job_html_file
	mkdir -p "$dob_folder/$job_number"
	python3 $BBLER_PATH/lib/job_download.py $job_number $dob_folder
    end

    if not test -s $job_json_file
	set -l parsed_dob_file_tmp_file (mktemp)
	python3 $job_parse $job_html_file > $parsed_dob_file_tmp_file
	
	if test $status -eq 0
	    mv $parsed_dob_file_tmp_file $job_json_file
	else
	    print_error "Error parsing $job_html_file"
	end
    end

    if not test -s $dobjob_info_file
	job_info_for $job_number | jq -M '.' > $dobjob_info_file
    end
end


function unit_counts_as_csv_for -a bbl
    cat ~/.nyc-data/bbl/$bbl/$bbl.json | jq '.dof.unitCounts | [."2015", ."2016", ."2017"] | @csv'
end
