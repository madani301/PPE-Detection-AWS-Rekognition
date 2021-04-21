#!/usr/local/bin/python3

"""

This script was created by Madani Napaul. 

This script extracts all the file names in the specified 
directory and store them into an array in a JSON file. 

"""

from os import listdir
from os.path import isfile, join
import json
import sys

res = []

onlyfiles = [
    f
    for f in listdir(
        "/Users/madani/Documents/GitHub/cpd_aws_rekognition/enhancement/files"
    )
    if isfile(
        join("/Users/madani/Documents/GitHub/cpd_aws_rekognition/enhancement/files", f)
    )
]

with open("data.json", "w") as outfile:
    for items in onlyfiles:
        res.append(items)
    json.dump(res, outfile)
