#!/bin/bash

# This setup script will replace the main.py file for the credit check service
# with a version that already includes the tagging changes
#
cp creditcheckservice/main-with-tags.py creditcheckservice/main.py

echo ""
echo Applied the tagging changes to creditcheckservice.
