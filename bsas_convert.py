# usage:
# python2 bsas_convert.py 'input_file.txt'

import sys
import re
import Tkinter as tk
import tkFileDialog as filedialog

if len(sys.argv) == 2:
    input_filename = sys.argv[1]
else:
    root = tk.Tk()
    root.withdraw()
    input_filename = filedialog.askopenfilename()

if len(input_filename) == 0:
    exit(1)

with open(input_filename) as input_file:
    lines = input_file.read().splitlines()

filenames = []
current_filename = ""
current_peaks = []
max_peaks = []

# function to select and output best peak
# remove peaks with Position < 1 or Position > 10000
# then print peak with max Area
def output_max_peak():
    global current_peaks
    global max_peaks
    acceptable_peaks = list(filter(lambda p: len(p) > 3 and 1 <= float(p[3]) <= 10000, current_peaks))
    if len(acceptable_peaks) > 0:
        best_peak = max(acceptable_peaks, key = lambda p: float(p[1]))
        series_number = re.search("\\d{5,}", current_filename).group(0)[-5:]
        max_peaks.append([series_number] + best_peak)
    current_peaks = []


assert lines[0].startswith("Files: ")

for line in lines:
    if line.startswith("Files: "):
        filenames = list(map(lambda f: f.strip(), line[7:].split(",")))
    if any(line.startswith(f) for f in filenames):
        if current_filename != "":
            output_max_peak()
        current_filename = line
    if line.startswith("   "):
        current_peaks.append(line.split())

output_max_peak()


with open(input_filename + ".rh.txt", "w") as output_file:
    for peak in sorted(max_peaks, key = lambda p: p[0]):
        output_file.write("\t".join(peak) + "\n")
