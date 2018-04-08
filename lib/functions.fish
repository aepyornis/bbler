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
