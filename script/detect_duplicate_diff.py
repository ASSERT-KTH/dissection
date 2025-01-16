#!/usr/bin/env python3
import os
import hashlib
import re

root = os.path.join(os.path.dirname(__file__), '..')

md5_diff = {}

for benchmark in ['defects4j', 'bugsjar', 'bears']:
    path_benchmark = os.path.join(root, "benchmark", benchmark)
    for project in sorted(os.listdir(path_benchmark)):
        project_path = os.path.join(path_benchmark, project)
        for bug_id in sorted(os.listdir(project_path)):
            bug_key = '%s_%s_%s' % (benchmark, project, bug_id)
            bug_path = os.path.join(project_path, bug_id)
            diff_path = os.path.join(bug_path, 'path.diff')
            with open(diff_path, encoding = "ISO-8859-1") as fd:
                diff = fd.read()
                cleaned_diff = ''
                lines = diff.splitlines()
                for line in lines:
                    if len(line) == 0:
                        continue
                    if (line[0] == '-' or line[0] == '+') and ('+++' not in line and '---' not in line):
                        cleaned_diff += line + '\n'
                m = hashlib.md5()
                m.update(cleaned_diff.encode('utf-8'))
                key = m.hexdigest()
                if key in md5_diff:
                    if len(diff) > 0:
                        print(bug_key, "is duplicate with:", ''.join(md5_diff[key]))
                else:
                    md5_diff[key] = []
                md5_diff[key].append(bug_key)