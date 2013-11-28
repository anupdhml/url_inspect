#!/bin/bash

for domain_file in `ls seeds_*`
do
    echo "Doing domain $domain_file..."
    echo ''
    #python make_tables.py -f $domain_file | tee -a "log_${domain_file}"
    python make_tables.py -f $domain_file
    echo ''
    echo "Done domain $domain_file..."
    echo ''
done
