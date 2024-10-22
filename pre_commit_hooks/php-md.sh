#!/usr/bin/env bash
################################################################################
#
# Bash PHPMD
#
# This script fails if the PHPMD output has the word "ERROR" in it.
#
# Exit 0 if no errors found
# Exit 1 if errors were found
#
# Requires
# - php
#
# See: https://phpmd.org/rules/index.html
#
################################################################################

# Plugin title
title="PHPMD"

# Possible command names of this tool
local_command="phpmd.phar"
vendor_command="vendor/bin/phpmd" 
global_command="phpmd"

# Print a welcome and locate the exec for this tool
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/helpers/colors.sh
source $DIR/helpers/formatters.sh
source $DIR/helpers/welcome.sh
source $DIR/helpers/locate.sh

command_args=$1
command_to_run="${vendor_command} src/ text phpmd.xml.dist"

echo -e "${bldwht}Running command ${txtgrn} ${command_to_run}"
hr
command_result=`eval $command_to_run`
if [[ ${#command_result} > 0 ]]
then
    hr
    echo -en "${bldmag}Errors Mess detected by ${title}... ${txtrst} \n"
    hr
    echo "$command_result"
    exit 1
fi

exit 0
