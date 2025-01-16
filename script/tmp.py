#!/usr/bin/env python
import os
import subprocess
import tempfile
import json
import collections
import sys
from Config import config

root = config.get('path', 'root')

file1 = ""
file2 = ""
with open(os.path.join(root, "features", "bears.json")) as fd:
    data = json.load(fd)
    for bug in data:
        bug_id = bug["bugId"]
        file1 += "%s\t%s\n" % (bug_id, bug["metrics"]["patchSize"])
        file2 += "%s\t%s\n" % (bug_id, bug["metrics"]["nbFiles"])

with open("patchSize.csv", "w") as fd:
    fd.write(file1)
with open("nbFiles.csv", "w") as fd:
    fd.write(file2)




