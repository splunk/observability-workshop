#!/usr/bin/bash
norum="True"  #no RUM is default
while getopts "r" option; do
  case "${option}" in
   r)  norum="False";;
   \?) #For invalid option
      echo "For RUM you have to use: [-r]"
      exit -1  
  esac    
done
if [ ${norum} == "True" ];
then
  echo "APM Only Deployment"
  RUM_TOKEN=""
  REALM=""
else
  echo "Adding RUM_TOKEN to deployment"
  if [ -z ${REALM+x} ]; then echo "REALM is unset. Please export REALM=YOUR_REALM"; fi
  if [ -z ${RUM_TOKEN+x} ]; then echo "RUM_TOKEN is unset. Please export RUM_TOKEN=YOUR_RUM_TOKEN"; fi    
fi
if [ -z ${INSTANCE+x} ]; then echo "INSTANCE is unset. Please export INSTANCE=YOUR_HOST_NAME"; fi 
envsubst '${REALM},${RUM_TOKEN},${INSTANCE}' < deployment-RUM-org.yaml > deployment.yaml
