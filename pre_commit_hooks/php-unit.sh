#!/usr/bin/env bash

################################################################################
# 
# Bash PHP Unit Task Runner
#
# Exit 0 if no errors found
# Exit 1 if errors were found
#
# Requires
# - php
#
# Arguments
# - None
################################################################################

# Plugin title
title="PHP Unit Task Runner"

# Possible command names of this tool
local_command="phpunit.phar"
vendor_command="vendor/bin/phpunit"
global_command="php bin/phpunit"

# Print a welcome and locate the exec for this tool
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/helpers/colors.sh
source $DIR/helpers/formatters.sh
source $DIR/helpers/welcome.sh
source $DIR/helpers/locate.sh

echo -e "${bldwht}Running command ${txtgrn}$exec_command${txtrst}"
command_result=`eval $exec_command`
if [[ $command_result =~ ERRORS! ]]
then
    hr
    echo -en "${bldmag}Failures detected in unit tests ... ${txtrst} \n"
    hr
    echo "$command_result"
    exit 1
fi
exit 0
