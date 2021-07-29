#!/usr/bin/env python3

import logging

import update_collette_data
import update_cosmos_data
import update_gate1_data
import update_globus_data
import update_tauck_data

def main():

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

    file_handler = logging.FileHandler(filename='update_competitor_data.log', mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    
    update_collette_data.main()
    update_cosmos_data.main()
    update_gate1_data.main()
    update_globus_data.main()
    update_tauck_data.main()

if __name__ == '__main__': main()