#!/usr/local/bin/python3

"""

This script was created by Madani Napaul. 

This script generates image files (.jpg) starting with 'image1.jpg'. 
The files generated are empty images used to test the batch system created
locally. 

"""

import os

for x in range(10000):
    i = 1
    while os.path.exists(
        "/Users/madani/Documents/GitHub/cpd_aws_rekognition/CPD_AWS_REKOGNITION/enhancement/files/image%s.jpg"
        % i
    ):
        i += 1

    fh = open(
        "/Users/madani/Documents/GitHub/cpd_aws_rekognition/CPD_AWS_REKOGNITION/enhancement/files/image%s.jpg"
        % i,
        "w",
    )
