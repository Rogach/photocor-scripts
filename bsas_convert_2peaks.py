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

def output_max_peaks():
    global current_peaks
    global max_peaks
    acceptable_peaks = list(filter(lambda p: len(p) > 3 and 1 <= float(p[3]) <= 10000, current_peaks))
    if len(acceptable_peaks) > 0:
        two_max_area_peaks = sorted(acceptable_peaks, key = lambda p: float(p[1]))[0:2]
        peaks_sorted_by_increasing_position = sorted(two_max_area_peaks, key = lambda p: float(p[3]))
        output_line = sum(peaks_sorted_by_increasing_position, [])
        if len(output_line) <= 5:
            output_line += ['0','0','0','0','0']
        series_number = re.search("\\d{5,}", current_filename).group(0)[-5:]
        max_peaks.append([series_number] + output_line)
    current_peaks = []


assert lines[0].startswith("Files: ")

for line in lines:
    if line.startswith("Files: "):
        filenames = list(map(lambda f: f.strip(), line[7:].split(",")))
    if any(line.startswith(f) for f in filenames):
        if current_filename != "":
            output_max_peaks()
        current_filename = line
    if line.startswith("   "):
        current_peaks.append(line.split())

output_max_peaks()


with open(input_filename + ".rh.txt", "w") as output_file:
    for peak in sorted(max_peaks, key = lambda p: p[0]):
        output_file.write("\t".join(peak) + "\n")
