#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
DATAPATH="${SCRIPTPATH}/../data/"

for i in airports runways; do
    rm -rf "${DATAPATH}/${i}.csv"
    wget -P "${DATAPATH}" "http://ourairports.com/data/${i}.csv"
done
