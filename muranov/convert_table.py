# usage:
# python2 convert_table.py 'input_file' 'output_file'

import sys
import re
import os
import codecs
import Tkinter as tk
import tkFileDialog as filedialog

if len(sys.argv) == 3:
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
else:
    tk_root = tk.Tk()
    tk_root.withdraw()
    input_file_name = filedialog.askopenfilename()
    output_file_name = filedialog.asksaveasfilename()

def parse_time(time_str):
    h,m,s = re.search("(\d{2}):(\d{2}):(\d{2})", time_str).groups()
    return float(s) + 60 * (float(m) + float(h) * 60)

with codecs.open(input_file_name, encoding="cp1251") as input_file:
    input_lines = input_file.read().splitlines()
    header = input_lines[0].split("\t")

    time_column_index = header.index("Measurement Date and Time")
    pk_column_indices = [header.index("Pk %d Mean Int" % i) for i in range(1,4)]

    row = 2
    start_time = parse_time(input_lines[row])

    with open(output_file_name, "w") as output_file:
        output_file.write("Time\tPk 1\tPk 2\tPk 3\n")

        while re.match("^\d+", input_lines[row]):
            line = input_lines[row].split("\t")
            time_str = line[time_column_index]
            pk = [float(line[i]) for i in pk_column_indices]

            if row <= 30:
                for i in range(len(pk)):
                    if pk[i] >= 4000:
                        pk[i] = 0.0

            time_since_start = ((parse_time(time_str) - start_time) % 86400) / 60
            output_file.write("%.3f" % time_since_start)

            for v in sorted(pk):
                output_file.write("\t%.3f" % v)

            output_file.write("\n")

            row += 1

            #