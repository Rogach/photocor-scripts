# usage:
# python2 intensity_1s.py 'input_dir_name'

import sys
import os
import itertools
import Tkinter as tk
import tkFileDialog as filedialog

if len(sys.argv) == 2:
    input_dir = sys.argv[1]
else:
    root = tk.Tk()
    root.withdraw()
    input_dir = filedialog.askdirectory()

if len(input_dir) == 0:
    exit(1)

files = []
for f in os.listdir(input_dir):
    if f.lower().endswith("txt"):
        with open(os.path.join(input_dir, f)) as input_file:
            lines = input_file.read().splitlines()
            if len(lines) > 3 and lines[2].startswith("Photocor Runtime Report"):
                files.append(lines)

with open(os.path.join(input_dir, "intensity_1s.txt"), "w") as output_file:
    t = 0
    for i, lines in enumerate(sorted(files, key = lambda lines: lines[2])):
        countLines = list(itertools.takewhile(lambda l: not l == "@", list(itertools.dropwhile(lambda l: not l.startswith("Count Rate"), lines))[1:]))
        for l in countLines:
            v = l.split(":")
            t_corrected = float(v[0]) + t
            output_file.write("\t".join([str(t_corrected), v[1]]) + "\n")
        t += len(countLines)
