#!/bin/bash

### Script to delete batches of Detectors
### Run by passing the Access Token, Realm and Search String as paramaters e.g.
### ./delete_detectors.sh $ACCESS_TOKEN $REALM $SEARCH
###
### Tip: The Search String is typically the beginning of the name, use %20 for any spaces
###
### Ensure the Search String only returns the Detectors you want to delete

### Read in the paramaters from the command line ###
ACCESS_TOKEN=$1
REALM=$2
SEARCH=$3

### Check the paramaters have been set, abort if any of them are missing ###
if [ -z "$1" ] ; then
  echo "Token not set, exiting ..."
  exit 1
else
  echo "Token = $ACCESS_TOKEN "
fi

if [ -z "$2" ] ; then
  echo "Realm not set, exiting ..."
  exit 1
else
  echo "Realm = $REALM "
fi

if [ -z "$3" ] ; then
  echo "Search String not set, exiting ..."
  exit 1
else
  echo "Search String = $SEARCH "
fi

### Build array of the Detectors using the three paramaters ###
DETECTORS="$(curl -sk --request GET --header 'X-SF-TOKEN: '$ACCESS_TOKEN'' 'https://api.'$REALM'.signalfx.com/v2/detector?name='$SEARCH'' | grep '"id"' | sed 's/^ *//' | cut -d' ' -f3- | tr -d '",')"

### List the Detector Names we are going to delete ###
echo ""
echo "Generating list of Detectors we are going to delete using search string $SEARCH"
echo ""
for id in $DETECTORS
do
curl -sk --request GET --header 'X-SF-TOKEN: '$ACCESS_TOKEN'' 'https://api.'$REALM'.signalfx.com/v2/detector/'$id'' | grep -e '"id"' -e '"name"' | paste - - | cut -d' ' -f3- | tr -d '",'
#curl -sk --request GET --header 'X-SF-TOKEN: '$ACCESS_TOKEN'' 'https://api.'$REALM'.signalfx.com/v2/detector/'$id'' | grep -w 'name' | sed 's/^ *//' | cut -d' ' -f3- | tr -d '",'
done 

### Prompt user to confirm the delettion or abort ###
echo ""
read -r -p "WARNING:- The above liest of detecors are about to be deleted, this cannot be undone, are you sure you want to continue? [y/N] " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
  for id in $DETECTORS
  do
  curl --request DELETE --header "Content-Type: application/json"  --header "X-SF-TOKEN: $ACCESS_TOKEN"  https://api.$REALM.signalfx.com/v2/detector/$id
  echo "Deleted $id"
  done
else
  echo "Cancelled"  
fi
