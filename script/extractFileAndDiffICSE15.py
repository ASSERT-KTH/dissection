import os, subprocess, shutil

from Config import config

root = config.get('path', 'root')
source = os.path.join(root, "benchmark", "svn-diff.d")
target = os.path.join(root, "benchmark", "icse15")


def create_diff(diff_id):
    path = os.path.join(target, diff_id)
    cmd = "cd %s; git diff --no-index buggy-version correct-version | sed -e 's/buggy-version\///g' | sed -e 's/correct-version\///g' > patch.diff" % path
    subprocess.check_output(cmd, shell=True)


def write_files(current_file_name, diff_id, old_file_content, new_file_content):
    if ".java" not in current_file_name:
        return
    output_buggy_folder = os.path.join(target, diff_id, "buggy-version", os.path.dirname(current_file_name))
    output_correct_folder = os.path.join(target, diff_id, "correct-version", os.path.dirname(current_file_name))
    if not os.path.exists(output_buggy_folder):
        os.makedirs(output_buggy_folder)
    if not os.path.exists(output_correct_folder):
        os.makedirs(output_correct_folder)
    with open(os.path.join(output_buggy_folder, os.path.basename(current_file_name)), "w") as fd:
        fd.write(old_file_content)
        fd.flush()
    with open(os.path.join(output_correct_folder, os.path.basename(current_file_name)), "w") as fd:
        fd.write(new_file_content)
        fd.flush()

count = 1

for diff in os.listdir(source):
    diff_id = diff.replace(".diff", "")
    if os.path.exists(os.path.join(target, diff_id, "patch.diff")):
        continue
    print count, diff_id
    count += 1
    with open(os.path.join(source, diff)) as fd:
        content = fd.read()
        lines = content.split("\n")

        current_file_name = None
        old_file_content = ""
        new_file_content = ""
        for line in lines:
            if len(line) == 0:
                continue
            if line == "===================================================================":
                continue
            if line[0:4] == "+++ " or line[0:4] == "--- ":
                continue
            if line[0:3] == "@@ ":
                continue 
            if line[0:7] == "Index: ":
                if current_file_name is not None:
                    write_files(current_file_name, diff_id, old_file_content, new_file_content)
                    old_file_content = ""
                    new_file_content = ""
                current_file_name = line[7:]
                print current_file_name
                continue
            if line[0] == " ":
                old_file_content += line[1:] + "\n"
                new_file_content += line[1:] + "\n"
            elif line[0] == "+":
                new_file_content += line[1:] + "\n"
            elif line[0] == "-":
                old_file_content += line[1:] + "\n"
            else:
                if current_file_name is not None:
                    write_files(current_file_name, diff_id, old_file_content, new_file_content)
                    old_file_content = ""
                    new_file_content = ""
                current_file_name = None
                # ignore
                pass
        if current_file_name is not None:
            write_files(current_file_name, diff_id, old_file_content, new_file_content)
        if os.path.exists(os.path.join(target, diff_id, "correct-version")):
            create_diff(diff_id)
            shutil.rmtree(os.path.join(target, diff_id, "correct-version"))